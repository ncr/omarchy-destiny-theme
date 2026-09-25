#!/usr/bin/env python3
"""Install the optional Destiny Wallpapers companion in a user-local prefix."""
import argparse
import json
from pathlib import Path
import shlex
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
MARKER = '# Destiny Wallpapers companion'


def desktop_quote(value):
    # Desktop Exec has its own escaping, distinct from shell quoting.
    value = str(value).replace('\\', '\\\\').replace('"', '\\"').replace('`', '\\`').replace('$', '\\$').replace('%', '%%')
    return '"' + value + '"'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--prefix', type=Path, default=Path.home()/'.local')
    ap.add_argument('--uninstall', action='store_true')
    args = ap.parse_args()
    prefix = args.prefix.expanduser().resolve()
    app = prefix/'share/destiny-wallpapers'
    launcher = prefix/'bin/destiny-wallpapers'
    desktop = prefix/'share/applications/destiny-wallpapers.desktop'
    if args.uninstall:
        if not (app/'install.json').is_file():
            ap.error('No companion installation recorded at this prefix')
        if launcher.is_file() and MARKER in launcher.read_text():launcher.unlink()
        if desktop.is_file() and 'StartupWMClass=destiny-wallpapers' in desktop.read_text():desktop.unlink()
        for name in ('view_wallpapers.py','wallpaper-viewer.ini','install.json'):
            (app/name).unlink(missing_ok=True)
        if not any(app.iterdir()):app.rmdir()
        print('Companion removed. Wallpaper files and theme checkout retained.')
    else:
        if not shutil.which('imv'):
            ap.error('imv is required; on Omarchy run: omarchy pkg add imv')
        if launcher.exists() and MARKER not in launcher.read_text():
            ap.error(f'Refusing to overwrite an unrelated executable: {launcher}')
        if desktop.exists() and 'StartupWMClass=destiny-wallpapers' not in desktop.read_text():
            ap.error(f'Refusing to overwrite an unrelated desktop entry: {desktop}')
        for directory in (app,launcher.parent,desktop.parent):directory.mkdir(parents=True,exist_ok=True)
        for name in ('view_wallpapers.py','wallpaper-viewer.ini'):
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
        (app/'install.json').write_text(json.dumps({'theme_root':str(ROOT),'prefix':str(prefix),'version':1},indent=2)+'\n')
        print(f'Installed Destiny Wallpapers: {launcher}\nWallpaper source: {ROOT}')
    refresh = shutil.which('update-desktop-database')
    if refresh and desktop.parent.is_dir():
        subprocess.run([refresh,str(desktop.parent)],check=True)


if __name__ == '__main__':main()
