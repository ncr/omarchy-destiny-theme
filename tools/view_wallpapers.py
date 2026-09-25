#!/usr/bin/env python3
"""Full-screen development gallery, using imv's native live image reload."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(os.environ.get('DESTINY_THEME_ROOT', Path(__file__).resolve().parents[1])).resolve()
DEVELOPMENT = ROOT / 'concepts/development'
EXTENSIONS = {'.webp', '.png', '.jpg', '.jpeg'}


def collection(directory):
    """Only numbered wallpaper masters, never comparison crops or thumbnails."""
    return sorted(p for p in directory.iterdir()
                  if p.is_file() and p.suffix.lower() in EXTENSIONS
                  and re.match(r'^\d{2,3}-', p.name))


def finalized_collection():
    """Use the retained registry; a clean checkout can show shipped originals.

    The generated ranking gallery is optional and is not a runtime dependency.
    Rejected Century studies are never discovered by scanning render folders.
    """
    registry = ROOT / 'docs/collection/catalog.json'
    if not registry.exists():
        return collection(ROOT / 'backgrounds')
    files = []
    for entry in json.loads(registry.read_text())['finalized']:
        source = (ROOT / entry['source']).resolve()
        if not source.is_relative_to(ROOT):
            raise ValueError('Collection source must be inside the theme checkout')
        if not source.is_file() and entry['id'].startswith('o'):
            source = ROOT / 'backgrounds' / source.name
        if source.is_file():
            files.append(source)
    return files


def select(files, query):
    if query is None:
        return files[0]
    if query.isdecimal():
        matches = [p for p in files if int(p.name.split('-')[0]) == int(query)]
    else:
        matches = [p for p in files if query.casefold() in p.name.casefold()]
    if len(matches) != 1:
        raise ValueError(f'Expected one wallpaper for {query!r}; found {len(matches)}. Use --list.')
    return matches[0]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('start', nargs='?', help='Wallpaper number or name, e.g. 9 or tether')
    ap.add_argument('--collection', choices=['development', 'finalized'], default='development',
                    help='Finalized reads the retained collection, with shipped backgrounds as fallback')
    ap.add_argument('--dir', type=Path, help='View a different render directory')
    ap.add_argument('--render', action='store_true', help='Regenerate the development set before opening')
    ap.add_argument('--list', action='store_true', help='List the selected collection and exit')
    args = ap.parse_args()
    directory = args.dir.expanduser().resolve() if args.dir else DEVELOPMENT
    if args.render and args.collection == 'finalized':
        ap.error('Render sources separately; --render only supports the development collection')
    if args.render:
        subprocess.run([sys.executable, str(ROOT/'tools/make_wallpapers.py'),
                        '--out', str(directory)], check=True)
    # A fresh checkout can still browse the shipped set without rendering.
    if args.dir is None and not directory.is_dir():
        directory = ROOT / 'backgrounds'
    try:
        retained = args.collection == 'finalized' and args.dir is None
        files = finalized_collection() if retained else collection(directory)
        if not files:
            raise ValueError(f'No numbered wallpapers in {directory}')
        if retained and args.start and args.start.isdecimal():
            index = int(args.start) - 1
            if not 0 <= index < len(files):
                raise ValueError(f'Wallpaper position must be between 1 and {len(files)}')
            first = files[index]
        else:
            first = select(files, args.start)
    except (OSError, ValueError) as exc:
        ap.error(str(exc))
    if args.list:
        print('\n'.join(str(p) for p in files))
        return
    viewer = shutil.which('imv')
    if not viewer:
        ap.error('imv is required. On Omarchy: omarchy pkg add imv')
    env = os.environ.copy()
    env['imv_config'] = str(Path(__file__).with_name('wallpaper-viewer.ini'))
    os.execve(viewer, [viewer, '-f', '-s', 'full', '-b', '000000',
                      '-i', 'destiny-wallpapers', '-n', str(first),
                      *map(str, files)], env)


if __name__ == '__main__':
    main()
