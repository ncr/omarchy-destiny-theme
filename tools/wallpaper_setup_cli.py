"""Explain the automatically selected wallpaper set in a terminal UI."""
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


def optimal_set(plan):
    return next(o for o in plan['options'] if o['profile']==plan['recommended'])


def size_label(option):
    value=option.get('total_bytes')
    return f'{value/1_000_000:.1f} MB' if value is not None else 'Size unknown'


def crop_geometry(size, display):
    """Centred cover viewport, as fractions of the original wallpaper."""
    w, h = size
    factor = max(display['width']/w, display['height']/h)
    visible_w = min(1., display['width']/(w*factor))
    visible_h = min(1., display['height']/(h*factor))
    return (1-visible_w)/2, (1-visible_h)/2, visible_w, visible_h


def draw_menu(screen, plan, apply, colors, page=0, alternative=0):
    height, width = screen.getmaxyx()
    screen.erase()
    bold = curses.A_BOLD
    normal, muted, accent, highlight, good, warning = colors
    def put(y, x, text, style=normal):
        if 0 <= y < height-1 and 0 <= x < width-1:
            try:
                screen.addstr(y, x, text[:width-x-1], style)
            except curses.error:
                pass
    chosen = optimal_set(plan)
    detail=' × '.join(map(str,chosen.get('size',[])))+'  /  '+size_label(chosen)
    action = 'Update Destiny desktop + open gallery' if apply else 'Open gallery; desktop stays unchanged'
    if height < 28 or width < 90:
        put(0, 1, 'DESTINY WALLPAPERS', bold|accent)
        put(2,1,'Optimal set',bold|accent)
        y=3
        for text in (detail,action,'Why: '+plan['reason']):
            for line in textwrap.wrap(text,max(8,width-3)):
                if y>=height-3: break
                put(y,1,line);y+=1
            y+=1
        put(height-3,1,'Enlarge terminal for the crop diagrams.',accent)
        put(height-2,1,'ENTER Continue · ESC Cancel',bold)
        return
    panel = min(108, width-6)
    left = (width-panel)//2
    put(0,left,'DESTINY / WALLPAPERS',bold|accent)
    put(2,left,'Optimal set',bold|accent)
    put(2,left+panel-len(detail)-1,detail,bold)
    count=plan.get('count',chosen.get('file_count',0))
    put(3,left,f'{count} wallpapers · '+action)
    put(5,left,'Priority: avoid enlargement → minimize cropping → save disk space',bold)
    for i,line in enumerate(textwrap.wrap(plan['reason'],panel)[:2]):
        put(7+i,left,line)
    others = [o for o in plan['options'] if o['profile']!=chosen['profile']]
    columns = [chosen]+([others[alternative % len(others)]] if others else [])
    col_width = panel//len(columns)
    for i,o in enumerate(columns):
        label=' × '.join(map(str,o.get('size',[])))
        mb=f"{o['total_bytes']/1_000_000:.1f} MB" if o.get('total_bytes') is not None else 'Size unknown'
        put(10,left+i*col_width,label+' / '+mb,bold)
        put(11,left+i*col_width,'OPTIMAL SET' if i==0 else 'ALTERNATIVE / FOR COMPARISON',accent)
    screens=chosen.get('displays',[])
    per_page=max(1,(height-17)//7)
    pages=max(1,(len(screens)+per_page-1)//per_page)
    page=page%pages
    for row,display in enumerate(screens[page*per_page:(page+1)*per_page]):
        y=13+row*7
        put(y,left,f"{display['name']}  {display['width']} × {display['height']}",bold)
        for col,o in enumerate(columns):
            d=next(r for r in o['displays'] if r['name']==display['name'])
            x=left+col*col_width
            # Character cells are approximately twice as tall as they are wide.
            # Same graphic height and proportional width preserve source aspect.
            gh=4
            gw=max(3,min(22,round(gh*2*o['size'][0]/o['size'][1])))
            cx,cy,vw,vh=crop_geometry(o['size'],d)
            for gy in range(gh):
                for gx in range(gw):
                    kept=cx <= (gx+.5)/gw <= cx+vw and cy <= (gy+.5)/gh <= cy+vh
                    put(y+1+gy,x+gx,'█' if kept else '▒',good if kept else warning)
            tx=x+gw+2
            crop=d['crop']
            put(y+1,tx,'Full image' if crop<.000001 else f'{crop:.0%} cropped',bold|(good if crop<.000001 else warning))
            put(y+2,tx,'No enlargement' if not d['upscale'] else f"Enlarged {d['factor']:.2f}×",warning if d['upscale'] else normal)
            if crop>.000001:
                put(y+3,tx,'Sides removed' if cx>cy else 'Top/bottom removed',warning)
    if not screens:
        put(14,left,'No monitors detected; desktop stays unchanged.',warning)
    put(height-4,left,'█ Visible image',good)
    put(height-4,left+20,'▒ Cropped away',warning)
    put(height-4,left+40,'One wallpaper shared by all screens',muted)
    controls='ENTER '+('Apply optimal set & open' if apply else 'Open gallery')+'   ESC Cancel'
    if pages>1: controls+=f'   PgUp/Dn Screens {page+1}/{pages}'
    if len(others)>1: controls+='   [ ] Formats'
    put(height-2,left,controls,bold|accent)


def tui(screen, plan, apply):
    try:
        curses.curs_set(0)
    except curses.error:
        pass
    screen.keypad(True)
    colors = (0,0,0,curses.A_REVERSE,0,curses.A_BOLD)
    if curses.has_colors():
        curses.use_default_colors()
        # Standard colour pairs also work over SSH and in 16-colour terminals.
        curses.init_pair(1,curses.COLOR_WHITE,-1)
        curses.init_pair(2,curses.COLOR_WHITE,-1)
        curses.init_pair(3,curses.COLOR_CYAN,-1)
        curses.init_pair(4,curses.COLOR_WHITE,curses.COLOR_BLUE)
        curses.init_pair(5,curses.COLOR_GREEN,-1)
        curses.init_pair(6,curses.COLOR_YELLOW,-1)
        colors = tuple(curses.color_pair(i) for i in range(1,7))
    page = alternative = 0
    while True:
        draw_menu(screen,plan,apply,colors,page,alternative)
        screen.refresh()
        key = screen.get_wch()
        if key in (curses.KEY_NPAGE,curses.KEY_PPAGE):
            page += 1 if key==curses.KEY_NPAGE else -1
        elif key in ('[',']'):
            alternative += 1 if key==']' else -1
        elif key in ('\n','\r',curses.KEY_ENTER):
            return 'auto'
        elif key in ('\x1b','q','Q'):
            return None
        # KEY_RESIZE redraws using the new dimensions on the next iteration.


def prompt(plan, apply):
    if sys.stdin.isatty() and sys.stdout.isatty() and os.environ.get('TERM') != 'dumb':
        try:
            return curses.wrapper(tui, plan, apply)
        except KeyboardInterrupt:
            return None
    option=optimal_set(plan)
    print('DESTINY WALLPAPERS / Optimal set')
    print(' × '.join(map(str,option.get('size',[])))+' / '+size_label(option))
    print('Why: '+plan['reason'])
    print('Update Destiny desktop + open gallery' if apply else 'Open gallery; desktop stays unchanged')
    try:
        while True:
            answer=input('Enter to continue, q to cancel: ').strip().lower()
            if answer in ('','q'):
                return None if answer=='q' else 'auto'
    except (KeyboardInterrupt,EOFError):
        return None


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
        return 'auto' if value=='auto' else None


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
