#!/usr/bin/env python3
"""Install the optional Destiny Wallpapers companion in a user-local prefix."""
import argparse
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
MARKER = '# Destiny Wallpapers companion'
RUNTIME = ('view_wallpapers.py', 'wallpaper_profiles.py', 'wallpaper_setup_cli.py', 'wallpaper-viewer.ini')


def desktop_quote(value):
    # Desktop Exec has its own escaping, distinct from shell quoting.
    value = str(value).replace('\\', '\\\\').replace('"', '\\"').replace('`', '\\`').replace('$', '\\$').replace('%', '%%')
    return '"' + value + '"'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--prefix', type=Path, default=Path.home()/'.local')
    ap.add_argument('--uninstall', action='store_true')
    ap.add_argument('--no-launch', action='store_true', help='Install without opening the app')
    args = ap.parse_args()
    prefix = args.prefix.expanduser().resolve()
    app = prefix/'share/destiny-wallpapers'
    launcher = prefix/'bin/destiny-wallpapers'
    desktop = prefix/'share/applications/destiny-wallpapers.desktop'
    local = prefix == (Path.home()/'.local').resolve()
    hook = Path.home()/'.config/omarchy/hooks/theme-set.d/destiny-wallpapers'
    if local and hook.exists() and MARKER not in hook.read_text():
        ap.error(f'Refusing to replace an unrelated hook: {hook}')
    if args.uninstall:
        if not (app/'install.json').is_file():
            ap.error('No companion installation recorded at this prefix')
        if launcher.is_file() and MARKER in launcher.read_text():launcher.unlink()
        if desktop.is_file() and 'StartupWMClass=destiny-wallpapers' in desktop.read_text():desktop.unlink()
        if local and hook.is_file() and MARKER in hook.read_text():hook.unlink()
        for name in (*RUNTIME, 'wallpaper_setup_ui.py', 'install.json', 'destiny-wallpapers'):
            (app/name).unlink(missing_ok=True)
        if not any(app.iterdir()):app.rmdir()
        print('Companion removed. Wallpaper files and theme checkout retained.')
    else:
        if not shutil.which('imv'):
            ap.error('imv is required; on Omarchy run: omarchy pkg add imv')
        if local and not (shutil.which('foot') or shutil.which('xdg-terminal-exec')):
            ap.error('foot or xdg-terminal-exec is required for setup from the application menu')
        if launcher.exists() and MARKER not in launcher.read_text():
            ap.error(f'Refusing to overwrite an unrelated executable: {launcher}')
        if desktop.exists() and 'StartupWMClass=destiny-wallpapers' not in desktop.read_text():
            ap.error(f'Refusing to overwrite an unrelated desktop entry: {desktop}')
        for directory in (app,launcher.parent,desktop.parent):directory.mkdir(parents=True,exist_ok=True)
        print('Installing Destiny Wallpapers, its application-menu entry and automatic format selection.', flush=True)
        (app/'wallpaper_setup_ui.py').unlink(missing_ok=True)
        for name in RUNTIME:
            shutil.copy2(ROOT/'tools'/name,app/name)
        launcher.write_text('#!/bin/sh\n'+MARKER+'\n'+
            'export DESTINY_THEME_ROOT='+shlex.quote(str(ROOT))+'\n'+
            'exec '+shlex.quote(sys.executable)+' '+shlex.quote(str(app/'view_wallpapers.py'))+
            ' --collection finalized "$@"\n')
        launcher.chmod(0o755)
        desktop.write_text('[Desktop Entry]\nType=Application\nName=Destiny Wallpapers\n'
            'Comment=Browse the Destiny wallpaper collection\n'
            'Exec='+desktop_quote(launcher)+'\nIcon=preferences-desktop-wallpaper\n'
            'Terminal=false\nCategories=Graphics;Viewer;\n'
            'Keywords=wallpaper;tapety;destiny;blueprint;\nStartupWMClass=destiny-wallpapers\n')
        if local and shutil.which('omarchy'):
            hook_source = app/'destiny-wallpapers'
            hook_source.write_text('#!/bin/sh\n'+MARKER+'\n'
                '[ "$1" = destiny ] || exit 0\nexec '+shlex.quote(str(launcher))+' --sync-backgrounds\n')
            subprocess.run(['omarchy', 'hook', 'install', 'theme-set', str(hook_source)], check=True)
        (app/'install.json').write_text(json.dumps({'theme_root':str(ROOT),'prefix':str(prefix),'version':5},indent=2)+'\n')
        print(f'Installed Destiny Wallpapers: {launcher}\nWallpaper source: {ROOT}')
    refresh = shutil.which('update-desktop-database')
    if refresh and desktop.parent.is_dir():
        subprocess.run([refresh,str(desktop.parent)],check=True)
    if not args.uninstall and not args.no_launch and local:
        if os.environ.get('WAYLAND_DISPLAY') or os.environ.get('DISPLAY'):
            log = app/'launch.log'
            with log.open('a') as stream:
                subprocess.Popen([str(launcher)], stdout=stream, stderr=stream, start_new_session=True)
            print('Opening Destiny Wallpapers. First launch explains the detected monitor and selected format.')
        else:
            print('No graphical session detected. Open Destiny Wallpapers from the application menu later.')


if __name__ == '__main__':main()
