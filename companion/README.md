# Destiny Wallpapers — companion app

A small optional desktop app for browsing the theme's engineering sheets.
It uses Python's standard library and imv; rendering tools and Blender are
not required to browse existing images. Theme installation alone does not
execute the companion installer.

From the theme checkout:

```sh
omarchy pkg add imv                   # only if missing
python3 companion/install.py
destiny-wallpapers
```

It appears as **Destiny Wallpapers** in the application menu. Installation is
user-local: `~/.local/bin/destiny-wallpapers`, `~/.local/share/destiny-wallpapers/`
and a `.desktop` entry. No sudo or compositor configuration changes.
If `~/.local/bin` is not on PATH, use the application menu or the full path.

The app reads `docs/collection/catalog.json` in this checkout. In the current
development checkout that is all 34 retained wallpapers, in collection order.
A fresh clone without development renders shows the 14 shipped backgrounds.
Rejected concepts are excluded. Generated HTML galleries and symlinks are not
required. The actual title bar always shows the available image count.

Wallpaper files stay in the checkout. New renders are available immediately;
imv reloads the displayed file when it changes. Keep the checkout in place,
or rerun the installer after moving it. After updating app code, rerun the
same installer. Reinstalling is safe and does not duplicate the menu entry.

| Key | Action |
|---|---|
| Left / Right | Previous / next, wrapping at the ends |
| Esc / Q | Close |
| F | Toggle fullscreen |
| I | Show filename and position |
| Home / End | First / last |

The existing local Super+O integration continues to recognize the unchanged
`destiny-wallpapers` window class. It is a local Hyprland customization, not a
global keybinding installed by this companion.

```sh
destiny-wallpapers truth-lamp        # Start by name
destiny-wallpapers 3                 # Third available sheet in collection order
destiny-wallpapers --list
destiny-wallpapers --dir /path/to/numbered-images
python3 companion/install.py --uninstall
```

Uninstalling removes the app launcher and its runtime files, preserving the
theme and wallpapers. `--prefix /some/path` is available for staging installs.
The development commands `./wallpapers` and `./century` remain available;
`./finalized` and `./destiny-wallpapers` open the companion's full collection.
