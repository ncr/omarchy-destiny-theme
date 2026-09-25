"""Two choices in the user's terminal; no graphical setup toolkit."""
import argparse
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import textwrap


def prompt(plan, apply):
    by_id = {o['profile']: o for o in plan['options']}
    def size(id):
        value = by_id[id]['total_bytes']
        return f'{value/1_000_000:.1f} MB' if value is not None else 'size unavailable'
    options = [(f"Perfectly good — {size(plan['recommended'])}", 'auto'),
               (f"I don't care, I want the biggest everything — {size(plan['biggest'])}", 'biggest')]
    explanation = plan['reason']
    if plan['recommended'] == plan['biggest']:
        explanation += '\nBoth use the same set today; smaller matching exports are not available yet.'
    columns = shutil.get_terminal_size(fallback=(80,24)).columns
    width = max(30, columns-4)
    explanation = '\n'.join(textwrap.fill(line, width) for line in explanation.splitlines())
    header = 'Destiny Wallpapers\n\n' + explanation + '\n'
    action = 'Enter applies to Destiny and opens the gallery.' if apply else 'Enter opens the gallery; your desktop stays unchanged.'
    gum = shutil.which('gum')
    if gum and columns >= 72:
        result = subprocess.run([gum, 'choose', '--header='+header+textwrap.fill(action, width),
                                 '--height=2', '--cursor.foreground=10', '--selected.foreground=10',
                                 '--label-delimiter=\t', *[title+'\t'+value for title,value in options]],
                                stdout=subprocess.PIPE, text=True)
        return result.stdout.strip() if result.returncode == 0 and result.stdout.strip() in ('auto','biggest') else None
    print(header)
    for i,(title, _) in enumerate(options,1):
        print(f'  {i}. {title}')
    print('\n'+action)
    try:
        answer = input('Choose [1/2, Enter=1, q=cancel]: ').strip().lower()
        while answer not in ('','1','2','q'):
            answer = input('Choose 1, 2 or q: ').strip().lower()
        return None if answer == 'q' else ('biggest' if answer == '2' else 'auto')
    except (KeyboardInterrupt, EOFError):
        return None


def choose_profile(plan, apply):
    if sys.stdin.isatty() and sys.stdout.isatty():
        return prompt(plan, apply)
    terminal = shutil.which('xdg-terminal-exec')
    if not terminal or not (os.environ.get('WAYLAND_DISPLAY') or os.environ.get('DISPLAY')):
        raise ValueError('Run destiny-wallpapers --configure in a terminal to choose a wallpaper set.')
    with tempfile.TemporaryDirectory(prefix='destiny-setup-') as directory:
        request, result = Path(directory)/'request.json', Path(directory)/'result.json'
        request.write_text(json.dumps({'plan':plan, 'apply':apply}))
        subprocess.run([terminal, '--title=Destiny Wallpapers setup', '--app-id=destiny-wallpapers-setup', sys.executable, str(Path(__file__).resolve()),
                        '--request', str(request), '--result', str(result)], check=False)
        if not result.is_file():
            return None
        value = json.loads(result.read_text())
        return value if value in ('auto','biggest') else None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--request', type=Path, required=True)
    parser.add_argument('--result', type=Path, required=True)
    args = parser.parse_args()
    def cancel(*_):
        raise KeyboardInterrupt
    signal.signal(signal.SIGHUP, cancel)
    signal.signal(signal.SIGTERM, cancel)
    value = None
    try:
        request = json.loads(args.request.read_text())
        value = prompt(request['plan'], request['apply'])
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        args.result.write_text(json.dumps(value))


if __name__ == '__main__':
    main()
