"""Three devices that say more about their owners than about engineering.

Same rules as the other sheets — a real job, plausible breakthroughs — but
the job exists only because people are the way they are.
"""

import math

from devices import centres, framing, start
from leisure import cuff, limb
from fidelity import enrich, seated, diner, dog, contour, hand, front_head
from sheet import ARC, GOLD, RED, WHITE, polar


# ---------------------------------------------------------------------------
# Proxy
# ---------------------------------------------------------------------------

def proxy(size):
    s = start(size, "proxy", 1212)
    mx, my, lx, rx = centres(s)
    s.begin_main(mx, my)
    framing(s, mx, my - 20, 478, a0=110, thick=(200, 245), thin=(320, 355))
    g = my + 300

    s.ln(mx - 440, g, mx + 440, g, 0.8, 0.9)
    for k in range(-22, 23):
        s.ln(mx + k * 20, g, mx + k * 20 - 9, g + 11, 0.3, 0.45)
    for k, (yy, x0) in enumerate(((my - 170, mx - 40), (my - 120, mx - 70), (my - 30, mx - 70), (my + 60, mx - 80), (my + 150, mx - 120))):
        s.fade_ln(x0, yy, x0 - 300 + k * 20, yy, 0.45, 0.0, 0.6)

    hipc, sh = (mx - 6, my + 20), (mx + 34, my - 178)
    # far-side arm and leg first, fainter
    e2, w2 = (mx - 44, my - 96), (mx - 108, my - 48)
    k2, a2 = (mx - 64, my + 138), (mx - 178, my + 236)
    limb(s, sh, e2, 17, 14, a=0.55, fill=0.03)
    limb(s, e2, w2, 14, 10, a=0.55, fill=0.03)
    hand(s, w2[0] - 8, w2[1] + 8, .55, 45, a=.6)
    for r in (20, 28, 36):
        s.arc(w2[0] - 8, w2[1] + 8, r, 140, 220, 0.5, 0.6)
    limb(s, hipc, k2, 26, 19, a=0.55, fill=0.03)
    limb(s, k2, a2, 19, 12, a=0.55, fill=0.03)
    s.poly([(a2[0] - 12, a2[1] - 6), (a2[0] + 16, a2[1] + 10), (mx - 122, g - 2), (mx - 152, g - 2)], 0.6, 0.8, fill=0.05)
    for j, r in ((e2, 9), (k2, 11), (a2, 8)):
        s.circ(j[0], j[1], r, 0.55, 0.7, fill=0.1)

    # torso with the owner's race number
    limb(s, hipc, sh, 46, 54, fill=0.07)
    s.c.save()
    s.c.translate((hipc[0] + sh[0]) / 2 + 6, (hipc[1] + sh[1]) / 2 - 10)
    s.c.rotate(math.radians(11.4))
    s.rect(-34, -26, 68, 52, 0.9, 0.8, fill=0.10)
    s.text_mid("114", 0, 2, 24, track=0.06, a=0.95, align="c", bold=True)
    s.text("CITY 10K", 0, -15, 5.5, a=0.7, align="c")
    s.c.restore()
    s.ln(sh[0] + 4, sh[1] - 50, sh[0] + 12, sh[1] - 88, 0.9, 1.0)
    s.ellipse(sh[0] + 12, sh[1] - 92, 22, 7, a=0.95, w=1.0)
    s.ellipse(sh[0] + 12, sh[1] - 92, 8, 2.5, a=0.9, w=0.7, color=ARC)

    # near-side leg and arm
    k1, a1 = (mx + 112, my + 96), (mx + 74, my + 226)
    limb(s, hipc, k1, 27, 20, fill=0.07)
    limb(s, k1, a1, 20, 13, fill=0.07)
    s.poly([(a1[0] - 12, a1[1] + 2), (a1[0] + 14, a1[1] - 6), (a1[0] + 62, a1[1] + 24), (a1[0] + 56, a1[1] + 36), (a1[0] - 10, a1[1] + 20)],
           0.95, 1.0, fill=0.08)
    e1, w1 = (mx + 104, my - 104), (mx + 172, my - 160)
    limb(s, sh, e1, 18, 15, fill=0.07)
    limb(s, e1, w1, 15, 11, fill=0.07)
    cuff(s, e1, w1, 0.52, 0.98, 14, fill=0.16, color=ARC)
    cuff(s, e1, w1, 0.70, 0.86, 17, fill=0.6, color=GOLD)
    hand(s, w1[0] + 9, w1[1] - 8, .55, -130)
    for j, r in ((sh, 14), (e1, 10), (hipc, 15), (k1, 12), (a1, 9)):
        s.circ(j[0], j[1], r, 0.95, 0.9, fill=0.18)
    px, py = w1[0] + 40, w1[1] - 44
    s.poly([(px, py), (px + 14, py), (px + 19, py - 12), (px + 25, py + 10), (px + 30, py), (px + 50, py)], 0.95, 0.9, close=False, color=GOLD)
    s.text("142 bpm", px + 56, py + 3, 7, a=0.9, color=GOLD)

    enrich(s, "proxy", mx, my)

    s.leader(sh[0] + 30, sh[1] - 94, 170, -50, 120, "HEAD", "NONE FITTED / NO TRACKER ASKS FOR ONE")
    s.leader(mx + 152, my - 142, 150, 60, 120, "OWNER'S WATCH", "THE ONLY PART THE INSURER SEES")
    s.leader(mx + 130, my - 124, 160, 130, 120, "LEFT WRIST", "SKIN, WARMTH, PULSE AND LIGHT SWEAT")
    s.leader(mx + 40, my - 60, 270, 130, 110, "CHEST", "BARE ALUMINIUM / NOBODY CHECKS")
    s.leader(k1[0] + 8, k1[1] + 30, 170, 80, 120, "RIGHT KNEE", "COPIES THE OWNER'S LIMP FROM A 2041 SKI TRIP")
    s.leader(w2[0] - 30, w2[1] + 8, -150, -70, -120, "WAVING HAND", "NEIGHBOURS ARE WITNESSES")
    s.leader(mx - 136, g - 4, -110, 60, -110, "FOOT", "WEARS OUT THE OWNER'S OWN SHOES")
    s.leader(mx - 30, my - 120, -250, -150, -110, "RACE NUMBER", "ENTERED UNDER THE OWNER'S NAME")
    s.end_main()

    s.legend("PROXY", "MODEL PX-1   /   EXERCISE, DELEGATED",
             "Runs ten kilometres every morning wearing the owner's fitness watch. The insurer sees an athlete "
             "and lowers the premium. The owner sees the ceiling and turns over.",
             [("ROBOTICS", "Legs that run on pavement, grass and stairs for two hours on a charge and find their own way home."),
              ("BIOMETRICS", "Copying one person's stride, arm swing and heartbeat so closely that a watch cannot tell who is wearing it."),
              ("MATERIALS SCIENCE", "Synthetic skin with a pulse, body warmth and sweat. Fitted to the left wrist only, to keep the price down."),
              ("BEHAVIOURAL ECONOMICS", "The finding that people will pay 4 000 a year to avoid doing something that is free.")],
             "2047")
    if not s.wide:
        return s

    # the wrist in section, left
    dx, dy = lx, 300
    s.detail_ring(dx, dy, 150)
    s.begin_clip_circle(dx, dy, 149)
    s.rect(dx - 80, dy - 96, 160, 40, 0.95, 1.1, fill=0.12)
    s.rect(dx - 16, dy - 58, 32, 6, 0.9, 0.6, fill=0.8, color=ARC)
    for off in (-8, 0, 8):
        s.ln(dx + off, dy - 52, dx + off * 2.4, dy - 6, 0.6, 0.5, dash=[2, 3], color=ARC)

    def skin():
        s.c.rectangle(dx - 160, dy - 50, 320, 22)
    s.hatch(skin, 3, 60, 0.35)
    s.rect(dx - 160, dy - 50, 320, 22, 0.8, 0.7)
    for k in range(-4, 5):
        x = dx + k * 34 + 12
        s.ln(x, dy - 28, x, dy - 50, 0.7, 0.5)
        s.circ(x, dy - 54, 2.2, 0.9, 0.5, fill=0.6, color=ARC)
    for yy in (dy - 14, dy + 8):
        s.ln(dx - 160, yy, dx + 160, yy, 0.85, 0.8, color=RED)
    s.ellipse(dx + 20, dy - 3, 34, 17, a=0.95, w=1.0, color=RED)
    s.poly([(dx - 160 + k * 12, dy + 26 + (8 if k % 2 else 0)) for k in range(28)], 0.85, 0.7, close=False, color=GOLD)

    def core():
        s.c.rectangle(dx - 160, dy + 46, 320, 120)
    s.hatch(core, 6, 45, 0.3)
    s.ln(dx - 160, dy + 46, dx + 160, dy + 46, 0.9, 0.9)
    s.end_clip()
    for yy, lab in ((dy - 76, "WATCH"), (dy - 39, "SKIN, WITH PORES"), (dy - 3, "PULSE TUBE"), (dy + 30, "HEATER, 33 °C"), (dy + 90, "ALUMINIUM")):
        s.ln(dx + 154, yy, dx + 166, yy, 0.5, 0.5)
        s.text(lab, dx + 172, yy + 3, 6.5, a=0.6)
    s.view_label(dx, dy + 190, "B", "LEFT WRIST", "SECTION / EVERYTHING A WATCH CAN MEASURE")

    # the owner, right
    qx, qy = rx, 330
    s.detail_ring(qx, qy, 170)
    s.rect(qx - 74, qy - 112, 148, 214, 0.95, 1.1, fill=0.04)
    s.rect(qx - 50, qy - 100, 100, 40, 0.8, 0.7, fill=0.08)
    front_head(s, qx - 4, qy - 80, .48)
    s.poly([(qx - 74, qy - 46), (qx + 74, qy - 52), (qx + 74, qy + 102), (qx - 74, qy + 102)], 0.9, 0.9, fill=0.07)
    s.bez((qx - 60, qy - 30), (qx - 20, qy + 10), (qx + 30, qy - 10), (qx + 60, qy + 40), 0.4, 0.5)
    s.bez((qx - 50, qy + 30), (qx - 10, qy + 60), (qx + 20, qy + 40), (qx + 50, qy + 84), 0.4, 0.5)
    s.rect(qx + 86, qy - 104, 46, 46, 0.8, 0.7)
    s.rect(qx + 97, qy - 98, 24, 34, 0.95, 0.8, fill=0.2, color=ARC)
    s.text("10.0 km", qx + 109, qy - 42, 7, a=0.95, align="c", color=ARC)
    s.text("DONE", qx + 109, qy - 30, 6, a=0.7, align="c", color=ARC)
    for i, (ox, oy, sz) in enumerate(((-36, -121, 9), (-52, -137, 12), (-72, -180, 16))):
        s.text("Z", qx + ox, qy + oy, sz, track=0, a=0.85 - i * 0.2, bold=True)
    s.view_label(qx, qy + 210, "C", "THE OWNER", "06:40, THE SAME MORNING")

    x0, y0, w_, h_ = rx - 170, 600, 260, 150
    s.chart(x0, y0, w_, h_, "THE OWNER'S FITNESS", lambda t: 0.30 + 0.62 * (1 - math.exp(-3.2 * t)), "YEARS OWNED, 0 – 5", "")
    s.poly([(x0 + w_ * i / 60, y0 + h_ * (1 - (0.30 - 0.22 * (i / 60.0) ** 0.8))) for i in range(61)], 0.8, 0.9, close=False, dash=[4, 3])
    s.text("SEEN BY THE INSURER", x0 + w_ - 4, y0 + 8, 6, a=0.9, align="r", color=ARC)
    s.text("SEEN BY THE STAIRS", x0 + w_ - 4, y0 + h_ - 22, 6, a=0.7, align="r")
    s.table(rx - 170, s.H - 190, [
        ("PROXY RUNS", "3 650 km / YEAR"), ("OWNER WALKS", "0.4 km, TO THE CHARGER"), ("PREMIUM", "DOWN 31 %"),
        ("MARATHONS FINISHED", "6"), ("MEDALS ON OWNER'S WALL", "6"),
    ], key_w=138)
    return s


# ---------------------------------------------------------------------------
# Greener
# ---------------------------------------------------------------------------

def gnome(s, x, g, lens=False):
    s.c.save();s.c.translate(x,g)
    contour(s,[("M",-15,0),("C",-18,-5,-12,-8,-10,-9),("L",-12,-21),
        ("C",-12,-30,-5,-34,0,-34),("C",8,-35,13,-26,13,-20),
        ("L",10,-8),("C",22,-5,18,0,14,0),("L",3,0),("L",0,-8),("L",-2,0)],w=.8,fill=.1,close=True)
    contour(s,[("M",-11,-37),("C",-8,-49,-1,-59,4,-63),
        ("C",3,-52,12,-46,11,-37),("C",5,-33,-5,-33,-11,-37)],w=.8,fill=.14,close=True)
    contour(s,[("M",-8,-29),("C",-10,-20,-3,-13,0,-12),
        ("C",7,-17,9,-21,7,-29)],a=.7,w=.65)
    s.ellipse(0,-31,3.4,4,a=.8,w=.55)
    for k in (-4,0,4):
        s.bez((k,-25),(k+2,-20),(k,-19),(0,-15),.4,.4)
    s.bez((-9,-23),(-14,-20),(-13,-16),(-9,-15),.7,.5)
    s.bez((10,-23),(15,-20),(14,-16),(10,-15),.7,.5)
    if lens:
        s.circ(-4,-32,2.2,.9,.4,color=ARC)
        s.dot(-4,-32,.8,.95,ARC)
    s.c.restore()


def mast(s, x, g, h, toward, color):
    """A periscope pole with a camera head looking over the fence."""
    for off in (-3, 3):
        s.ln(x + off, g, x + off, g - h, 0.9, 0.8)
    for k in range(1, int(h // 40)):
        s.ln(x - 3, g - k * 40, x + 3, g - k * 40, 0.5, 0.5)
    hx = x + toward * 26
    s.poly([(x - toward * 10, g - h - 22), (hx + toward * 18, g - h - 14), (hx + toward * 14, g - h + 8), (x - toward * 10, g - h + 2)],
           0.95, 1.0, fill=0.14)
    s.circ(hx + toward * 16, g - h - 3, 5, 0.95, 0.8, fill=0.6, color=color)
    return hx + toward * 16, g - h - 3


def greener(size):
    s = start(size, "greener", 1313)
    mx, my, lx, rx = centres(s)
    s.begin_main(mx, my)
    framing(s, mx, my - 20, 478, a0=200, thick=(150, 190), thin=(20, 55))
    g = my + 150

    # night sky
    s.circ(mx + 360, my - 370, 26, 0.9, 0.9, fill=0.10)
    s.arc(mx + 372, my - 376, 24, 120, 250, 0.6, 0.6)
    s.text("03:00", mx + 396, my - 366, 7, a=0.7)
    for k in range(14):
        s.cross(mx - 440 + s.rng.uniform(0, 760), my - 430 + s.rng.uniform(0, 150), 2.5, 0.5, 0.45)

    # ground, soil, the two buried antenna wires
    s.ln(mx - 470, g, mx + 470, g, 0.9, 1.0)
    for k in range(60):
        x, y = mx - 460 + s.rng.uniform(0, 920), g + s.rng.uniform(16, 150)
        s.ln(x, y, x + 5, y + 4, 0.25, 0.45)
    for x0, x1 in ((mx - 360, mx - 26), (mx + 26, mx + 440)):
        s.poly([(x, g + 46 + 7 * math.sin((x - x0) / 5.0)) for x in range(int(x0), int(x1), 2)], 0.85, 0.7, close=False, color=GOLD)

    # the owner's house and control box
    s.rect(mx - 470, g - 236, 84, 236, 0.9, 1.0, fill=0.05)
    s.poly([(mx - 470, g - 236), (mx - 470, g - 290), (mx - 372, g - 236)], 0.9, 1.0, fill=0.05)
    s.rect(mx - 450, g - 190, 40, 50, 0.7, 0.6, fill=0.12)
    s.rect(mx - 384, g - 120, 24, 38, 0.95, 0.9, fill=0.12)
    s.dot(mx - 372, g - 108, 2.4, 0.95, ARC)
    s.poly([(mx - 372, g - 82), (mx - 372, g + 46), (mx - 360, g + 46)], 0.7, 0.6, close=False, dash=[4, 3], color=GOLD)

    # fence, raised twice
    s.rect(mx - 6, g - 184, 12, 184, 0.95, 1.2, fill=0.12)
    s.rect(mx - 5, g - 240, 10, 56, 0.8, 0.8, fill=0.06, dash=[5, 3])
    s.rect(mx - 4, g - 282, 8, 42, 0.65, 0.7, fill=0.04, dash=[3, 3])

    # both units, each measuring the other lawn
    lens1 = mast(s, mx - 64, g, 318, 1, ARC)
    for k in range(7):
        s.fade_ln(lens1[0], lens1[1], mx + 90 + k * 55, g - 8, 0.6, 0.05, 0.5, ARC)
    for cx_, cy_, r in ((mx + 60, g - 40, 40), (mx + 96, g - 70, 46), (mx + 50, g - 104, 38), (mx + 100, g - 130, 34), (mx + 70, g - 160, 28)):
        s.circ(cx_, cy_, r, 0.45, 0.6, dash=[4, 3])
    lens2 = mast(s, mx + 76, g, 336, -1, GOLD)
    for k in range(7):
        s.fade_ln(lens2[0], lens2[1], mx - 90 - k * 42, g - 8, 0.6, 0.05, 0.5, GOLD)

    # grass, both sides equally and unreasonably green
    x = mx - 384
    while x < mx + 466:
        if abs(x - mx) > 9:
            h = s.rng.uniform(14, 30)
            s.ln(x, g, x + s.rng.uniform(-5, 5), g - h, s.rng.uniform(0.55, 0.98), 0.8, color=ARC)
        x += 2.6
    gnome(s, mx - 180, g)
    gnome(s, mx + 300, g, lens=True)
    s.fade_ln(mx + 297, g - 31, mx + 40, g - 60, 0.5, 0.0, 0.5, GOLD)
    for sx_ in (mx - 300, mx - 140, mx + 200, mx + 400):
        s.ln(sx_, g, sx_, g - 9, 0.9, 0.9)
        s.ln(sx_ - 6, g - 9, sx_ + 6, g - 9, 0.9, 0.9)

    enrich(s, "greener", mx, my)

    s.leader(lens1[0] - 18, lens1[1] - 6, -150, -70, -120, "PERISCOPE CAMERA", "READS THE NEIGHBOUR'S GREEN BY STARLIGHT")
    s.leader(lens2[0] + 20, lens2[1] - 6, 150, -30, 120, "THE NEIGHBOUR'S UNIT", "BOUGHT THREE WEEKS LATER / 18 mm TALLER")
    s.leader(mx + 5, g - 262, 210, 0, 110, "FENCE", "RAISED TWICE, BY BOTH PARTIES")
    s.leader(mx - 372, g - 100, -30, -190, 30, "CONTROL BOX", "SET TO: NEIGHBOUR + 4 %")
    s.leader(mx - 180, g - 50, -30, -100, -70, "GNOME", "DECOY. CONTAINS NOTHING.")
    s.leader(mx + 310, g - 46, 60, -90, 100, "THEIR GNOME", "CONTAINS A SECOND CAMERA")
    s.leader(mx - 200, g + 46, -60, 90, -110, "ANTENNA WIRE", "TELLS THE GRASS HOW GREEN TO BE")
    s.leader(mx + 118, g - 96, 80, 190, 110, "SHRUB", "PLANTED TO HIDE THE MAST. HIDES NOTHING.")
    s.end_main()

    s.legend("GREENER", "MODEL G-4   /   COMPETITIVE LAWN SYSTEM",
             "Keeps the owner's lawn exactly four per cent greener than the neighbour's. It measures their grass "
             "over the fence at night and corrects its own by morning. Most neighbours respond by buying one.",
             [("SYNTHETIC BIOLOGY", "Grass whose chlorophyll is set by a gene switch that listens to a radio signal from a wire under the turf."),
              ("REMOTE SENSING", "A camera that reads the exact green of a lawn by starlight, over a fence, from nine metres."),
              ("GAME THEORY", "A proof that two units facing each other never settle. Marketing called it a feature and sold them in pairs."),
              ("PUBLIC LAW", "A legal limit on how green grass may be, first passed in 2061 after airline pilots reported glare.")],
             "2049")
    if not s.wide:
        return s

    # leaf cells, left
    dx, dy = lx, 300
    s.detail_ring(dx, dy, 150)
    s.begin_clip_circle(dx, dy, 149)
    for i in range(-3, 4):
        for j in range(-3, 4):
            cx_, cy_ = dx + i * 64 + (32 if j % 2 else 0), dy + j * 52
            s.rect(cx_ - 30, cy_ - 24, 60, 48, 0.7, 0.7, fill=0.03)
            for _ in range(22):
                s.ellipse(cx_ + s.rng.uniform(-24, 24), cy_ + s.rng.uniform(-18, 18), 5, 2.6, rot=s.rng.uniform(0, 180),
                          a=0.9, w=0.6, color=ARC)
    s.end_clip()
    s.view_label(dx, dy + 190, "B", "LEAF CELLS", "CHLOROPLASTS PER CELL: 40 BEFORE, 310 NOW")

    # the street, right
    qx, qy = rx, 330
    s.ln(qx - 180, qy, qx + 180, qy, 0.4, 0.6, dash=[10, 8])
    for row in (0, 1):
        for k in range(4):
            no = (2 + k * 4) if row == 0 else (3 + k * 4)
            x = qx - 176 + k * 90
            y = qy - 168 if row == 0 else qy + 22
            first, paved = no == 14, no == 7
            s.rect(x, y, 82, 146, 0.9 if first else 0.6, 1.2 if first else 0.6, color=GOLD if first else WHITE)
            hy = y + 6 if row == 0 else y + 146 - 46
            ly = y + 52 if row == 0 else y + 6
            s.rect(x + 16, hy, 50, 40, 0.8, 0.7, fill=0.10)
            if paved:
                def lot(x=x, ly=ly):
                    s.c.rectangle(x + 6, ly, 70, 88)
                s.hatch(lot, 6, 45, 0.35)
            else:
                s.rect(x + 6, ly, 70, 88, 0.6, 0.5, fill=(0.30 if first else 0.12 + 0.02 * ((no * 7) % 9)), color=ARC)
            s.text(f"{no}", x + 41, (y - 6) if row == 0 else (y + 160), 6.5, track=0, a=0.8, align="c", color=GOLD if first else WHITE)
    s.view_label(qx, qy + 214, "C", "THE STREET, YEAR SIX", "No. 14 BOUGHT THE FIRST ONE. No. 7 PAVED THE LAWN.")

    x0, y0, w_, h_ = rx - 170, 640, 260, 110
    f1 = lambda t: min(0.84, 0.10 + 0.05 * math.exp(4.4 * t))
    s.chart(x0, y0, w_, h_, "GREEN OF BOTH LAWNS", f1, "YEARS, 0 – 12", "")
    s.poly([(x0 + w_ * i / 60, y0 + h_ * (1 - min(0.84, 0.10 + 0.05 * math.exp(4.4 * max(0, i / 60.0 - 0.03))) + 0.03)) for i in range(61)],
           0.8, 0.9, close=False, dash=[4, 3], color=GOLD)
    s.ln(x0, y0 + h_ * 0.16, x0 + w_, y0 + h_ * 0.16, 0.7, 0.6, dash=[2, 3], color=RED)
    s.text("LEGAL LIMIT", x0 + 6, y0 + h_ * 0.16 - 5, 6, a=0.9, color=RED)
    s.table(rx - 170, s.H - 190, [
        ("TARGET", "NEIGHBOUR + 4 %"), ("CHECKS PER NIGHT", "12"), ("FENCE RAISED", "TWICE"),
        ("SOLD IN PAIRS", "88 %"), ("SEEN FROM ORBIT", "SINCE 2059"),
    ], key_w=124)
    return s


# ---------------------------------------------------------------------------
# Truth lamp
# ---------------------------------------------------------------------------

def truth_lamp(size):
    s = start(size, "truth-lamp", 1414)
    mx, my, lx, rx = centres(s)
    s.begin_main(mx, my)
    framing(s, mx, my - 20, 478, a0=95, thick=(35, 70), thin=(310, 345))
    ceil, top, g = my - 410, my + 87, my + 300

    s.ln(mx - 440, ceil, mx + 440, ceil, 0.8, 0.9)
    for k in range(-22, 23):
        s.ln(mx + k * 20, ceil, mx + k * 20 + 9, ceil - 11, 0.3, 0.45)
    s.ln(mx - 440, g, mx + 440, g, 0.8, 0.9)

    # lamp
    s.rect(mx - 16, ceil, 32, 10, 0.9, 0.8, fill=0.2)
    s.ln(mx, ceil + 10, mx, my - 252, 0.9, 0.9)
    s.rect(mx - 7, my - 340, 14, 24, 0.95, 0.9, fill=0.6, color=GOLD)
    s.poly([(mx - 40, my - 252), (mx + 40, my - 252), (mx + 132, my - 172), (mx - 132, my - 172)], 0.95, 1.3, fill=0.09)
    s.rect(mx - 124, my - 172, 248, 13, 0.95, 1.0, fill=0.12)
    for k in range(9):
        s.circ(mx - 108 + k * 27, my - 165.5, 3.6, 0.95, 0.6, fill=0.5, color=ARC)
    for k in range(-7, 8):
        s.fade_ln(mx + k * 14, my - 158, mx + k * 46, top - 4, 0.55 - abs(k) * 0.03, 0.04, 0.6, RED)
    s.arc(mx, my - 159, 60, 20, 160, 0.8, 1.2, color=RED)

    # table, settings
    s.rect(mx - 336, top, 672, 16, 0.95, 1.2, fill=0.14)
    for sgn in (-1, 1):
        s.rect(mx + sgn * 250 - 8, top + 16, 16, g - top - 16, 0.9, 0.9, fill=0.08)
    # three people on the far side, one at each end
    far = [mx - 182, mx, mx + 182]
    for i, x in enumerate(far):
        diner(s, x, my - 46, i)
        s.ln(mx + (x - mx) * 0.3, my - 159, x, my - 78, 0.35, 0.45, dash=[2, 4], color=ARC)
    liar = far[2]
    s.circ(liar, my - 46, 42, 0.95, 1.1, dash=[5, 3], color=RED)
    s.dot(liar, my - 40, 3.2, 0.95, RED)
    ends = {-1: mx - 400, 1: mx + 400}
    for sgn, x in ends.items():
        seated(s, x, my - 46, facing=-sgn)
        s.ln(mx + sgn * 120, my - 165, x - sgn * 8, my - 74, 0.35, 0.45, dash=[2, 4], color=ARC)
    s.circ(ends[-1] + 4, my - 46, 40, 0.8, 0.8, dash=[2, 4], color=ARC)

    for k in range(5):
        x = mx - 264 + k * 132
        s.ellipse(x, top - 4, 32, 5, a=0.9, w=0.8)
        s.ln(x + 46, top, x + 46, top - 22, 0.8, 0.7)
        s.poly([(x + 36, top - 44), (x + 38, top - 26), (x + 46, top - 22), (x + 54, top - 26), (x + 56, top - 44)], 0.8, 0.7, close=False)

    # the dog
    dx_, dy_ = mx + 96, g - 46
    dog(s, dx_, dy_)

    enrich(s, "truth-lamp", mx, my)

    s.leader(mx - 124, my - 166, -170, -70, -120, "MICROPHONE RING", "HEARS THE HALF SECOND BEFORE \"OF COURSE NOT\"")
    s.leader(mx + 124, my - 166, 170, -90, 120, "THERMAL CAMERAS", "NOSES COOL BY 0.4 °C WHEN THEIR OWNERS LIE")
    s.leader(mx - 70, my - 214, -150, -130, -120, "LAMP", "GLOWS RED FOR THREE SECONDS. NOT DIMMABLE.")
    s.leader(mx + 7, my - 328, 150, -36, 110, "OFF SWITCH", "NEW IN VERSION 2")
    s.leader(liar + 38, my - 66, 110, -40, 120, "SEAT 4", "\"NO, I LOVE IT. I'LL WEAR IT ALL THE TIME.\"")
    s.leader(ends[-1] + 4, my - 86, 30, -90, 80, "SEAT 1, GRANDMOTHER", "NEVER SETS IT OFF. SAYS WHAT SHE THINKS.")
    s.leader(dx_ + 70, dy_ - 10, 120, -50, 110, "DOG", "HAS NEVER SET IT OFF EITHER")
    s.leader(mx - 60, top - 4, -120, 190, -110, "DINNER", "THE SUBJECT OF 31 % OF ALL DETECTIONS")
    s.end_main()

    s.legend("TRUTH LAMP", "MODEL TL-1   /   LIE DETECTOR FOR THE DINING TABLE",
             "Hangs over the table and glows red for three seconds whenever someone says a thing they do not "
             "believe. It is right 97 % of the time. Most owners unplug it before dessert.",
             [("AFFECTIVE SCIENCE", "Reading a lie from voice, face and the temperature of the nose, at three metres, without touching anyone."),
              ("SIGNAL PROCESSING", "Telling six people apart while all of them talk at once, which at this table is always."),
              ("SOCIOLOGY", "The discovery, made with this lamp, that a family dinner runs on about forty small untruths an hour and stops without them."),
              ("PRODUCT DESIGN", "An off switch. Added in version 2, and the only change in version 2.")],
             "2046")
    if not s.wide:
        return s

    # one dinner by seat, left
    tx, ty = lx, 300
    s.c.new_sub_path()
    s.c.arc(tx + 70, ty, 56, -math.pi / 2, math.pi / 2)
    s.c.arc(tx - 70, ty, 56, math.pi / 2, 1.5 * math.pi)
    s.c.close_path()
    s._ink(0.07, WHITE)
    s.c.fill_preserve()
    s._stroke(0.95, 1.2, None, WHITE)
    s.circ(tx, ty, 16, 0.7, 0.7, color=RED)
    s.circ(tx, ty, 8, 0.9, 0.8, fill=0.5, color=RED)
    seats = [(-176, 0, "GRANDMOTHER", 0), (-70, -104, "UNCLE", 14), (70, -104, "AUNT", 9),
             (176, 0, "HOST", 22), (70, 104, "GUEST", 17), (-70, 104, "TEENAGER", 11)]
    for ox, oy, who, n in seats:
        col = ARC if n == 0 else (RED if n >= 20 else WHITE)
        s.circ(tx + ox, ty + oy, 24, 0.95, 1.0, fill=0.10, color=col)
        s.text_mid(f"{n}", tx + ox, ty + oy, 13, track=0, a=0.95, align="c", bold=True, color=col)
        s.text(who, tx + ox, ty + oy + (42 if oy >= 0 else -32), 6.5, a=0.7, align="c")
    s.view_label(tx, ty + 200, "B", "ONE DINNER", "UNTRUTHS DETECTED, BY SEAT")

    # what it hears most, right
    s.text("MOST DETECTED SENTENCES", rx - 170, 196, 7.5, a=0.8)
    s.table(rx - 170, 226, [
        ("“IT'S DELICIOUS”", "31 %"), ("“WE SHOULD DO THIS MORE OFTEN”", "22 %"), ("“I'M FINE”", "19 %"),
        ("“NO, YOU CHOOSE”", "11 %"), ("“TRAFFIC WAS TERRIBLE”", "9 %"), ("“I WAS JUST ABOUT TO CALL YOU”", "8 %"),
    ], key_w=226, size=7, lead=24)
    s.view_label(rx - 170, 410, "C", "FIELD DATA", "11 000 DINNERS, BEFORE THE RETURNS BEGAN", align="l")

    s.chart(rx - 170, 600, 260, 150, "LAMPS STILL PLUGGED IN",
            lambda t: 0.04 + 0.92 * math.exp(-9 * t), "DAYS SINCE PURCHASE, 0 – 30", "")
    s.table(rx - 170, s.H - 190, [
        ("RIGHT", "97 % OF THE TIME"), ("UNTRUTHS PER DINNER", "40"), ("OF THOSE, KIND ONES", "36"),
        ("TYPICAL OWNERSHIP", "ONE DINNER"), ("GIVEN AWAY AS A GIFT", "61 %"),
    ], key_w=132)
    return s


SHEETS = [
    ("proxy", proxy),
    ("greener", greener),
    ("truth-lamp", truth_lamp),
]
