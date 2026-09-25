"""Monitor selection and first-run setup for the optional wallpaper companion."""
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time


def monitors():
    try:
        result = subprocess.run(['hyprctl', '-j', 'monitors'], capture_output=True,
                                text=True, check=True, timeout=3)
        return normalize_monitors(json.loads(result.stdout))
    except (OSError, ValueError, subprocess.SubprocessError):
        return []


def normalize_monitors(rows):
    out = []
    if not isinstance(rows, list):
        return out
    for row in rows:
        try:
            if row.get('disabled') or row.get('name') == 'FALLBACK':
                continue
            w, h, scale = int(row['width']), int(row['height']), float(row.get('scale', 1))
            if min(w, h, scale) <= 0 or not math.isfinite(scale):
                continue
            if int(row.get('transform', 0)) % 2:
                w, h = h, w
            out.append(dict(name=str(row['name']), width=w, height=h, scale=scale,
                            focused=bool(row.get('focused'))))
        except (KeyError, TypeError, ValueError, AttributeError, OverflowError):
            continue
    return out


def profiles(root):
    manifest = json.loads((root/'docs/collection/profiles.json').read_text())
    ids = [x['id'] for x in json.loads((root/'docs/collection/catalog.json').read_text())['finalized']]
    ready = []
    for profile in manifest['profiles']:
        if [x['id'] for x in profile['files']] != ids:
            raise ValueError(f"Incomplete collection in profile {profile['id']}")
        paths = [(root/x['file']).resolve() for x in profile['files']]
        if any(not p.is_relative_to(root.resolve()) for p in paths):
            raise ValueError('Wallpaper profile points outside the checkout')
        if len({p.name for p in paths}) != len(paths):
            raise ValueError('Duplicate wallpaper names in profile')
        if len(profile['size']) != 2 or min(profile['size']) <= 0:
            raise ValueError('Invalid profile dimensions')
        if all(p.is_file() for p in paths):
            ready.append({**profile, 'paths': paths})
    if not ready:
        raise ValueError('No complete wallpaper profile is installed. Reinstall from a complete checkout.')
    return manifest, ready


def plan(root, requested='auto', monitor=None, detected=None):
    manifest, available = profiles(root)
    detected = monitors() if detected is None else detected
    screen = next((m for m in detected if m['name'] == monitor), None) if monitor else next(
        (m for m in detected if m['focused']), detected[0] if detected else None)
    if monitor and screen is None:
        raise ValueError(f'Monitor {monitor!r} is not connected')
    if requested != 'auto':
        profile = next((p for p in available if p['id'] == requested), None)
        if profile is None:
            raise ValueError(f'Unavailable profile: {requested}')
    elif screen:
        ratio = screen['width']/screen['height']
        profile = min(available, key=lambda p: abs(math.log((p['size'][0]/p['size'][1])/ratio)))
    else:
        profile = next((p for p in available if p['id'] == manifest['default']), available[0])
    warnings = []
    if screen:
        factor = min(screen['width']/profile['size'][0], screen['height']/profile['size'][1])
        text_size = profile['min_text_px'] * factor / screen['scale']
        if text_size < 12:
            warnings.append(f'Small labels will be about {text_size:.1f} logical pixels. Larger-type layouts for small screens are not published yet.')
        if abs(screen['width']/screen['height'] - profile['size'][0]/profile['size'][1]) > .04:
            warnings.append('This screen has no exact aspect-ratio variant. The viewer fits the full sheet; the desktop may crop it.')
    else:
        warnings.append('Monitor detection is unavailable. Using the shipped default; desktop settings will stay unchanged.')
    if len(detected) > 1:
        warnings.append('Omarchy currently shares one wallpaper across monitors. Selection follows the focused screen; other screens may crop it.')
    return dict(profile=profile['id'], label=profile['label'], size=profile['size'], count=len(profile['paths']),
                screen=screen, monitors=detected, warnings=warnings,
                files=[str(p) for p in profile['paths']], hashes=[r['sha256'] for r in profile['files']])


def current_dir():
    # Omarchy itself uses this path, not XDG_STATE_HOME.
    return Path.home()/'.local/state/omarchy/current'


def active_destiny(current):
    try:
        return (current/'theme.name').read_text().strip() == 'destiny'
    except OSError:
        return False


def setup_path():
    return Path(os.environ.get('XDG_STATE_HOME', Path.home()/'.local/state'))/'destiny-wallpapers/setup.json'


def read_setup():
    try:
        value = json.loads(setup_path().read_text())
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError):
        return {}


def save_setup(data):
    target = setup_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(dir=target.parent, prefix='.setup-')
    try:
        with os.fdopen(fd, 'w') as stream:
            json.dump(data, stream, indent=2)
            stream.write('\n')
        os.replace(name, target)
    finally:
        Path(name).unlink(missing_ok=True)


def announce(p, apply):
    screen = p['screen']
    detected = (f"{screen['name']}: {screen['width']} × {screen['height']}, scale {screen['scale']:g}" if screen else 'Monitor unavailable')
    text = (f"Detected: {detected}\nSelected: {p['label']} · {p['count']} wallpapers\n\n" +
            ('The Destiny desktop collection will use this format. Your current sheet will be kept.\n' if apply else
             'The viewer will use this format. Your desktop theme stays unchanged.\n') +
            '\n'.join(p['warnings']) +
            '\n\nSetup continues automatically in 10 seconds, then the viewer opens. Cancel makes no changes.\n'
            'Later: use --profile or --monitor to override the automatic selection.')
    zenity = shutil.which('zenity')
    if not zenity:
        print(text + '\nInstall zenity to enable the automatic first-run setup.')
        return False
    proc = subprocess.Popen([zenity, '--progress', '--title=Destiny Wallpapers — first launch',
                             '--width=660', '--no-markup', '--text='+text, '--percentage=0', '--auto-close'],
                            stdin=subprocess.PIPE, text=True)
    try:
        for percent in range(0, 101, 10):
            if proc.poll() is not None:
                return False
            proc.stdin.write(f'{percent}\n')
            proc.stdin.flush()
            if percent < 100:
                time.sleep(1)
        proc.stdin.close()
        return proc.wait(timeout=5) == 0
    except (BrokenPipeError, subprocess.TimeoutExpired):
        proc.terminate()
        proc.wait()
        return False


def sync(p, current=None):
    """Replace only this collection's files in Omarchy's disposable theme stage."""
    current = current or current_dir()
    if not p['screen'] or not active_destiny(current):
        return False
    theme = current/'theme'
    destination = theme/'backgrounds'
    # Never follow a theme stage symlink into a source checkout.
    if theme.is_symlink() or destination.is_symlink() or not destination.is_dir():
        raise ValueError('Expected a regular staged Omarchy backgrounds directory')
    sources = [Path(x) for x in p['files']]
    for src, digest in zip(sources, p['hashes'], strict=True):
        if hashlib.sha256(src.read_bytes()).hexdigest() != digest:
            raise ValueError(f'Wallpaper changed since packaging: {src.name}')
    selected = Path(os.readlink(current/'background')).name if (current/'background').is_symlink() else None
    changed = False
    # Stage the whole set first so an out-of-space failure cannot leave half copied.
    with tempfile.TemporaryDirectory(prefix='.destiny-', dir=theme) as work:
        stage = Path(work)
        pending = []
        for src, digest in zip(sources, p['hashes'], strict=True):
            target = destination/src.name
            if target.exists() and not target.is_symlink() and hashlib.sha256(target.read_bytes()).hexdigest() == digest:
                continue
            shutil.copyfile(src, stage/src.name)
            pending.append(src.name)
        for name in pending:
            os.replace(stage/name, destination/name)
        changed = bool(pending)
    # Keep custom user wallpapers selected. Owned sheets always use stage paths,
    # so Omarchy's next-background operation can match its current-file list.
    if changed and selected in {s.name for s in sources}:
        subprocess.run(['omarchy', 'theme', 'bg', 'set', str(destination/selected)], check=True, timeout=15)
    return changed


def initialize(root, p, requested='auto', monitor=None):
    previous = read_setup()
    if previous.get('version') != 2 or previous.get('root') != str(root):
        if not announce(p, bool(p['screen']) and active_destiny(current_dir())):
            return False
    sync(p)
    # No monitor: browse fallback, but retry the setup when discovery works.
    if p['screen']:
        save_setup(dict(version=2, root=str(root), profile=requested, monitor=monitor))
    return True
