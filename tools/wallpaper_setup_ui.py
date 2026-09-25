"""Native display setup with compact, keyboard-accessible format cards."""
from html import escape
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib, Gdk

GREEN = '#86dfb5'
RED = '#ff98a5'
AMBER = '#e9c584'
CSS = b'''
window.destiny-setup { background: #090d16; color: #d9e8ff; }
.destiny-setup headerbar { background: #090d16; box-shadow: none; border-bottom: 1px solid #202c40; }
.destiny-setup label { font-size: 14px; }
.destiny-setup .eyebrow { color: #94b4d8; font-size: 11px; font-weight: 700; letter-spacing: 2px; }
.destiny-setup .heading { color: #f1f5fc; font-size: 27px; font-weight: 700; }
.destiny-setup .muted { color: #a2b2ca; }
.destiny-setup .small { font-size: 12px; }
.destiny-setup .monitor { background: #121a28; border: 1px solid #243047; border-radius: 8px; padding: 10px 13px; }
.destiny-setup .card { background: #101725; border: 1px solid #2b3850; border-radius: 12px; padding: 18px; }
.destiny-setup .card:hover { border-color: #657d9f; }
.destiny-setup .card.selected { background: #142337; border: 1px solid #84b8e8; }
.destiny-setup .card checkbutton label { font-size: 18px; font-weight: 700; color: #f1f5fc; }
.destiny-setup .card checkbutton radio { color: #b4dcff; }
.destiny-setup .size { font-size: 29px; font-weight: 600; color: #f1f5fc; }
.destiny-setup .warning { color: #e9c584; font-size: 11px; font-weight: 700; letter-spacing: 1px; }
.destiny-setup .badge { color: #86dfb5; font-size: 11px; font-weight: 700; letter-spacing: 1px; }
.destiny-setup .divider { background: #2b3850; min-height: 1px; }
.destiny-setup .notice { background: #19202b; border-radius: 8px; padding: 12px 14px; }
.destiny-setup .demo { color: #e9c584; font-size: 12px; }
.destiny-setup button { border-radius: 8px; padding: 10px 18px; background: #182234; color: #d9e8ff; border: 1px solid #35435a; box-shadow: none; }
.destiny-setup button:hover { background: #24354e; }
.destiny-setup button.primary { background: #b4d6f5; color: #0b1728; border: 1px solid #b4d6f5; font-weight: 700; }
.destiny-setup button.primary:hover { background: #cee7ff; }
.destiny-setup button:focus-visible, .destiny-setup checkbutton:focus-visible { outline: 2px solid #b4d6f5; outline-offset: 3px; }
.destiny-setup scrollbar slider { background: #435770; min-width: 5px; }
'''


def label(text, markup=False, *classes):
    widget = Gtk.Label(xalign=0, wrap=True)
    widget.set_max_width_chars(80)
    if markup:
        widget.set_markup(text)
    else:
        widget.set_text(text)
    for name in classes:
        widget.add_css_class(name)
    return widget


def box(spacing=10, horizontal=False):
    return Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL if horizontal else Gtk.Orientation.VERTICAL, spacing=spacing)


def flow(maximum=2):
    widget = Gtk.FlowBox(selection_mode=Gtk.SelectionMode.NONE, homogeneous=True,
                         min_children_per_line=1, max_children_per_line=maximum,
                         column_spacing=14, row_spacing=14)
    return widget


class SetupWindow(Gtk.Window):
    def __init__(self, plan, apply, finished, demo=None):
        super().__init__(title='Destiny Wallpapers — display setup')
        self.add_css_class('destiny-setup')
        provider = Gtk.CssProvider()
        provider.load_from_data(CSS)
        Gtk.StyleContext.add_provider_for_display(self.get_display(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.provider = provider
        monitors = self.get_display().get_monitors()
        geometry = monitors.get_item(0).get_geometry() if monitors.get_n_items() else None
        width = min(960, max(560, geometry.width - 80)) if geometry else 960
        height = min(900, max(480, geometry.height - 80)) if geometry else 790
        self.set_default_size(width, height)
        self.set_resizable(False)
        self.set_modal(True)
        self.set_titlebar(Gtk.HeaderBar())
        self.finished, self.choice = finished, None
        self.buttons, self.cards, self.details = {}, {}, {}
        self.options = {o['profile']: o for o in plan['options']}
        self.connect('close-request', self.cancel)
        keys = Gtk.EventControllerKey()
        keys.connect('key-pressed', self.key_pressed)
        self.add_controller(keys)
        outer = box(18)
        for edge in ('top', 'bottom', 'start', 'end'):
            getattr(outer, 'set_margin_'+edge)(26)
        self.set_child(outer)
        heading = box(7)
        heading.append(label('◈  DESTINY  /  WALLPAPERS', False, 'eyebrow'))
        heading.append(label('Matched to your monitors', False, 'heading'))
        heading.append(label('The smallest set that stays sharp and fits your screens best.' if any(not o['upscale'] for o in plan['options']) else 'Every available set needs enlargement on at least one screen.', False, 'muted'))
        outer.append(heading)
        if demo:
            outer.append(label('TEST  ·  '+demo, False, 'demo'))
        scroll = Gtk.ScrolledWindow(vexpand=True, hexpand=True)
        self.scroller = scroll
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        outer.append(scroll)
        content = box(18)
        scroll.set_child(content)
        monitors = flow(3)
        for m in plan['monitors']:
            chip = box(10, True)
            chip.add_css_class('monitor')
            chip.append(Gtk.Image.new_from_icon_name('video-display-symbolic'))
            desc = box(3)
            desc.append(label(m['name']))
            desc.append(label(f"{m['width']} × {m['height']}  ·  {m['scale']:g}× scale", False, 'muted', 'small'))
            chip.append(desc)
            monitors.insert(chip, -1)
        if plan['monitors']:
            content.append(monitors)
        else:
            content.append(label('No display detected. You can browse wallpapers; your desktop will stay unchanged.', False, 'muted'))
        if len(plan['monitors']) > 1:
            content.append(label('One wallpaper across all screens. Each option is checked against every monitor.', False, 'muted', 'small'))
        cards = flow(2)
        content.append(cards)
        group = None
        small_text = False
        for option in plan['options']:
            card = box(9)
            card.add_css_class('card')
            card.set_size_request(300, -1)
            self.cards[option['profile']] = card
            recommended = option['profile'] == plan['recommended']
            card.append(label(('BEST AVAILABLE' if option['upscale'] else 'RECOMMENDED') if recommended else 'ALTERNATIVE', False,
                              ('warning' if option['upscale'] else 'badge') if recommended else 'eyebrow'))
            button = Gtk.CheckButton(label=option['label'])
            if group:
                button.set_group(group)
            else:
                group = button
            button.connect('toggled', self.selected, option['profile'])
            self.buttons[option['profile']] = button
            card.append(button)
            card.append(label(f"{option['size'][0]} × {option['size'][1]}", False, 'muted'))
            card.append(label(f"{option['total_bytes']/1_000_000:.1f} MB" if option['total_bytes'] is not None else 'Size unavailable', False, 'size'))
            if option['average_bytes'] is not None:
                card.append(label(f"{option['file_count']} wallpapers  ·  {option['average_bytes']/1_000_000:.2f} MB each on average", False, 'muted', 'small'))
            divider = Gtk.Separator()
            divider.add_css_class('divider')
            card.append(divider)
            for row in option['displays']:
                status = f"↑ Enlarged {row['factor']:.2f}×" if row['upscale'] else '✓ No enlargement'
                color = RED if row['upscale'] else GREEN
                card.append(label(f"<b>{escape(row['name'])}</b>   <span foreground='{color}'>{status}</span>", True))
                crop = f"{row['crop']*100:.0f}% cropped" if row['crop'] > .01 else 'Full sheet visible'
                color = AMBER if row['crop'] > .01 else '#a2b2ca'
                card.append(label(f"<span foreground='{color}'>{crop}</span>", True, 'small'))
                small_text = small_text or row['text_px'] < 12
            detail = Gtk.Expander(label='Display details')
            self.details[option['profile']] = detail
            detail_box = box(6)
            for row in option['displays']:
                text = label(f"{row['name']}: image scale {row['factor']:.2f}×; smallest labels in the full-sheet viewer ~{row['text_px']:.1f} px.", False, 'muted', 'small')
                text.set_max_width_chars(34)
                detail_box.append(text)
            if not option['displays']:
                detail_box.append(label('Connect a display to compare quality.', False, 'muted', 'small'))
            detail.set_child(detail_box)
            card.append(detail)
            cards.insert(card, -1)
        if small_text:
            note = box(4)
            note.add_css_class('notice')
            note.append(label('Fine print may still be small', False))
            note.append(label('Sharp images and readable text are different things. Larger-type layouts for smaller screens are still in development.', False, 'muted', 'small'))
            content.append(note)
        content.append(label('MB shows image-file size. All formats are bundled; this choice does not remove the others.', False, 'muted', 'small'))
        footer = box(12, True)
        summary = box(4)
        summary.set_hexpand(True)
        self.summary = label('')
        summary.append(self.summary)
        summary.append(label('Keep your current sheet and custom wallpapers.' if apply else 'Your desktop theme stays unchanged.', False, 'muted', 'small'))
        footer.append(summary)
        cancel = Gtk.Button(label='Cancel', valign=Gtk.Align.CENTER)
        cancel.connect('clicked', lambda *_: self.cancel())
        self.apply_button = Gtk.Button(label='Apply & open' if apply else 'Open gallery', valign=Gtk.Align.CENTER)
        self.apply_button.add_css_class('primary')
        self.apply_button.connect('clicked', self.accept)
        footer.append(cancel)
        footer.append(self.apply_button)
        outer.append(footer)
        self.buttons[plan['profile']].set_active(True)

    def selected(self, button, value):
        if button.get_active():
            self.choice = value
            for id, card in self.cards.items():
                (card.add_css_class if id==value else card.remove_css_class)('selected')
            if hasattr(self, 'summary'):
                self.summary.set_text(self.options[value]['label']+' selected')

    def key_pressed(self, controller, keyval, keycode, state):
        if keyval == Gdk.KEY_Escape:
            self.cancel()
            return True
        return False

    def finish(self, choice):
        Gtk.StyleContext.remove_provider_for_display(self.get_display(), self.provider)
        self.finished(choice)
        self.destroy()

    def cancel(self, *_):
        self.finish(None)
        return True

    def accept(self, *_):
        self.finish(self.choice)


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
