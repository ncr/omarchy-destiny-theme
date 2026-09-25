# Destiny Wallpapers — companion app

Optional fullscreen wallpaper browser with automatic monitor-format selection.
The theme installed through Omarchy's menu is data only: it cannot install or
launch this app by itself. Explicitly run the companion installer once:

```sh
omarchy pkg add imv              # only if missing
python3 companion/install.py
```

The installer announces what it installs, adds **Destiny Wallpapers** to the
application menu, and opens it automatically in a graphical session. Use
`--no-launch` to install without opening it. No sudo, permanent viewer autostart,
or compositor configuration changes are involved.

## Automatic setup

Opening the app automatically selects the optimal wallpaper set and opens the
gallery. There is no first-run dialog. Selection considers all connected
monitors: avoid enlargement, minimize cropping, then prefer smaller files.

A short notification appears on the first selection or when the chosen set
changes. It states the resolution; clicking it opens settings. With another
theme active, it says “Gallery only” and leaves the desktop unchanged.
Unchanged launches do not repeat the notification.

Settings are available through **Wallpaper settings** in the application's
context menu, or `destiny-wallpapers --configure`. This optional TUI offers
**Automatic · Optimal set** and the installed resolutions. A manual override
is remembered; selecting Automatic restores monitor-based selection.
Escape cancels without changing anything. The settings window uses a large
font in Foot, without modifying terminal configuration.

`--show-plan` provides detailed read-only diagnostics. Earlier setup policies
migrate to automatic selection. No monitor detection means no desktop change;
the app retries automatically on the next launch.

Both native formats (42 sheets each) ship on **main**: 5120×2880 (16:9) and
5120×2160 (ultrawide). MB describes compressed image files, not RAM or download
savings; selecting a set does not delete the other bundled format.
**Readable reflow for 1080p and 1440p is still pending.** Resolution and small
text legibility are different things; detailed estimates remain in `--show-plan`.

Hyprland's synthetic FALLBACK output is not treated as a physical monitor.
Without monitor detection, the app can browse the default but leaves the
desktop unchanged and retries setup when detection works.

If Destiny is active, the app copies the chosen set into Omarchy's staged
backgrounds while preserving custom files and the currently selected sheet.
A user-local `theme-set` hook repeats this selection when Destiny is reapplied,
including after an update. The hook does nothing before the app has initialized.
Other themes are never activated or modified. Opening the app checks the
monitors again; this is not a resident hotplug service.

Omarchy currently displays one shared wallpaper on all monitors. Selection
considers the whole monitor arrangement, not a separate profile per output. Other aspect
ratios may crop on the desktop; the viewer always fits the complete sheet.

## Controls

| Key | Action |
|---|---|
| Left / Right | Previous / next, wrapping |
| Esc / Q | Close |
| F | Toggle fullscreen |
| I | Show filename and position |
| Home / End | First / last |

The local Super+O integration recognizes the unchanged `destiny-wallpapers`
window class. This app does not install a global keybinding.

```sh
destiny-wallpapers truth-lamp
destiny-wallpapers 3                  # Collection position, not filename number
destiny-wallpapers --configure        # Change resolution settings
destiny-wallpapers --show-plan        # JSON; no changes or setup dialog
destiny-wallpapers --list             # All 42 chosen files; read-only
destiny-wallpapers --monitor DP-1     # Prefer its proportions; still avoid upscaling on all screens
destiny-wallpapers --dir /path/to/numbered-images
python3 companion/install.py --uninstall
```

Installation is user-local: `~/.local/bin/destiny-wallpapers`,
`~/.local/share/destiny-wallpapers/`, the application-menu entry and
`~/.config/omarchy/hooks/theme-set.d/destiny-wallpapers`. Setup preferences
live under `$XDG_STATE_HOME/destiny-wallpapers/setup.json` (default
`~/.local/state/`). Omarchy's own staged files follow its fixed state path.

Keep the checkout in place: wallpaper assets are read from it. Rerun the
installer after moving it or updating app code. New production masters must
be packaged with `tools/package_wallpaper_profiles.py` to refresh verified
hashes. Development viewers `./wallpapers` and `./century` continue to read
live renders independently of the packaged release.

Uninstall removes the launcher, owned hook and runtime files. It retains the
theme, wallpaper files and setup preferences. A custom `--prefix /some/path`
is a staging installation: it neither installs hooks nor launches the app.
