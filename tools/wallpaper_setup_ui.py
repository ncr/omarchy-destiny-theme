"""Native, scrollable display comparison; colour always has a text equivalent."""
from html import escape
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib, Gdk

GREEN = '#80d6a0'
RED = '#ff9393'
AMBER = '#f1c477'


def label(text, markup=False):
    widget = Gtk.Label(xalign=0, wrap=True)
    widget.set_max_width_chars(90)
    if markup:
        widget.set_markup(text)
    else:
        widget.set_text(text)
    return widget


class SetupWindow(Gtk.Window):
    def __init__(self, plan, apply, finished, demo=None):
        super().__init__(title='Destiny Wallpapers — display setup')
        self.set_default_size(820, 690)
        self.finished = finished
        self.choice = None
        self.buttons = {}
        self.connect('close-request', self.cancel)
        keys = Gtk.EventControllerKey()
        keys.connect('key-pressed', self.key_pressed)
        self.add_controller(keys)
        outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        for edge in ('top', 'bottom', 'start', 'end'):
            getattr(outer, 'set_margin_'+edge)(24)
        self.set_child(outer)
        outer.append(label('<span size="x-large" weight="bold">Which wallpaper format should we use?</span>', True))
        if demo:
            outer.append(label(f'<span foreground="{AMBER}" weight="bold">TEST — {escape(demo)}</span>', True))
        outer.append(label('We recommend the smallest set that avoids enlargement on every monitor and fits their proportions best. Extra resolution is optional.'))
        scroll = Gtk.ScrolledWindow(vexpand=True, hexpand=True)
        self.scroller = scroll
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        outer.append(scroll)
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        scroll.set_child(content)
        screens = '\n'.join(f"{m['name']}   {m['width']} × {m['height']}   ·   scale {m['scale']:g}" for m in plan['monitors'])
        content.append(label('<b>Connected monitors</b>\n'+escape(screens or 'Not detected — desktop unchanged'), True))
        if len(plan['monitors']) > 1:
            content.append(label('Omarchy uses one shared wallpaper. The comparison below shows its effect on every screen.'))
        group = None
        for option in plan['options']:
            recommended = option['profile'] == plan['recommended']
            frame = Gtk.Frame()
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
            for edge in ('top', 'bottom', 'start', 'end'):
                getattr(box, 'set_margin_'+edge)(14)
            frame.set_child(box)
            content.append(frame)
            button = Gtk.CheckButton(label=f"{option['label']}  —  {option['size'][0]} × {option['size'][1]}" + ('   ·   RECOMMENDED' if recommended else ''))
            if group:
                button.set_group(group)
            else:
                group = button
            button.connect('toggled', self.selected, option['profile'])
            self.buttons[option['profile']] = button
            box.append(button)
            if option['total_bytes'] is not None:
                box.append(label(f"{option['file_count']} wallpapers · {option['total_bytes']/1_000_000:.1f} MB total · {option['average_bytes']/1_000_000:.2f} MB per wallpaper on average"))
            else:
                box.append(label('File size unavailable — no image files supplied for this test option.'))
            if not option['displays']:
                box.append(label('Quality cannot be assessed without a detected screen.'))
            for row in option['displays']:
                color = RED if row['upscale'] else GREEN
                status = f"ENLARGED {row['factor']:.2f}× — lower sharpness" if row['upscale'] else (
                    'NATIVE — no enlargement' if abs(row['factor']-1) < .000001 else f"REDUCED to {row['factor']*100:.0f}% — no enlargement")
                text = f"<b>{escape(row['name'])}</b>   <span foreground='{color}'>{status}</span>"
                if row['crop'] > .01:
                    text += f"\n<span foreground='{AMBER}'>Different proportions: about {row['crop']*100:.0f}% of the image area is cropped on this desktop.</span>"
                else:
                    text += '\nMatching proportions — the complete sheet fits.'
                if row['text_px'] < 12:
                    text += f"\nSmallest labels in the full-sheet viewer: ~{row['text_px']:.1f} px. Larger-type layouts are still pending."
                box.append(label(text, True))
        self.buttons[plan['profile']].set_active(True)
        content.append(label('Sizes describe the image files (1 MB = 1,000,000 bytes), not memory use. All published formats are currently bundled; choosing one does not remove the others.'))
        outer.append(label('Apply this format to the active Destiny desktop and open the viewer. Keep the current sheet and custom wallpapers.' if apply else
                           'Open the viewer with this format. Your desktop theme stays unchanged.'))
        controls = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12, halign=Gtk.Align.END)
        cancel = Gtk.Button(label='Cancel')
        cancel.connect('clicked', lambda *_: self.cancel())
        self.apply_button = Gtk.Button(label='Apply and open' if apply else 'Open viewer')
        self.apply_button.add_css_class('suggested-action')
        self.apply_button.connect('clicked', self.accept)
        controls.append(cancel)
        controls.append(self.apply_button)
        outer.append(controls)

    def selected(self, button, value):
        if button.get_active():
            self.choice = value

    def key_pressed(self, controller, keyval, keycode, state):
        if keyval == Gdk.KEY_Escape:
            self.cancel()
            return True
        return False

    def cancel(self, *_):
        self.finished(None)
        self.destroy()
        return True

    def accept(self, *_):
        self.finished(self.choice)
        self.destroy()


def choose_profile(plan, apply):
    Gtk.init()
    loop = GLib.MainLoop()
    result = [None]
    def finished(choice):
        result[0] = choice
        loop.quit()
    window = SetupWindow(plan, apply, finished)
    window.present()
    loop.run()
    return result[0]
