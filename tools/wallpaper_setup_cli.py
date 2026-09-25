"""Two choices in the user's terminal; no graphical setup toolkit."""
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
import textwrap


def choices(plan):
    by_id = {o['profile']: o for o in plan['options']}
    def size(id):
        value = by_id[id]['total_bytes']
        return f'{value/1_000_000:.1f} MB' if value is not None else 'Size unknown'
    return [('Perfectly good', size(plan['recommended']), 'auto'),
            ("I don't care, I want the biggest everything", size(plan['biggest']), 'biggest')]


def draw_menu(screen, plan, apply, selected, colors):
    height, width = screen.getmaxyx()
    screen.erase()
    bold = curses.A_BOLD
    normal, muted, accent, highlight = colors
    def put(y, x, text, style=normal):
        if 0 <= y < height and 0 <= x < width-1:
            try:
                screen.addstr(y, x, text[:width-x-1], style)
            except curses.error:
                pass
    items = choices(plan)
    if height < 22 or width < 64:
        # Keep the chooser usable even in a split pane or resized SSH terminal.
        put(0, 1, 'DESTINY WALLPAPERS', bold|accent)
        y = 2
        for i, (title, size, _) in enumerate(items):
            style = bold | (highlight if i == selected else normal)
            for line in textwrap.wrap(('> ' if i == selected else '  ')+title+'  '+size, max(8,width-3)):
                put(y, 1, line, style); y += 1
            y += 1
        for line in textwrap.wrap('Why: '+plan['reason'], max(8,width-3)):
            if y >= height-2: break
            put(y, 1, line, muted); y += 1
        put(height-1, 1, '↑↓ / 1,2 choose · Enter select · Esc cancel', bold)
        return
    panel = min(86, width-8)
    left = (width-panel)//2
    top = max(1, (height-22)//2)
    put(top, left, 'D E S T I N Y   /   W A L L P A P E R S', bold|accent)
    y = top+3
    for i,(title,size,_) in enumerate(items):
        active = i==selected
        style = (highlight if active else normal)|bold
        edge = (accent if active else muted)|bold
        put(y,left,'┏'+'━'*(panel-2)+'┓' if active else '┌'+'─'*(panel-2)+'┐',edge)
        for row in range(1,4):
            put(y+row,left,'┃' if active else '│',edge)
            put(y+row,left+1,' '*(panel-2),highlight if active else normal)
            put(y+row,left+panel-1,'┃' if active else '│',edge)
        text = ('▶  ' if active else '   ')+title
        if len(text)+len(size)+6 <= panel:
            put(y+2,left+3,text,style)
            put(y+2,left+panel-len(size)-3,size,style)
        else:
            put(y+1,left+3,text,style)
            put(y+3,left+6,size,style)
        put(y+4,left,'┗'+'━'*(panel-2)+'┛' if active else '└'+'─'*(panel-2)+'┘',edge)
        y += 6
    for line in textwrap.wrap('Why: '+plan['reason'],panel):
        put(y,left,line,normal);y+=1
    if plan['recommended']==plan['biggest']:
        put(y+1,left,'Both choices currently use the same files.',muted)
    action = 'Apply & open' if apply else 'Open gallery'
    put(min(height-2,top+22),left,'↑ ↓  Choose      ENTER  '+action+'      ESC  Cancel',bold|accent)


def tui(screen, plan, apply):
    try:
        curses.curs_set(0)
    except curses.error:
        pass
    screen.keypad(True)
    colors = (0,0,0,curses.A_REVERSE)
    if curses.has_colors():
        curses.use_default_colors()
        # Standard colour pairs also work over SSH and in 16-colour terminals.
        curses.init_pair(1,curses.COLOR_WHITE,-1)
        curses.init_pair(2,curses.COLOR_WHITE,-1)
        curses.init_pair(3,curses.COLOR_CYAN,-1)
        curses.init_pair(4,curses.COLOR_WHITE,curses.COLOR_BLUE)
        colors = tuple(curses.color_pair(i) for i in range(1,5))
    selected = 0
    while True:
        draw_menu(screen,plan,apply,selected,colors)
        screen.refresh()
        key = screen.get_wch()
        if key in (curses.KEY_UP,curses.KEY_DOWN,curses.KEY_LEFT,curses.KEY_RIGHT,'j','k','\t'):
            selected = 1-selected
        elif key in ('1','2'):
            selected = int(key)-1
        elif key in ('\n','\r',curses.KEY_ENTER):
            return ('auto','biggest')[selected]
        elif key in ('\x1b','q','Q'):
            return None
        # KEY_RESIZE redraws using the new dimensions on the next iteration.


def prompt(plan, apply):
    if sys.stdin.isatty() and sys.stdout.isatty() and os.environ.get('TERM') != 'dumb':
        try:
            return curses.wrapper(tui, plan, apply)
        except KeyboardInterrupt:
            return None
    print('DESTINY WALLPAPERS\n')
    for i,(title,size,_) in enumerate(choices(plan),1):
        print(f'{i}. {title} — {size}')
    print('\nWhy: '+plan['reason'])
    try:
        answer = input('Choose [1/2, Enter=1, q=cancel]: ').strip().lower()
        while answer not in ('','1','2','q'):
            answer = input('Choose 1, 2 or q: ').strip().lower()
        return None if answer=='q' else ('biggest' if answer=='2' else 'auto')
    except (KeyboardInterrupt,EOFError):
        return None


def choose_profile(plan, apply):
    if sys.stdin.isatty() and sys.stdout.isatty():
        return prompt(plan, apply)
    foot = shutil.which('foot')
    terminal = shutil.which('xdg-terminal-exec')
    if not (foot or terminal) or not (os.environ.get('WAYLAND_DISPLAY') or os.environ.get('DISPLAY')):
        raise ValueError('Run destiny-wallpapers --configure in a terminal to choose a wallpaper set.')
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
