"""Optional wallpaper settings; normal launches never open this TUI."""
import argparse
import curses
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile


def settings(plan):
    rows=[('auto','Automatic · Optimal set')]
    for o in plan['options']:
        size=' × '.join(map(str,o['size']))
        mb=f"{o['total_bytes']/1_000_000:.1f} MB" if o.get('total_bytes') is not None else 'Size unknown'
        rows.append((o['profile'],size+' / '+mb))
    return rows


def tui(screen,plan,apply):
    try:curses.curs_set(0)
    except curses.error:pass
    screen.keypad(True)
    rows=settings(plan)
    selected=next((i for i,(key,_) in enumerate(rows) if key==plan.get('setting','auto')),0)
    while True:
        screen.erase()
        h,w=screen.getmaxyx()
        left=max(1,(w-66)//2)
        top=max(0,(h-min(len(rows)*3+8,h))//2)
        def put(y,text,style=0):
            if 0<=y<h-1:
                try:screen.addstr(y,left,text[:max(0,w-left-1)],style)
                except curses.error:pass
        put(top,'DESTINY / WALLPAPER SETTINGS',curses.A_BOLD)
        count=max(1,(h-top-6)//3)
        start=selected//count*count
        for j,(key,label) in enumerate(rows[start:start+count]):
            i=start+j
            style=curses.A_BOLD|(curses.A_REVERSE if i==selected else 0)
            put(top+3+j*3,('▶ ' if i==selected else '  ')+label,style)
        put(h-2,'↑↓ Choose   ENTER Save   ESC Cancel',curses.A_BOLD)
        screen.refresh()
        key=screen.get_wch()
        if key in (curses.KEY_DOWN,'j','\t'):selected=(selected+1)%len(rows)
        elif key in (curses.KEY_UP,'k'):selected=(selected-1)%len(rows)
        elif key in ('\n','\r',curses.KEY_ENTER):return rows[selected][0]
        elif key in ('\x1b','q','Q'):return None


def prompt(plan,apply):
    if sys.stdin.isatty() and sys.stdout.isatty() and os.environ.get('TERM')!='dumb':
        try:return curses.wrapper(tui,plan,apply)
        except KeyboardInterrupt:return None
    rows=settings(plan)
    print('DESTINY / WALLPAPER SETTINGS')
    for i,(_,label) in enumerate(rows,1):print(f'{i}. {label}')
    try:
        while True:
            value=input('Number, Enter=automatic, q=cancel: ').strip().lower()
            if value=='q':return None
            if value=='':return 'auto'
            if value.isdecimal() and 1<=int(value)<=len(rows):return rows[int(value)-1][0]
    except (KeyboardInterrupt,EOFError):return None


def choose_profile(plan, apply):
    if sys.stdin.isatty() and sys.stdout.isatty():
        return prompt(plan, apply)
    foot = shutil.which('foot')
    terminal = shutil.which('xdg-terminal-exec')
    if not (foot or terminal) or not (os.environ.get('WAYLAND_DISPLAY') or os.environ.get('DISPLAY')):
        raise ValueError('Run destiny-wallpapers --configure in a terminal to review the optimal wallpaper set.')
    with tempfile.TemporaryDirectory(prefix='destiny-setup-') as directory:
        request, result = Path(directory)/'request.json', Path(directory)/'result.json'
        request.write_text(json.dumps({'plan':plan, 'apply':apply}))
        command = [sys.executable, str(Path(__file__).resolve()), '--request', str(request), '--result', str(result)]
        if foot:
            launcher = [foot, '--fullscreen', '--font=monospace:size=20',
                        '--title=Destiny Wallpapers setup', '--app-id=destiny-wallpapers-setup']
        else:
            launcher = [terminal, '--title=Destiny Wallpapers setup', '--app-id=destiny-wallpapers-setup']
        subprocess.run([*launcher, *command], check=False)
        if not result.is_file():
            return None
        value = json.loads(result.read_text())
        return value if value in {'auto',*(o['profile'] for o in plan['options'])} else None


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
