"""Keep the active Destiny desktop matched to connected monitors."""
import argparse
from pathlib import Path
import sys
import time
import wallpaper_profiles as wp


def stamp(path):
    try:
        s=path.stat()
        return (s.st_ino,s.st_mtime_ns,s.st_size)
    except OSError:
        return None


def fingerprint(root,screens):
    # Focus, window moves and wallpaper cycling do not require recopying assets.
    topology=sorted((m['name'],m['width'],m['height'],m['scale']) for m in screens)
    current=wp.current_dir()
    return (topology,stamp(current/'theme.name'),stamp(current/'theme'),
            stamp(root/'docs/collection/profiles.json'),stamp(wp.setup_path()))


class DesktopWatcher:
    def __init__(self,root):
        self.root=root
        self.last=None

    def tick(self):
        screens=wp.monitors()
        if not screens or not wp.active_destiny(wp.current_dir()):
            self.last=None
            return False
        signature=fingerprint(self.root,screens)
        if signature==self.last:
            return False
        previous=wp.read_setup()
        requested=previous.get('profile','auto') if previous.get('version')==6 and previous.get('root')==str(self.root) else 'auto'
        monitor=previous.get('monitor')
        if monitor not in {m['name'] for m in screens}:monitor=None
        _,available=wp.profiles(self.root)
        if requested not in {'auto',*(p['id'] for p in available)}:requested='auto'
        p=wp.plan(self.root,requested,monitor,screens)
        wp.initialize(self.root,p,requested,monitor)
        # Synchronization itself touches the stage and preferences.
        self.last=fingerprint(self.root,screens)
        return True


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,required=True)
    args=parser.parse_args()
    watcher=DesktopWatcher(args.root.resolve())
    last_error=None
    while True:
        try:
            watcher.tick()
            last_error=None
        except (OSError,ValueError,wp.subprocess.SubprocessError) as exc:
            if str(exc)!=last_error:
                print(f'Destiny desktop: {exc}',file=sys.stderr,flush=True)
                last_error=str(exc)
        time.sleep(10)


if __name__=='__main__':main()
