import io
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools'))
import wallpaper_setup_cli as cli

PLAN = dict(recommended='small', biggest='big', reason='Smallest set that fits both screens.',
            options=[dict(profile='small',size=[1920,1080],total_bytes=80_000_000,displays=[]),
                     dict(profile='big',size=[3840,2160],total_bytes=280_000_000,displays=[])])


class CLI(unittest.TestCase):
    def test_exactly_two_choices(self):
        self.assertEqual(cli.choices(PLAN), [('Smallest suitable set','80.0 MB','auto'),
            ("Highest resolution",'280.0 MB','biggest')])

    def test_tui_navigation_and_cancel(self):
        class Screen:
            def __init__(self, keys, size=(33,110)):
                self.keys=iter(keys); self.size=size; self.lines=[]
            def getmaxyx(self):return self.size
            def erase(self):self.lines=[]
            def addstr(self,y,x,text,style):
                assert 0<=y<self.size[0] and x+len(text)<self.size[1]
                self.lines.append(text)
            def refresh(self):pass
            def keypad(self,value):pass
            def get_wch(self):return next(self.keys)
        with patch.object(cli.curses,'curs_set'),patch.object(cli.curses,'has_colors',return_value=False):
            screen=Screen([cli.curses.KEY_DOWN,'\n'])
            self.assertEqual(cli.tui(screen,PLAN,True),'biggest')
            self.assertTrue(any('Smallest suitable set' in text for text in screen.lines))
            self.assertTrue(any('SELECTED FORMAT' in text for text in screen.lines))
            self.assertIsNone(cli.tui(Screen(['\x1b']),PLAN,True))
            self.assertEqual(cli.tui(Screen(['\n'],(10,35)),PLAN,False),'auto')

    def test_crop_geometry_matches_cover_area(self):
        for size, display, axis in [([5120,2160],dict(width=1920,height=1080),'sides'),
                                    ([1920,1080],dict(width=3440,height=1440),'vertical'),
                                    ([3840,2160],dict(width=1920,height=1080),'none')]:
            x,y,w,h=cli.crop_geometry(size,display)
            self.assertAlmostEqual(2*x+w,1)
            self.assertAlmostEqual(2*y+h,1)
            if axis=='sides':
                self.assertAlmostEqual(1-w*h,.25)
                self.assertEqual(y,0)
            elif axis=='vertical':
                self.assertGreater(y,0)
                self.assertEqual(x,0)
            else:self.assertEqual((x,y,w,h),(0,0,1,1))

    def test_plain_default_and_cancel(self):
        with patch.object(cli.shutil,'which',return_value=None),patch('sys.stdout',new_callable=io.StringIO):
            with patch('builtins.input',return_value=''):
                self.assertEqual(cli.prompt(PLAN,False),'auto')
            with patch('builtins.input',return_value='q'):
                self.assertIsNone(cli.prompt(PLAN,False))

    def test_desktop_terminal_passes_choice_back(self):
        def terminal(args, **kwargs):
            result=Path(args[args.index('--result')+1])
            request=json.loads(Path(args[args.index('--request')+1]).read_text())
            self.assertEqual(request['plan'],PLAN)
            result.write_text('"biggest"')
            return subprocess.CompletedProcess(args,0)
        with patch('sys.stdin.isatty',return_value=False),patch.dict(os.environ,{'WAYLAND_DISPLAY':'wayland-1'}), \
             patch.object(cli.shutil,'which',return_value='/usr/bin/xdg-terminal-exec'), \
             patch.object(cli.subprocess,'run',side_effect=terminal):
            self.assertEqual(cli.choose_profile(PLAN,True),'biggest')

    def test_terminal_closed_without_result_is_cancel(self):
        with patch('sys.stdin.isatty',return_value=False),patch.dict(os.environ,{'WAYLAND_DISPLAY':'wayland-1'}), \
             patch.object(cli.shutil,'which',return_value='/usr/bin/xdg-terminal-exec'), \
             patch.object(cli.subprocess,'run',return_value=subprocess.CompletedProcess([],1)):
            self.assertIsNone(cli.choose_profile(PLAN,True))


if __name__=='__main__':unittest.main()
