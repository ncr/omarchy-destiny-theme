# Destiny Wallpapers — companion app

Optional fullscreen wallpaper browser with automatic monitor-format selection.
The theme installed through Omarchy's menu is data only: it cannot install or
launch this app by itself. Explicitly run the companion installer once:

```sh
omarchy pkg add imv gtk4 python-gobject          # only if missing
python3 companion/install.py
```

The installer announces what it installs, adds **Destiny Wallpapers** to the
application menu, and opens it automatically in a graphical session. Use
`--no-launch` to install without opening it. No sudo, permanent viewer autostart,
or compositor configuration changes are involved.

## First launch

The app reads all connected monitors from Hyprland, including rotation and
scale. It first avoids enlargement on **any** screen, then minimizes the worst
crop and the area-weighted crop. It never follows window focus. With matching
proportions, a high-resolution source is preferred over enlarging a low one.

A scrollable comparison lists every monitor under each available format:
green means native or reduced resolution, red warns about enlargement, and
amber separately warns about cropping. Every colour also has a written label.
The recommended option is preselected. **Apply and open** confirms it; Cancel
or Escape makes no changes. There is no countdown. Choosing the recommendation
keeps future selection automatic; another choice becomes a manual override.
Use `--configure` to reopen this comparison. Existing v2 installations see the
new comparison once. The theme hook only runs after completing this setup.

Both complete native formats (42 sheets each) ship on **main**:
5120×2880 (16:9) and 5120×2160 (ultrawide). No separate branch is needed.
These are independently composed masters, not upscales.
**Readable reflow for 1080p and 1440p is still pending.** Even green resolution
status does not guarantee readable labels on a small display; the comparison
reports estimated text size independently. A portrait monitor can still crop
most of a landscape sheet. If every source is too small, the least enlargement
is recommended and still shown in red.

Hyprland's synthetic FALLBACK output is not treated as a physical monitor.
Without monitor detection, the app can browse the default but leaves the
desktop unchanged and retries setup when detection works.

If Destiny is active, the app copies the chosen set into Omarchy's staged
backgrounds while preserving custom files and the currently selected sheet.
A user-local `theme-set` hook repeats this selection when Destiny is reapplied,
including after an update. The hook does nothing before first-run setup.
Other themes are never activated or modified. Opening the app checks the
monitors again; this is not a resident hotplug service.

Omarchy currently displays one shared wallpaper on all monitors. Selection
considers the whole monitor arrangement, not a separate profile per output. Other aspect
ratios may crop on the desktop; the viewer always fits the complete sheet.

## Controls and overrides

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
destiny-wallpapers --configure        # Reopen the coloured comparison
destiny-wallpapers --show-plan        # JSON; no changes or setup dialog
destiny-wallpapers --list             # All 42 chosen files; read-only
destiny-wallpapers --profile 16-9      # Remember a manual override
destiny-wallpapers --profile auto     # Resume automatic aspect selection
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
