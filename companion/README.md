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

## First launch: two choices in a full-screen TUI

Setup uses a full-screen TUI with bold choices and a strong selection highlight.
It runs in your current terminal. From the application menu, it opens Foot
full-screen with a large 20-point font, falling back to the default terminal.
This font setting applies only to the setup window; no terminal config changes.

- **Perfectly good** — the smallest suitable set for all connected monitors.
- **I don't care, I want the biggest everything** — the highest resolution
  available in the matching aspect ratio.

Each choice shows its total MB. One short reason explains the recommendation,
including why a smaller file loses if it would crop content or require
upscaling. If both policies currently resolve to the same set, setup says so.
Arrow keys choose; Enter applies; Escape cancels. Python's standard curses
module renders the TUI; a numbered prompt supports non-interactive terminals.
The selected policy is remembered, so new exports
and monitor changes can be handled without asking for a resolution again.
`--configure` reopens setup; `--show-plan` provides the full read-only details.
Existing graphical-setup installations see the terminal choice once.

Automatic selection considers every monitor, not window focus. It avoids
upscaling first, minimizes cropping, then chooses the smallest file total.
The biggest policy selects the highest pixel count in that same aspect ratio;
it does not switch to the wrong proportions just to use a larger file.

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
destiny-wallpapers --configure        # Reopen the two-choice terminal setup
destiny-wallpapers --show-plan        # JSON; no changes or setup dialog
destiny-wallpapers --list             # All 42 chosen files; read-only
destiny-wallpapers --profile biggest   # Prefer highest matching resolution
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
