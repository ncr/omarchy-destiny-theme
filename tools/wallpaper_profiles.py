"""Monitor selection and first-run setup for the optional wallpaper companion."""
import base64
import time
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


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


def assess(profile, screens):
    """Physical pixel density for desktop cover, independent of UI scaling."""
    w, h = profile['size']
    paths = profile.get('paths', [])
    # Measure the files users actually have, rather than guessing from pixels
    # or treating compressed file size as decoded RAM use.
    sizes = [p.stat().st_size for p in paths]
    rows = []
    for m in screens:
        fill = max(m['width']/w, m['height']/h)
        fit = min(m['width']/w, m['height']/h)
        crop = max(0., 1 - (m['width']*m['height'])/(w*h*fill*fill))
        rows.append(dict(name=m['name'], width=m['width'], height=m['height'],
                         scale=m['scale'], factor=fill, crop=crop,
                         text_px=profile['min_text_px']*fit/m['scale'],
                         upscale=fill > 1.000001))
    return dict(profile=profile['id'], label=profile['label'], size=profile['size'],
                total_bytes=sum(sizes) if sizes else None, file_count=len(sizes),
                average_bytes=sum(sizes)/len(sizes) if sizes else None,
                displays=rows, upscale=any(r['upscale'] for r in rows))


def quality_score(option, preferred=None):
    rows = option['displays']
    if not rows:
        return (0, 0, 0, 0, 0, 0, option['profile'])
    # First avoid enlargement on ANY display. Then minimize worst cropping and
    # area-weighted cropping. Among equally suitable sets, prefer fewer bytes,
    # then fewer pixels. Focus changes must never alter the recommendation.
    worst_scale = max(1., max(r['factor'] for r in rows))
    relevant = [r for r in rows if r['name'] == preferred] if preferred else rows
    crop = max(r['crop'] for r in relevant)
    area = sum(r['width']*r['height'] for r in relevant)
    average = sum(r['crop']*r['width']*r['height'] for r in relevant)/area
    return (option['upscale'], round(worst_scale, 6), round(crop, 6), round(average, 6),
            option['total_bytes'] if option['total_bytes'] is not None else math.inf,
            option['size'][0]*option['size'][1], option['profile'])


def recommendation_reason(option, options):
    rows = option['displays']
    if not rows:
        return 'No monitors detected; the desktop will stay unchanged.'
    if option['upscale']:
        return f"No set is large enough; this needs the least enlargement ({max(r['factor'] for r in rows):.2f}×)."
    cheaper = sorted((o for o in options if o['total_bytes'] is not None and option['total_bytes'] is not None and o['total_bytes'] < option['total_bytes']), key=lambda o:o['total_bytes'])
    for other in cheaper:
        enlarged = [r for r in other['displays'] if r['upscale']]
        if enlarged:
            row = max(enlarged, key=lambda r:r['factor'])
            return f"The cheaper set needs {row['factor']:.2f}× enlargement on {row['name']}; this one does not."
        crop = max(r['crop'] for r in other['displays'])
        own_crop = max(r['crop'] for r in rows)
        if crop > own_crop + .01:
            return (f"The cheaper {other['label']} set crops {crop:.0%} of the image; " +
                    ('this set keeps the whole sheet.' if own_crop < .01 else f'this set limits cropping to {own_crop:.0%}.'))
    crop = max(r['crop'] for r in rows)
    if crop > .01:
        return f"Smallest set with the best available fit; mixed screen proportions still crop up to {crop:.0%}."
    return f"Smallest set that fits all {len(rows)} displays without enlargement or cropping."


def plan(root, requested='auto', monitor=None, detected=None):
    manifest, available = profiles(root)
    detected = monitors() if detected is None else detected
    if monitor and monitor not in {m['name'] for m in detected}:
        raise ValueError(f'Monitor {monitor!r} is not connected')
    options = sorted([assess(p, detected) for p in available], key=lambda o: quality_score(o, monitor))
    recommended = options[0]['profile'] if detected else manifest['default']
    recommended_option = next((o for o in options if o['profile']==recommended), options[0])
    ratio = recommended_option['size'][0]/recommended_option['size'][1]
    matching = [o for o in options if abs(o['size'][0]/o['size'][1]-ratio) < .000001]
    biggest = max(matching, key=lambda o:(o['size'][0]*o['size'][1], o['total_bytes'] or 0, o['profile']))['profile']
    choice = biggest if requested == 'biggest' else (requested if requested != 'auto' else recommended)
    profile = next((p for p in available if p['id'] == choice), None)
    if profile is None:
        if requested != 'auto':
            raise ValueError(f'Unavailable profile: {requested}')
        profile = available[0]
        recommended = profile['id']
    chosen = next(o for o in options if o['profile'] == profile['id'])
    warnings = []
    small = [r for r in chosen['displays'] if r['text_px'] < 12]
    if small:
        warnings.append(f"Small labels in the full-sheet viewer can be as small as {min(r['text_px'] for r in small):.1f} logical pixels. Larger-type layouts are not published yet.")
    if not detected:
        warnings.append('Monitor detection is unavailable. Using the shipped default; desktop settings will stay unchanged.')
    if len(detected) > 1:
        warnings.append('One shared wallpaper is used on all monitors. The recommendation considers every connected display.')
    return dict(profile=profile['id'], recommended=recommended, biggest=biggest,
                reason=recommendation_reason(recommended_option, options), options=options,
                label=profile['label'], size=profile['size'], count=len(profile['paths']),
                screen=detected[0] if detected else None, monitors=detected, warnings=warnings,
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
    from wallpaper_setup_cli import choose_profile
    return choose_profile(p, apply)


def refresh_desktop(target, current):
    subprocess.run(['omarchy','theme','bg','set',str(target)],check=True,timeout=15)
    # The shell ignores set(path) when the path is unchanged. Use its existing
    # theme-transition API with an uncached snapshot and the same final path.
    # The canonical link stays intact for Omarchy's next-background command.
    shell=shutil.which('omarchy-shell')
    if not shell:return
    def payload(name):
        path=current/'theme'/name
        return base64.b64encode(path.read_bytes() if path.is_file() else b'').decode()
    with tempfile.TemporaryDirectory(prefix='destiny-refresh-') as directory:
        snapshot=Path(directory)/target.name
        shutil.copyfile(target,snapshot)
        result=subprocess.run(['omarchy','shell','-q','background','themeTransition','',str(snapshot),str(target),
                               payload('colors.toml'),payload('shell.json')],check=False,timeout=10)
        if result.returncode==0:time.sleep(3)


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
    if selected in {s.name for s in sources} and (changed or (current/'background').resolve() != (destination/selected).resolve()):
        refresh_desktop(destination/selected,current)
    return changed


def notify_selection(p, desktop):
    notifier = shutil.which('omarchy-notification-send')
    fallback = shutil.which('notify-send')
    if not notifier and not fallback:
        return
    resolution=' × '.join(map(str,p['size']))
    title=('Optimal desktop wallpaper resolution applied' if p['profile']==p['recommended']
           else 'Desktop wallpaper resolution applied')
    title+=': '+resolution
    if not desktop:
        return
    scope=''
    command=shutil.which('destiny-wallpapers')
    if notifier and command:
        args=[notifier,'--app-name','Destiny Wallpapers','-t','9000',title,
              scope+'Click to change settings.', '--exec',command,'--configure']
    else:
        args=[notifier or fallback,title,scope+'Settings: destiny-wallpapers --configure']
    try:
        subprocess.run(args,check=False,timeout=5,capture_output=True)
    except (OSError,subprocess.SubprocessError):
        pass  # A notification failure must never prevent the gallery opening.


def initialize(root, p, requested='auto', monitor=None, configure=False):
    lock=setup_path().with_suffix('.lock')
    lock.parent.mkdir(parents=True,exist_ok=True)
    with lock.open('a') as handle:
        fcntl.flock(handle,fcntl.LOCK_EX)
        return _initialize(root,p,requested,monitor,configure)


def _initialize(root, p, requested='auto', monitor=None, configure=False):
    previous = read_setup()
    # Old chooser preferences migrate to automatic; only explicit new settings
    # can establish a manual override.
    if previous.get('version') != 6 or previous.get('root') != str(root):
        requested='auto'
    p = plan(root, requested, monitor, p['monitors'])
    desktop=bool(p['screen']) and active_destiny(current_dir())
    if configure:
        choice=announce({**p,'setting':requested}, desktop)
        if not choice:
            return None
        if choice not in {'auto',*(o['profile'] for o in p['options'])}:
            raise ValueError('Invalid wallpaper setting')
        requested=choice
        p=plan(root,requested,monitor,p['monitors'])
    updated=sync(p)
    if p['screen']:
        changed=(previous.get('version')!=6 or previous.get('root')!=str(root)
                 or previous.get('selected')!=p['profile']
                 or (desktop and (updated or previous.get('desktop_selected')!=p['profile'])))
        save_setup(dict(version=6,root=str(root),profile=requested,monitor=monitor,
                        selected=p['profile'],desktop_selected=p['profile'] if desktop else previous.get('desktop_selected')))
        if changed:
            notify_selection(p,desktop)
    return p
