import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tools'))
import wallpaper_profiles as wp


class Profiles(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        docs = self.root/'docs/collection'
        docs.mkdir(parents=True)
        (docs/'catalog.json').write_text(json.dumps({'finalized': [{'id': 'one'}, {'id': 'two'}]}))
        self.manifest = {'default': 'wide', 'profiles': []}
        for name, size in [('wide', [5120, 2160]), ('16-9', [5120, 2880])]:
            entries = []
            (self.root/name).mkdir()
            for id in ['one', 'two']:
                path = self.root/name/f'{id}.webp'
                path.write_bytes(f'{name}-{id}'.encode())
                entries.append(dict(id=id, file=str(path.relative_to(self.root)), sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
            self.manifest['profiles'].append(dict(id=name, label=name, files=entries, size=size, min_text_px=14))
        self.save()

    def save(self):
        (self.root/'docs/collection/profiles.json').write_text(json.dumps(self.manifest))

    def screen(self, w=1920, h=1080):
        return dict(name='DP-1', width=w, height=h, scale=1, focused=True)

    def plan(self, **kwargs):
        return wp.plan(self.root, detected=[self.screen()], **kwargs)

    def test_selection_and_honest_readability(self):
        p = self.plan()
        self.assertEqual(p['profile'], '16-9')
        self.assertIn('5.2 logical pixels', p['warnings'][0])
        self.assertEqual(wp.plan(self.root, detected=[self.screen(5120, 2160)])['profile'], 'wide')
        self.assertEqual(self.plan(requested='wide')['profile'], 'wide')
        self.assertEqual(wp.plan(self.root, detected=[])['profile'], 'wide')

    def test_normalize_rotation_scaling_invalid(self):
        rows = [dict(name='portrait', width=2560, height=1440, scale=1.5, transform=1),
                dict(name='off', width=1920, height=1080, disabled=True), {}, None,
                dict(name='FALLBACK', width=1920, height=1080),
                dict(name='bad', width=1920, height=1080, scale=float('nan'))]
        self.assertEqual(wp.normalize_monitors(rows), [dict(name='portrait', width=1440, height=2560, scale=1.5, focused=False)])

    def test_all_monitors_and_manual(self):
        a, b = self.screen(), {**self.screen(5120,2160), 'name':'DP-2', 'focused':False}
        self.assertEqual(wp.plan(self.root, detected=[b,a])['profile'], 'wide')
        self.assertEqual(wp.plan(self.root, detected=[a,b], monitor='DP-2')['profile'], 'wide')
        with self.assertRaisesRegex(ValueError, 'not connected'):
            self.plan(monitor='missing')

    def test_focus_and_order_do_not_change_recommendation(self):
        a, b = self.screen(), {**self.screen(5120,2160), 'name':'DP-2', 'focused':False}
        p = wp.plan(self.root, detected=[a,b])
        a['focused'], b['focused'] = False, True
        self.assertEqual(wp.plan(self.root, detected=[b,a])['recommended'], p['recommended'])

    def test_largest_monitor_prevents_low_resolution_choice(self):
        low = {**self.manifest['profiles'][1], 'id':'1080-test', 'size':[1920,1080]}
        self.manifest['profiles'].append(low)
        self.save()
        screens = [self.screen(), {**self.screen(3840,2160), 'name':'DP-2'}]
        p = wp.plan(self.root, detected=screens)
        self.assertEqual(p['recommended'], '16-9')
        low_result = next(x for x in p['options'] if x['profile']=='1080-test')
        self.assertTrue(low_result['upscale'])
        self.assertEqual(low_result['displays'][1]['factor'], 2)
        self.assertFalse(p['options'][0]['upscale'])

    def test_more_than_two_screens_and_portrait_crop(self):
        screens = [self.screen(), {**self.screen(3840,2160), 'name':'DP-2'},
                   {**self.screen(1080,1920), 'name':'DP-3'},
                   {**self.screen(3440,1440), 'name':'DP-4'}]
        p = wp.plan(self.root, detected=screens)
        self.assertTrue(all(len(o['displays'])==4 for o in p['options']))
        self.assertGreater(p['options'][0]['displays'][2]['crop'], .5)

    def test_when_all_are_too_small_choose_least_enlargement(self):
        p = wp.plan(self.root, detected=[self.screen(7680,4320)])
        self.assertTrue(all(o['upscale'] for o in p['options']))
        self.assertEqual(p['recommended'], '16-9')
        self.assertEqual(p['options'][0]['displays'][0]['factor'], 1.5)

    def test_dialog_choice_changes_actual_files_and_saved_preference(self):
        with patch.object(wp, 'read_setup', return_value={}), patch.object(wp, 'announce', return_value='wide'), \
             patch.object(wp, 'sync') as sync, patch.object(wp, 'save_setup') as save:
            result = wp.initialize(self.root, self.plan())
            self.assertEqual(result['profile'], 'wide')
            self.assertIn('/wide/', result['files'][0])
            self.assertEqual(sync.call_args.args[0]['profile'], 'wide')
            self.assertEqual(save.call_args.args[0]['profile'], 'wide')

    def test_incomplete_profile_not_mixed_and_escape_rejected(self):
        (self.root/'16-9/one.webp').unlink()
        self.assertEqual(self.plan()['profile'], 'wide')
        with self.assertRaisesRegex(ValueError, 'Unavailable'):
            self.plan(requested='16-9')
        self.manifest['profiles'][0]['files'][0]['file'] = '../outside.webp'
        self.save()
        with self.assertRaisesRegex(ValueError, 'outside'):
            self.plan()

    def stage(self):
        current = self.root/'current'
        dest = current/'theme/backgrounds'
        dest.mkdir(parents=True)
        (current/'theme.name').write_text('destiny\n')
        (dest/'one.webp').write_bytes(b'old')
        (dest/'custom.webp').write_bytes(b'keep')
        (current/'background').symlink_to(dest/'one.webp')
        return current, dest

    def test_sync_preserves_custom_and_selected_idempotently(self):
        current, dest = self.stage()
        with patch.object(wp.subprocess, 'run') as run:
            self.assertTrue(wp.sync(self.plan(), current))
            self.assertEqual(run.call_args.args[0][-1], str(dest/'one.webp'))
            self.assertFalse(wp.sync(self.plan(), current))
            self.assertEqual(run.call_count, 1)
        self.assertEqual((dest/'custom.webp').read_bytes(), b'keep')
        self.assertEqual((dest/'one.webp').read_bytes(), b'16-9-one')
        self.assertFalse((dest/'one.webp').is_symlink())

    def test_other_theme_and_no_monitor_are_untouched(self):
        current, dest = self.stage()
        self.assertFalse(wp.sync(wp.plan(self.root, detected=[]), current))
        (current/'theme.name').write_text('other')
        self.assertFalse(wp.sync(self.plan(), current))
        self.assertEqual((dest/'one.webp').read_bytes(), b'old')

    def test_hash_failure_before_any_replacement(self):
        current, dest = self.stage()
        p = self.plan()
        Path(p['files'][-1]).write_bytes(b'tampered')
        with self.assertRaisesRegex(ValueError, 'changed since packaging'):
            wp.sync(p, current)
        self.assertEqual((dest/'one.webp').read_bytes(), b'old')

    def test_symlink_stage_refused(self):
        current = self.root/'current'
        current.mkdir()
        (current/'theme.name').write_text('destiny')
        (current/'theme').symlink_to(self.root/'16-9', target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'regular staged'):
            wp.sync(self.plan(), current)

    def test_cancel_does_not_sync_or_save(self):
        with patch.object(wp, 'read_setup', return_value={}), patch.object(wp, 'announce', return_value=False), \
             patch.object(wp, 'sync') as sync, patch.object(wp, 'save_setup') as save:
            self.assertFalse(wp.initialize(self.root, self.plan()))
            sync.assert_not_called()
            save.assert_not_called()

    def test_setup_once_and_retry_when_detection_unavailable(self):
        with patch.object(wp, 'read_setup', return_value={'version':3, 'root':str(self.root)}), \
             patch.object(wp, 'announce') as announce, patch.object(wp, 'sync'), patch.object(wp, 'save_setup') as save:
            self.assertTrue(wp.initialize(self.root, self.plan()))
            announce.assert_not_called()
            save.assert_called_once()
        with patch.object(wp, 'read_setup', return_value={}), patch.object(wp, 'announce', return_value='16-9'), \
             patch.object(wp, 'sync'), patch.object(wp, 'save_setup') as save:
            wp.initialize(self.root, wp.plan(self.root, detected=[]))
            save.assert_not_called()


if __name__ == '__main__':
    unittest.main()
