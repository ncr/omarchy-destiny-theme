"""The order of the sheets, and the colour mood of each one.

Omarchy cycles backgrounds by file name, so this list is the order people see.
It is arranged by hand: neighbours are far apart in hue, so every switch
changes how the desktop feels, and the serious sheets, the playful ones and the
three jokes take turns. The first sheet is the one a new user sees; it sits
closest to the theme's own navy.

A sheet's number, its file name prefix and the "NCR-07" printed on it all come
from its position here. To reorder, move a line.
"""

# (sheet, palette from sheet.PALETTES)
ORDER = [
    ("quantum-simulator", "indigo"),
    ("sky-racer", "petrol"),
    ("fusion-transport", "rust"),
    ("greener", "grass"),
    ("cortical-mesh", "plum"),
    ("bounder", "royal"),
    ("air-refinery", "olive"),
    ("aroma-organ", "wine"),
    ("tether-climber", "navy"),
    ("truth-lamp", "umber"),
    ("organ-foundry", "teal"),
    ("volumetric-stage", "violet"),
    ("proxy", "sand"),
    ("presence-rig", "graphite"),
]

TOTAL = len(ORDER)


def number(sheet):
    return [name for name, _ in ORDER].index(sheet) + 1


def palette(sheet):
    return dict(ORDER)[sheet]
