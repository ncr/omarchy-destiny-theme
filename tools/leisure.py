"""Five more devices, this time for fun: racing, shows, games, smell, athletics.

Same rules as devices.py: a real job, breakthroughs that have not happened
yet, plausible within about fifty years. Nothing here saves the world.
"""

import math

from devices import centres, framing, start, truss
from sheet import ARC, GOLD, WHITE, polar


# ---------------------------------------------------------------------------
# 07  Sky racer
# ---------------------------------------------------------------------------

def sky_racer(size):
    s = start(size, 7, 707)
    mx, my, lx, rx = centres(s)
    s.begin_main(mx, my)
    framing(s, mx, my, 478, a0=100, thick=(205, 250), thin=(330, 372))
    c = s.c

    # the envelope the flight computer keeps clear
    s.circ(mx, my, 440, 0.4, 0.6, dash=[5, 4], color=ARC)
    fans = [(sgn * fx, fy, r) for fx, fy, r in ((215, -185, 88), (305, 15, 98), (215, 215, 88)) for sgn in (-1, 1)]
    sensors = [(0, -196, -90), (0, 186, 90)] + [(fx + math.copysign(r, fx), fy, 0 if fx > 0 else 180) for fx, fy, r in fans]
    for ox, oy, d in sensors:
        for spread in (-16, 0, 16):
            s.fade_ln(mx + ox, my + oy, *polar(mx + ox, my + oy, 130, d + spread), 0.5, 0.0, 0.5, ARC)
        s.dot(mx + ox, my + oy, 2.4, 0.95, ARC)

    # arms
    for fx, fy, r in fans:
        sgn = 1 if fx > 0 else -1
        p1 = (mx + sgn * 44, my + fy * 0.35)
        ang = math.atan2(my + fy - p1[1], mx + fx - p1[0])
        p2 = (mx + fx - r * math.cos(ang), my + fy - r * math.sin(ang))
        nx, ny = -math.sin(ang) * 5, math.cos(ang) * 5
        for k in (-1, 1):
            s.ln(p1[0] + k * nx, p1[1] + k * ny, p2[0] + k * nx, p2[1] + k * ny, 0.85, 0.8)
        mid = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
        s.circ(mid[0], mid[1], 6, 0.8, 0.6, fill=0.2)

    # ducted fans, rim-driven
    for i, (fx, fy, r) in enumerate(fans):
        x, y = mx + fx, my + fy
        s.circ(x, y, r, 0.95, 1.3, fill=0.04)
        s.circ(x, y, r - 9, 0.5, 0.5)
        s.circ(x, y, r - 4.5, 0.85, 1.8, dash=[6, 3], color=ARC)
        turn = 1 if i % 2 else -1
        for k in range(7):
            d = k * 360 / 7 + i * 13
            s.bez(polar(x, y, 15, d), polar(x, y, r * 0.45, d + turn * 10), polar(x, y, r * 0.75, d + turn * 26),
                  polar(x, y, r - 10, d + turn * 40), 0.7, 0.7)
        for k in range(3):
            s.ln(*polar(x, y, 15, k * 120 + 30), *polar(x, y, r - 9, k * 120 + 30), 0.3, 0.45, dash=[3, 3])
        s.circ(x, y, 15, 0.95, 0.9, fill=0.18)
        a0 = 200 if turn > 0 else 340
        s.arc(x, y, r + 10, min(a0, a0 + turn * 50), max(a0, a0 + turn * 50), 0.6, 0.6)
        tip = polar(x, y, r + 10, a0 + turn * 50)
        back = polar(x, y, r + 10, a0 + turn * 44)
        s.arrow(back[0], back[1], tip[0], tip[1], 0.7, 0.5, head=6)

    # pod: teardrop, nose up
    def pod(k=1.0):
        c.move_to(mx, my - 196 * k)
        c.curve_to(mx + 58 * k, my - 150 * k, mx + 60 * k, my - 20 * k, mx + 42 * k, my + 84 * k)
        c.curve_to(mx + 30 * k, my + 136 * k, mx + 10 * k, my + 176 * k, mx, my + 186 * k)
        c.curve_to(mx - 10 * k, my + 176 * k, mx - 30 * k, my + 136 * k, mx - 42 * k, my + 84 * k)
        c.curve_to(mx - 60 * k, my - 20 * k, mx - 58 * k, my - 150 * k, mx, my - 196 * k)
        c.close_path()
    pod()
    s._ink(0.07, WHITE)
    c.fill_preserve()
    s._stroke(0.95, 1.3, None, WHITE)
    c.save()
    c.translate(0, -my * 0.0)
    pod(0.62)
    c.restore()
    s._stroke(0.6, 0.6, None, WHITE)
    s.ellipse(mx, my - 40, 40, 96, a=0.5, w=0.6, dash=[4, 3], color=ARC)
    s.circ(mx, my - 64, 15, 0.9, 0.9, fill=0.2)
    s.rect(mx - 17, my - 44, 34, 58, 0.6, 0.5)
    for sgn in (-1, 1):
        s.rect(mx + sgn * 24 - 7, my + 10, 14, 120, 0.6, 0.5, dash=[4, 3], color=GOLD)
        s.ln(mx + sgn * 64, my - 120, mx + sgn * 64, my + 150, 0.3, 0.5, dash=[8, 4])

    s.leader(mx + 305 + 60, my + 15 - 60, 100, -150, 110, "RIM-DRIVEN FAN", "6 OFF / 95 kW EACH")
    s.leader(mx + 26, my - 100, 150, -250, 120, "CRASH CELL", "PILOT, SEAT AND HARNESS")
    s.leader(mx + 24, my + 100, 330, 130, 110, "LITHIUM-AIR PACK", "1 100 Wh PER kg")
    s.leader(mx, my - 196, -150, -150, -120, "SENSING ARRAY", "14 HEADS / SEES 200 m")
    s.leader(*polar(mx, my, 440, 160), -70, -60, -90, "KEEP-CLEAR ENVELOPE", "NOTHING COMES CLOSER THAN 3 m")
    s.leader(mx - 150, my + 140, -190, 160, -110, "FOLDING ARM", "WOVEN NANOTUBE FIBRE")
    s.dim(mx - 403, my + 440, mx + 403, my + 440, "SPAN 4.6 m", a=0.4)
    s.end_main()

    s.legend("SKY RACER", "CLASS SR-1   /   ONE-SEAT ELECTRIC RACING COPTER",
             "A racing aircraft for one pilot, flown through courses of gates in the air at up to 320 km/h. "
             "The pilot steers; the machine refuses to hit a gate, the ground or another racer.",
             [("ELECTROCHEMISTRY", "Lithium-air cells that hold 1 100 Wh per kilogram, four times today's best, and survive a thousand fast charges."),
              ("MOTOR DESIGN", "Fan motors built into the duct rim and wound with carbon nanotube wire, 25 kW for every kilogram."),
              ("AUTONOMY", "A flight computer that tracks every racer and gate a thousand times a second and overrides the pilot only in the last metre."),
              ("MATERIALS SCIENCE", "Airframes woven from nanotube fibre, half the mass of carbon composite, that fold around the cockpit instead of shattering.")],
             "2052")
    if not s.wide:
        return s

    # side view, pitched forward
    c.save()
    c.translate(lx, 300)
    s.ln(-210, 40, 210, 40, 0.25, 0.5, dash=[18, 4, 3, 4])
    c.rotate(math.radians(-12))
    k = 0.62
    c.move_to(-196 * k, 6)
    c.curve_to(-150 * k, -30, -80 * k, -52, -10 * k, -50)
    c.curve_to(70 * k, -46, 150 * k, -22, 186 * k, -4)
    c.curve_to(120 * k, 26, -120 * k, 30, -196 * k, 6)
    c.close_path()
    s._ink(0.07, WHITE)
    c.fill_preserve()
    s._stroke(0.95, 1.2, None, WHITE)
    s.bez((-130 * k, -28), (-90 * k, -58), (-10 * k, -62), (40 * k, -42), 0.7, 0.6, color=ARC)
    for x0, x1 in ((-273, -97), (-83, 113), (127, 303)):
        s.rect(x0 * k, -4, (x1 - x0) * k, 16, 0.9, 0.9, fill=0.12)
        s.ln(x0 * k, 4, x1 * k, 4, 0.8, 0.8, color=ARC)
    for x in (-60, 60):
        s.ln(x * k, 22, x * k - 6, 48, 0.7, 0.6)
    s.ln(-110 * k, 48, 110 * k, 48, 0.9, 0.9)
    c.restore()
    s.arc(lx, 340, 150, 168, 180, 0.7, 0.7)
    s.text("12°", lx - 172, 322, 7, a=0.8)
    s.view_label(lx, 470, "B", "SIDE VIEW", "RACING ATTITUDE, NOSE DOWN")

    # a course, right
    qx, qy = rx, 330
    s.detail_ring(qx, qy, 170)

    def course(t):
        return (qx + 118 * math.sin(t) + 30 * math.sin(2 * t + 0.6), qy + 92 * math.cos(t) - 38 * math.cos(3 * t))
    s.poly([course(i * 2 * math.pi / 240) for i in range(240)], 0.95, 1.2, color=ARC)
    for g in range(9):
        t = g * 2 * math.pi / 9 + 0.2
        x, y = course(t)
        x2, y2 = course(t + 0.01)
        ang = math.degrees(math.atan2(y2 - y, x2 - x)) + 90
        a_, b_ = polar(x, y, 11, ang), polar(x, y, 11, ang + 180)
        s.ln(a_[0], a_[1], b_[0], b_[1], 0.95, 1.6, color=GOLD if g == 0 else WHITE)
        tx, ty = polar(x, y, 22, ang)
        s.text(f"{g + 1}", tx, ty + 3, 6.5, track=0, a=0.7, align="c")
    s.view_label(qx, qy + 210, "C", "COURSE", "9 GATES / 2.4 km / 30 – 180 m ABOVE GROUND")

    s.chart(rx - 170, 600, 260, 150, "SPEED OVER ONE LAP",
            lambda t: 0.55 + 0.22 * math.sin(t * 17) * math.cos(t * 5) + 0.15 * math.sin(t * 7 + 1), "GATE 1 – 9", "km/h")
    s.table(rx - 170, s.H - 190, [
        ("TOP SPEED", "320 km/h"), ("PEAK POWER", "570 kW"), ("MASS WITH PILOT", "410 kg"),
        ("TURN LOAD", "6 g"), ("ONE HEAT", "12 min"),
    ], key_w=120)
    return s


# ---------------------------------------------------------------------------
# 08  Volumetric stage
# ---------------------------------------------------------------------------

def volumetric_stage(size):
    s = start(size, 8, 808)
    mx, my, lx, rx = centres(s)
    s.begin_main(mx, my)
    framing(s, mx, my - 30, 480, a0=30, thick=(200, 240), thin=(305, 345))
    deck = my + 250

    # deck, towers, bridge
    s.rect(mx - 450, deck, 900, 16, 0.95, 1.1, fill=0.10)
    for sgn in (-1, 1):
        truss(s, mx + sgn * 412, deck, mx + sgn * 412, my - 344, depth=30, bay=30, a=0.8)
    truss(s, mx - 427, my - 357, mx + 427, my - 357, depth=26, bay=26, a=0.8)
    heads = []
    for sgn in (-1, 1):
        for k in range(5):
            y = my - 290 + k * 112
            x = mx + sgn * 397
            s.poly([(x, y - 9), (x - sgn * 24, y - 5), (x - sgn * 24, y + 5), (x, y + 9)], 0.95, 0.8, fill=0.2)
            heads.append((x - sgn * 24, y))
    for k in range(7):
        x = mx - 300 + k * 100
        s.poly([(x - 9, my - 344), (x - 5, my - 322), (x + 5, my - 322), (x + 9, my - 344)], 0.95, 0.8, fill=0.2)
        heads.append((x, my - 322))
    for k in range(9):
        x = mx - 320 + k * 80
        s.rect(x - 12, deck - 12, 24, 12, 0.9, 0.7, fill=0.12)
        for off in (-7, 0, 7):
            s.fade_ln(x, deck - 12, x + off * 2.2, deck - 80, 0.28, 0.0, 0.5)

    # the volume the image lives in
    s.rect(mx - 336, my - 296, 672, 516, 0.35, 0.5, dash=[6, 4])
    for cx_, cy_ in ((mx - 336, my - 296), (mx + 336, my - 296), (mx - 336, my + 220), (mx + 336, my + 220)):
        s.cross(cx_, cy_, 7, 0.8, 0.7)

    # the image: a trefoil knot of light, drawn as voxels
    tilt = math.radians(72)
    pts = []
    n = 1700
    for i in range(n):
        t = 2 * math.pi * i / n
        for _ in range(4):
            X = (math.sin(t) + 2 * math.sin(2 * t)) / 2.0 + s.rng.gauss(0, 0.035)
            Y = (math.cos(t) - 2 * math.cos(2 * t)) / 2.0 + s.rng.gauss(0, 0.035)
            Z = -0.55 * math.sin(3 * t) + s.rng.gauss(0, 0.035)
            depth = Y * math.cos(tilt) - Z * math.sin(tilt)
            up = Y * math.sin(tilt) + Z * math.cos(tilt)
            pts.append((depth, mx + 150 * X, my - 20 - 150 * up))
    pts.sort()
    for depth, x, y in pts:
        near = min(1.0, max(0.0, (depth + 1.3) / 2.6))
        s.dot(x, y, 0.7 + 1.2 * near, 0.2 + 0.75 * near, WHITE if s.rng.random() < 0.12 else ARC)
    lit = [pts[900], pts[3300], pts[5600]]
    for (hx, hy), (_, vx, vy) in zip((heads[1], heads[6], heads[12], heads[3], heads[8], heads[14]), lit + lit):
        s.ln(hx, hy, vx, vy, 0.22, 0.45, dash=[2, 4])
    right = max(pts, key=lambda p: p[1])

    # audience, seen from behind
    for row in range(3):
        for k in range(40 - row):
            x = mx - 380 + k * 19.5 + row * 9.7
            s.circ(x, deck + 50 + row * 22, 5.5, 0.4 - row * 0.08, 0.5, fill=0.05)

    s.leader(heads[0][0] + 10, heads[0][1], -150, -90, -120, "EMITTER HEAD", "INFRARED / STEERED ON A CHIP")
    s.leader(mx - 427, my - 100, -60, 60, -100, "TOWER", "24 m")
    s.leader(mx + 100, my - 357, 140, -60, 120, "BRIDGE", "7 HEADS POINTING DOWN")
    s.leader(mx + 336, my - 120, 120, -40, 110, "IMAGE VOLUME", "40 × 22 × 18 m")
    s.leader(right[1], right[2], 46, -80, 46, "VOXEL", None)
    s.leader(mx + 240, deck - 8, 250, 70, 110, "HAZE UNIT", "LIGHT-CONVERTING PARTICLES")
    s.dim(mx - 336, my - 420, mx + 336, my - 420, "40 m", a=0.4)
    s.ln(mx - 336, my - 296, mx - 336, my - 426, 0.1, 0.4)
    s.ln(mx + 336, my - 296, mx + 336, my - 426, 0.1, 0.4)
    s.end_main()

    s.legend("VOLUMETRIC STAGE", "MODEL VS-40   /   MOVING 3D IMAGES IN OPEN AIR",
             "Draws moving three-dimensional images in the air above a stage, forty metres wide, seen "
             "correctly from every seat without glasses. For concerts, theatre and sport replays.",
             [("PHOTONICS", "Haze particles that turn infrared into visible light a thousand times better than today's, and only where two beams cross."),
              ("OPTICAL CHIPS", "Beam steering on a chip, with no moving parts, that aims at two billion points sixty times a second."),
              ("AEROSOL SCIENCE", "A haze proven harmless to breathe for hours and cleared from the hall air within a minute."),
              ("COMPUTER GRAPHICS", "Rendering a whole volume at once instead of one camera view, live, from performers on stage.")],
             "2060")
    if not s.wide:
        return s

    # hall plan, left
    s.rect(lx - 120, 150, 240, 84, 0.95, 1.1, fill=0.06)
    s.ellipse(lx, 192, 96, 30, a=0.7, w=0.7, dash=[4, 3], color=ARC)
    for sgn in (-1, 1):
        s.rect(lx + sgn * 112 - 6, 186, 12, 12, 0.95, 0.8, fill=0.5)
    for k in range(9):
        r = 96 + k * 20
        for a0, a1 in ((24, 68), (74, 106), (112, 156)):
            s.arc(lx, 214, r, a0, a1, 0.75 - k * 0.05, 0.9 if k == 0 else 0.6)
    s.view_label(lx, 520, "B", "HALL PLAN", "12 000 SEATS / EVERY ONE SEES DEPTH")

    # one voxel, right
    qx, qy = rx, 330
    s.detail_ring(qx, qy, 170)
    s.begin_clip_circle(qx, qy, 169)
    for ang in (-24, 24):
        for off in (-9, 9):
            ox, oy = polar(0, 0, off, ang + 90)
            a_, b_ = polar(qx + ox, qy + oy, 200, ang), polar(qx + ox, qy + oy, 200, ang + 180)
            s.ln(a_[0], a_[1], b_[0], b_[1], 0.6, 0.6, dash=[6, 4])
    s.poly([(qx - 22, qy), (qx, qy - 10), (qx + 22, qy), (qx, qy + 10)], 0.9, 0.7, fill=0.25, color=ARC)
    for k in range(70):
        x, y = qx + s.rng.uniform(-170, 170), qy + s.rng.uniform(-170, 170)
        inside = abs(x - qx) / 22 + abs(y - qy) / 10 < 1.4
        if inside:
            s.circ(x, y, 7, 0.4, 0.5, color=ARC)
            s.dot(x, y, 3, 0.95, ARC)
        else:
            s.circ(x, y, s.rng.uniform(1.5, 3), 0.35, 0.45)
    s.end_clip()
    s.ln(qx - 120, qy + 140, qx - 60, qy + 140, 0.9, 1.0)
    s.text("1 mm", qx - 90, qy + 132, 6.5, a=0.8, align="c")
    s.view_label(qx, qy + 210, "C", "ONE VOXEL", "PARTICLES GLOW ONLY INSIDE THE CROSSING")

    s.chart(rx - 170, 600, 260, 150, "LIGHT FROM ONE PARTICLE",
            lambda t: 0.04 + 0.92 * math.exp(-(((t - 0.5) / 0.045) ** 2)), "DISTANCE FROM THE CROSSING, ± 5 mm", "")
    s.table(rx - 170, s.H - 190, [
        ("VOXELS", "2 × 10⁹"), ("REFRESH", "60 Hz"), ("EMITTER HEADS", "17"),
        ("GLASSES", "NONE"), ("AUDIENCE", "12 000"),
    ], key_w=110)
    return s


# ---------------------------------------------------------------------------
# 09  Presence rig
# ---------------------------------------------------------------------------

def limb(s, p1, p2, r1, r2, a=0.9, w=1.0, fill=0.05, dash=None):
    """A tapered body segment between two joints."""
    ang = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    nx, ny = -math.sin(ang), math.cos(ang)
    s.poly([(p1[0] + nx * r1, p1[1] + ny * r1), (p2[0] + nx * r2, p2[1] + ny * r2),
            (p2[0] - nx * r2, p2[1] - ny * r2), (p1[0] - nx * r1, p1[1] - ny * r1)], a, w, True, fill, dash)


def cuff(s, p1, p2, f0, f1, half, a=0.9, fill=0.3, color=ARC):
    """A band across a limb, from fraction f0 to f1 of its length."""
    ang = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    nx, ny = -math.sin(ang) * half, math.cos(ang) * half
    a_ = (p1[0] + (p2[0] - p1[0]) * f0, p1[1] + (p2[1] - p1[1]) * f0)
    b_ = (p1[0] + (p2[0] - p1[0]) * f1, p1[1] + (p2[1] - p1[1]) * f1)
    s.poly([(a_[0] + nx, a_[1] + ny), (b_[0] + nx, b_[1] + ny), (b_[0] - nx, b_[1] - ny), (a_[0] - nx, a_[1] - ny)],
           a, 0.6, True, fill, None, color)


def presence_rig(size):
    s = start(size, 9, 909)
    mx, my, lx, rx = centres(s)
    s.begin_main(mx, my)
    framing(s, mx, my - 30, 478, a0=20, thick=(195, 235), thin=(300, 340))
    floor = my + 250

    # roller floor, pylons, overhead arch
    s.rect(mx - 400, floor, 800, 24, 0.95, 1.1, fill=0.10)
    for k in range(80):
        x = mx - 395 + k * 10
        s.arc(x, floor, 4, 180, 360, 0.6, 0.5, color=ARC if abs(x - mx) < 70 else WHITE)
    for sgn in (-1, 1):
        s.rect(mx + sgn * 430 - 9, my - 380, 18, 654, 0.85, 0.8, fill=0.05)
        for off in (-5, 5):
            s.bez((mx + sgn * 430, my - 380 + off), (mx + sgn * 300, my - 440 + off), (mx + sgn * 120, my - 432 + off),
                  (mx, my - 432 + off), 0.8, 0.7)
        s.ln(mx + sgn * 34, my - 404, mx + sgn * 84, my - 246, 0.5, 0.5, dash=[5, 3])
    s.ellipse(mx, my - 410, 44, 10, a=0.9, w=0.9)
    s.ln(mx, my - 427, mx, my - 420, 0.8, 0.7)
    for sgn in (-1, 1):
        s.arrow(mx + sgn * 30 + 26, floor + 40, mx + sgn * 30 - 26, floor + 40, 0.8, 0.7, head=6, color=ARC)
    s.text("FLOOR RUNS AT −1.4 m/s", mx, floor + 62, 6.5, a=0.8, align="c", color=ARC)

    # the player in the suit
    head = (mx, my - 300)
    sh = {-1: (mx - 86, my - 236), 1: (mx + 86, my - 236)}
    el = {-1: (mx - 126, my - 118), 1: (mx + 132, my - 130)}
    wr = {-1: (mx - 150, my - 6), 1: (mx + 176, my - 36)}
    hip = {-1: (mx - 36, my - 30), 1: (mx + 36, my - 30)}
    kn = {-1: (mx - 50, my + 104), 1: (mx + 62, my + 96)}
    an = {-1: (mx - 52, my + 220), 1: (mx + 84, my + 214)}
    torso = [(mx - 84, my - 250), (mx + 84, my - 250), (mx + 56, my - 74), (mx + 64, my - 24), (mx - 64, my - 24), (mx - 56, my - 74)]
    s.poly(torso, 0.95, 1.2, fill=0.05)
    s.c.save()
    s.c.move_to(*torso[0])
    for p in torso[1:]:
        s.c.line_to(*p)
    s.c.close_path()
    s.c.clip()
    for i in range(-10, 11):
        for j in range(0, 26):
            s.dot(mx + i * 9 + (4.5 if j % 2 else 0), my - 246 + j * 9, 0.9, 0.55)
    s.c.restore()
    s.rect(mx - 22, my - 214, 44, 56, 0.9, 0.8, fill=0.14)
    s.rect(mx - 12, my - 200, 24, 24, 0.9, 0.6, color=ARC)
    s.rect(mx - 9, my - 268, 18, 20, 0.8, 0.7)
    s.circ(head[0], head[1], 34, 0.95, 1.2, fill=0.06)
    s.band(head[0], head[1], 22, 34, 205, 335, 0.9, 0.7, fill=0.35, color=ARC)
    for sgn in (-1, 1):
        s.rect(head[0] + sgn * 33 - 4, head[1] + 2, 8, 16, 0.95, 0.7, fill=0.7, color=GOLD)
        limb(s, sh[sgn], el[sgn], 19, 15)
        limb(s, el[sgn], wr[sgn], 15, 11)
        limb(s, hip[sgn], kn[sgn], 27, 19)
        limb(s, kn[sgn], an[sgn], 19, 13)
        for p1, p2, half in ((sh[sgn], el[sgn], 21), (el[sgn], wr[sgn], 17), (hip[sgn], kn[sgn], 29), (kn[sgn], an[sgn], 21)):
            for f0 in (0.28, 0.58):
                cuff(s, p1, p2, f0, f0 + 0.10, half)
        for j, r in ((sh[sgn], 12), (el[sgn], 10), (hip[sgn], 13), (kn[sgn], 12), (an[sgn], 9)):
            s.circ(j[0], j[1], r, 0.9, 0.8, fill=0.18)
        hx, hy = wr[sgn][0] + sgn * 6, wr[sgn][1] + 22
        s.circ(hx, hy, 15, 0.9, 0.9, fill=0.08)
        for k in range(-2, 3):
            s.ln(*polar(hx, hy, 15, 90 + k * 22 - sgn * 10), *polar(hx, hy, 34, 90 + k * 24 - sgn * 10), 0.85, 0.8)
        for k in range(12):
            s.dot(*polar(hx, hy, s.rng.uniform(2, 12), s.rng.uniform(0, 360)), 1.0, 0.9, ARC)
        fx = an[sgn][0]
        s.poly([(fx - 16, an[sgn][1] + 8), (fx + sgn * 44, an[sgn][1] + 20), (fx + sgn * 46, floor - 4), (fx - 16, floor - 4)],
               0.9, 0.9, fill=0.10)

    s.leader(head[0] + 24, head[1] - 12, 190, -70, 110, "HEADSET", "SIGHT AND SOUND")
    s.leader(head[0] + 36, head[1] + 10, 250, 10, 120, "INNER-EAR PADS", "A FEW mA, FELT AS ACCELERATION")
    s.leader(el[1][0] - 18, el[1][1] - 44, 210, -10, 120, "MUSCLE BAND", "RESISTS OR ASSISTS EVERY JOINT")
    s.leader(mx + 40, my - 120, 300, 110, 110, "TACTILE SKIN", "A MILLION MOVING POINTS")
    s.leader(wr[-1][0] - 8, wr[-1][1] + 26, -150, 30, -110, "GLOVE", "1 POINT PER mm²")
    s.leader(mx - 12, my - 190, -250, -90, -110, "SUIT COMPUTER", None)
    s.leader(mx - 60, my - 330, -180, -40, -110, "SAFETY TETHER", None)
    s.leader(mx - 250, floor + 4, -60, 70, -110, "ROLLER FLOOR", "MOVES THE GROUND, NOT THE PLAYER")
    s.end_main()

    s.legend("PRESENCE RIG", "MODEL PR-2   /   SUIT AND FLOOR FOR FULL-BODY GAMES",
             "Lets a player walk, climb and fight inside a game and feel it: weight in the arms, wind on the "
             "skin, the lurch of a fall. The floor slides under the feet, so a living room is enough.",
             [("SOFT ROBOTICS", "Woven polymer muscle fibres, as strong as real muscle and silent, thin enough to wear as clothing."),
              ("NEUROSCIENCE", "Small currents behind the ear that make the balance organ feel acceleration, which ends motion sickness in virtual worlds."),
              ("MICROSYSTEMS", "Printed tactile sheets with a million independently moving points that survive sweat and washing."),
              ("COMPUTING", "Simulation of touch, cloth and impact that answers in under four milliseconds.")],
             "2057")
    if not s.wide:
        return s

    # floor plan, left
    px, py = lx, 300
    s.circ(px, py, 168, 0.95, 1.2)
    s.circ(px, py, 154, 0.5, 0.5)
    s.begin_clip_circle(px, py, 152)
    row, y = 0, py - 156
    while y < py + 156:
        x = px - 156 + (4.5 if row % 2 else 0)
        while x < px + 156:
            hot = ((x - px - 2) / 46.0) ** 2 + ((y - py - 8) / 60.0) ** 2 < 1
            s.dot(x, y, 1.5 if hot else 1.0, 0.95 if hot else 0.4, ARC if hot else WHITE)
            x += 9
        y += 7.8
        row += 1
    s.end_clip()
    for fx, fy in ((px - 16, py - 6), (px + 18, py + 20)):
        s.ellipse(fx, fy, 9, 22, a=0.95, w=1.0)
    s.arrow(px + 50, py + 40, px + 50, py - 40, 0.9, 0.8, head=7)
    s.arrow(px - 56, py - 40, px - 56, py + 40, 0.9, 0.8, head=7, color=ARC)
    for d in (90, 210, 330):
        x, y = polar(px, py, 182, d)
        s.rect(x - 7, y - 7, 14, 14, 0.9, 0.8, fill=0.3)
    s.view_label(px, py + 225, "B", "FLOOR PLAN", "Ø 3 m / 18 000 DRIVEN ROLLERS")

    # tactile skin in section, right
    qx, qy = rx, 330
    s.detail_ring(qx, qy, 170)
    s.begin_clip_circle(qx, qy, 169)
    for yy, a_ in ((qy - 70, 0.8), (qy - 58, 0.4)):
        s.ln(qx - 180, yy, qx + 180, yy, a_, 0.8)
    pressed = (2, 3, 6)
    for k in range(9):
        x = qx - 164 + k * 40
        s.rect(x, qy - 54, 32, 44, 0.85, 0.7, fill=0.06)
        down = 26 if k in pressed else 6
        s.rect(x + 10, qy - 10, 12, down, 0.95, 0.8, fill=0.6 if k in pressed else 0.15, color=ARC if k in pressed else WHITE)
    skin = []
    for x in range(int(qx - 180), int(qx + 181), 4):
        dip = sum(14 * math.exp(-(((x - (qx - 164 + k * 40 + 16)) / 12.0) ** 2)) for k in pressed)
        skin.append((x, qy + 6 + dip))
    s.poly(skin, 0.95, 1.2, close=False)
    for d in range(1, 5):
        s.poly([(x, y + d * 22) for x, y in skin], 0.3 - d * 0.05, 0.5, close=False)
    s.end_clip()
    s.text("SUIT", qx - 150, qy - 80, 6.5, a=0.6)
    s.text("SKIN", qx - 150, qy + 120, 6.5, a=0.6)
    s.ln(qx + 60, qy + 140, qx + 120, qy + 140, 0.9, 1.0)
    s.text("1 mm", qx + 90, qy + 132, 6.5, a=0.8, align="c")
    s.view_label(qx, qy + 210, "C", "TACTILE SKIN", "SECTION / THREE POINTS PRESSING")

    s.chart(rx - 170, 600, 260, 150, "ARM RESISTANCE, PUSHING A DOOR",
            lambda t: 0.06 + 0.8 / (1 + math.exp(-(t - 0.3) * 24)) - 0.35 / (1 + math.exp(-(t - 0.75) * 30)), "0 – 2 s", "N·m")
    s.table(rx - 170, s.H - 190, [
        ("TACTILE POINTS", "1.2 × 10⁶"), ("TOUCH DELAY", "4 ms"), ("ELBOW TORQUE", "60 N·m"),
        ("SUIT MASS", "3.8 kg"), ("FLOOR", "Ø 3 m"),
    ], key_w=114)
    return s


# ---------------------------------------------------------------------------
# 10  Aroma organ
# ---------------------------------------------------------------------------

def aroma_organ(size):
    s = start(size, 10, 1010)
    mx, my, lx, rx = centres(s)
    my -= 30
    s.begin_main(mx, my)
    framing(s, mx, my, 478, a0=200, thick=(140, 175), thin=(10, 50))

    s.circ(mx, my, 388, 0.95, 1.3, fill=0.03)
    s.circ(mx, my, 398, 0.4, 0.5)
    active = {3, 11, 12, 27, 40, 41, 58, 66, 79, 80, 91}
    for i in range(96):
        outer = i % 2 == 0
        r_c, r_b = (338, 13) if outer else (292, 11)
        d = i * 3.75
        x, y = polar(mx, my, r_c, d)
        on = i in active
        s.ln(*polar(mx, my, r_c - r_b, d), *polar(mx, my, 152, d), 0.85 if on else 0.13, 0.7 if on else 0.4, color=ARC if on else WHITE)
        s.circ(x, y, r_b, 0.9, 0.8, fill=0.5 if on else 0.05, color=ARC if on else WHITE)
        s.arc(x, y, r_b - 4, d + 90, d + 90 + 200 + (i * 37) % 120, 0.5, 0.5)
        vx, vy = polar(mx, my, 250, d)
        s.c.save()
        s.c.translate(vx, vy)
        s.c.rotate(math.radians(d))
        s.rect(-5, -2.5, 10, 5, 0.9, 0.5, fill=0.9 if on else 0.1, color=ARC if on else WHITE)
        s.c.restore()
    s.circ(mx, my, 250, 0.2, 0.45, dash=[1.5, 4])
    s.circ(mx, my, 152, 0.9, 0.9)
    s.circ(mx, my, 144, 0.4, 0.5)

    # mixing chip with a serpentine channel
    s.rect(mx - 84, my - 84, 168, 168, 0.95, 1.1, fill=0.08)
    for k in range(8):
        d = k * 45 + 22.5
        s.ln(*polar(mx, my, 144, d), *polar(mx, my, 100, d), 0.8, 0.7, color=ARC)
    pts = []
    for row in range(9):
        y = my - 68 + row * 17
        xs = (mx - 68, mx + 68) if row % 2 == 0 else (mx + 68, mx - 68)
        pts += [(xs[0], y), (xs[1], y)]
    s.poly(pts, 0.8, 0.8, close=False, color=ARC)
    s.circ(mx, my, 34, 0.9, 0.9, dash=[4, 3], color=GOLD)
    s.circ(mx, my, 22, 0.95, 1.1, fill=0.35)
    s.circ(mx, my, 9, 0.9, 0.7)

    # clearing fan and scrubber, below
    s.rect(mx - 130, my + 384, 260, 84, 0.95, 1.1, fill=0.05)
    fx, fy = mx - 70, my + 428
    s.circ(fx, fy, 32, 0.9, 0.9)
    for k in range(6):
        s.bez(polar(fx, fy, 6, k * 60), polar(fx, fy, 16, k * 60 + 12), polar(fx, fy, 26, k * 60 + 30), polar(fx, fy, 30, k * 60 + 48), 0.7, 0.7)
    s.circ(fx, fy, 6, 0.9, 0.7, fill=0.3)

    def scrub():
        s.c.rectangle(mx - 10, my + 398, 120, 56)
    s.hatch(scrub, 5, 45, 0.45, color=GOLD)
    s.hatch(scrub, 5, -45, 0.45, color=GOLD)
    s.rect(mx - 10, my + 398, 120, 56, 0.9, 0.8, color=GOLD)
    s.arrow(mx - 170, my + 428, mx - 134, my + 428, 0.7, 0.7, head=6)
    s.arrow(mx + 134, my + 428, mx + 176, my + 428, 0.7, 0.7, head=6)

    s.leader(*polar(mx, my, 338, 12 * 3.75), 120, 60, 110, "BASE ODORANT", "96 CARTRIDGES / 6 MONTHS EACH")
    s.leader(*polar(mx, my, 250, 300), 260, -70, 110, "VALVE RING", "DOSES OF 5 pl")
    s.leader(*polar(mx, my, 152, 330), 330, -40, 110, "MANIFOLD", None)
    s.leader(mx + 60, my + 60, 380, 130, 110, "MIXING CHIP", "NEW BLEND 12 TIMES A SECOND")
    s.leader(mx - 16, my - 16, -330, -300, -110, "HEATED OUTLET", "TO THE NOSE PIECE OR THE ROOM DUCT")
    s.leader(fx - 20, fy + 10, -190, 30, -110, "CLEARING FAN", None)
    s.leader(mx + 100, my + 440, 170, 30, 110, "SCRUBBER", "DESTROYS THE LAST SMELL IN 0.4 s")
    s.dim(mx - 388, my - 440, mx + 388, my - 440, "Ø 310 mm", a=0.4)
    s.end_main()

    s.legend("AROMA ORGAN", "MODEL AO-96   /   SMELL AND FLAVOUR ON CUE",
             "Plays smells the way a speaker plays sound. It blends 96 base odorants into any of two million "
             "smells, switches in a tenth of a second and clears the air before the next. For cinema, games and kitchens.",
             [("SENSORY BIOLOGY", "A full map from the 400 human smell receptors to what people say they smell, so any odour can be written down as a recipe."),
              ("CHEMISTRY", "A palette of 96 safe base odorants that covers nearly the whole map, the way three colours cover sight."),
              ("MICROFLUIDICS", "Valves that meter picolitre doses, and a mixer that changes the blend twelve times a second."),
              ("CATALYSIS", "A room-temperature catalyst that destroys the last smell in under half a second, so scenes can change.")],
             "2050")
    if not s.wide:
        return s

    # side section, left
    s.rect(lx - 190, 270, 380, 100, 0.95, 1.2, fill=0.04)
    for sgn in (-1, 1):
        for k in range(8):
            x = lx + sgn * (64 + k * 15) - 5
            s.rect(x, 282, 10, 70, 0.8, 0.6, fill=0.4 if (k * 3 + (sgn > 0)) % 5 == 0 else 0.05,
                   color=ARC if (k * 3 + (sgn > 0)) % 5 == 0 else WHITE)
    s.rect(lx - 46, 318, 92, 34, 0.95, 0.9, fill=0.10)
    s.ln(lx - 190, 360, lx + 190, 360, 0.5, 0.5)
    s.rect(lx - 9, 232, 18, 86, 0.9, 0.8, fill=0.08)
    s.rect(lx - 16, 244, 32, 14, 0.9, 0.7, color=GOLD)
    for k in range(-5, 6):
        s.fade_ln(lx + k * 1.5, 232, lx + k * 15, 120, 0.7, 0.0, 0.6, ARC)
    s.rect(lx - 70, 370, 140, 46, 0.9, 0.9, fill=0.05)
    s.ellipse(lx - 30, 393, 26, 7, a=0.8, w=0.7)
    s.view_label(lx, 470, "B", "SECTION", "CARTRIDGES, MIXER, HEATED OUTLET, FAN")

    # receptor pattern, right
    n, cell = 20, 15
    gx, gy = rx - n * cell / 2, 330 - n * cell / 2
    for i in range(n):
        for j in range(n):
            v = s.rng.random()
            a_ = 0.85 * s.rng.random() ** 0.5 if v > 0.9 else 0.10 * v
            s.rect(gx + i * cell + 1, gy + j * cell + 1, cell - 2, cell - 2, 0.18, 0.35, fill=a_, color=ARC)
    s.rect(gx - 4, gy - 4, n * cell + 8, n * cell + 8, 0.7, 0.7)
    s.view_label(rx, 330 + n * cell / 2 + 50, "C", "RECEPTOR PATTERN", '"ORANGE PEEL" ACROSS 400 HUMAN RECEPTORS')

    s.chart(rx - 170, 600, 260, 150, "ONE SMELL, ON AND OFF",
            lambda t: 0.04 + 0.9 / (1 + math.exp(-(t - 0.22) * 70)) / (1 + math.exp((t - 0.72) * 40)), "0 – 2 s", "")
    s.table(rx - 170, s.H - 190, [
        ("BASE ODORANTS", "96"), ("SMELLS IT CAN MAKE", "2 × 10⁶"), ("ONSET", "80 ms"),
        ("CLEARING", "400 ms"), ("SMALLEST DOSE", "5 pl"),
    ], key_w=130)
    return s


# ---------------------------------------------------------------------------
# 11  Bounder
# ---------------------------------------------------------------------------

def spindle(s, p1, p2, off, width, color=ARC):
    """A muscle bundle beside a limb: a lens shape, hatched along its length."""
    ang = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    nx, ny = -math.sin(ang), math.cos(ang)
    a_ = (p1[0] + (p2[0] - p1[0]) * 0.12 + nx * off, p1[1] + (p2[1] - p1[1]) * 0.12 + ny * off)
    b_ = (p1[0] + (p2[0] - p1[0]) * 0.88 + nx * off, p1[1] + (p2[1] - p1[1]) * 0.88 + ny * off)

    def ctrl(f, k):
        return (a_[0] + (b_[0] - a_[0]) * f + nx * width * k, a_[1] + (b_[1] - a_[1]) * f + ny * width * k)
    for k in (-1.0, -0.5, 0.0, 0.5, 1.0):
        s.bez(a_, ctrl(0.3, k), ctrl(0.7, k), b_, 0.9 if abs(k) == 1 else 0.45, 0.9 if abs(k) == 1 else 0.5, color=color)
    return a_, b_


def bounder(size):
    s = start(size, 11, 1111)
    mx, my, lx, rx = centres(s)
    s.begin_main(mx, my)
    framing(s, mx, my - 30, 478, a0=330, thick=(190, 232), thin=(120, 160))
    g = my + 330
    H, K, A = (mx - 10, my - 250), (mx + 84, my - 36), (mx + 18, my + 172)
    T = (mx + 124, g - 6)

    s.ln(mx - 430, g, mx + 430, g, 0.8, 0.9)
    for k in range(-21, 22):
        s.ln(mx + k * 20, g, mx + k * 20 - 9, g + 11, 0.3, 0.45)

    # the athlete, dashed
    for p1, p2, ry in ((H, K, 48), (K, A, 35)):
        ang = math.degrees(math.atan2(p2[1] - p1[1], p2[0] - p1[0]))
        s.ellipse((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2, math.hypot(p2[0] - p1[0], p2[1] - p1[1]) / 2 + 8, ry,
                  rot=ang, a=0.3, w=0.6, dash=[5, 4])
    s.poly([(A[0] - 28, A[1] + 4), (A[0] + 74, A[1] + 34), (A[0] + 80, A[1] + 52), (A[0] - 28, A[1] + 52)], 0.3, 0.6, dash=[5, 4])
    s.poly([(mx - 86, my - 330), (mx - 74, my - 450)], 0.3, 0.6, close=False, dash=[5, 4])
    s.poly([(mx + 70, my - 330), (mx + 78, my - 450)], 0.3, 0.6, close=False, dash=[5, 4])

    # belt and pack
    s.rect(mx - 96, my - 332, 176, 58, 0.95, 1.1, fill=0.07)
    s.rect(mx - 168, my - 356, 68, 118, 0.95, 1.1, fill=0.06)
    for k in range(1, 6):
        s.ln(mx - 162, my - 356 + k * 19, mx - 106, my - 356 + k * 19, 0.4, 0.45)
    s.rect(mx - 158, my - 350, 20, 10, 0.9, 0.5, fill=0.8, color=ARC)
    s.bez((mx - 134, my - 356), (mx - 130, my - 420), (mx - 90, my - 440), (mx - 76, my - 450), 0.4, 0.6, dash=[5, 4])

    # frame, muscles, joints
    limb(s, H, K, 13, 11, fill=0.07)
    limb(s, K, A, 11, 9, fill=0.07)
    f1 = spindle(s, H, K, 36, 13)
    f2 = spindle(s, H, K, -36, 13)
    f3 = spindle(s, K, A, 30, 11)
    for a_, b_ in (f1, f2):
        s.ln(a_[0], a_[1], H[0], H[1] + 10, 0.6, 0.5, color=ARC)
        s.ln(b_[0], b_[1], K[0], K[1] - 6, 0.6, 0.5, color=ARC)
    s.ln(f3[0][0], f3[0][1], K[0], K[1] + 8, 0.6, 0.5, color=ARC)
    s.ln(f3[1][0], f3[1][1], A[0], A[1] - 6, 0.6, 0.5, color=ARC)
    cuff(s, H, K, 0.30, 0.40, 58, fill=0.10)
    ang = math.atan2(K[1] - H[1], K[0] - H[0])
    for k in range(-5, 6):
        bx = H[0] + (K[0] - H[0]) * 0.35 - math.sin(ang) * k * 10
        by = H[1] + (K[1] - H[1]) * 0.35 + math.cos(ang) * k * 10
        s.dot(bx, by, 1.6, 0.95, GOLD)
    s.circ(H[0], H[1], 33, 0.95, 1.2, fill=0.10)
    s.circ(H[0], H[1], 23, 0.9, 1.6, dash=[5, 3], color=ARC)
    s.dot(H[0], H[1], 4, 0.95)
    s.circ(K[0], K[1], 27, 0.95, 1.2, fill=0.10)
    s.circ(K[0], K[1], 45, 0.5, 0.6, dash=[4, 3])
    s.dot(K[0], K[1], 4, 0.95)
    s.circ(A[0], A[1], 20, 0.95, 1.1, fill=0.10)
    s.dot(A[0], A[1], 3, 0.95)

    # spring blade
    s.bez((A[0] - 4, A[1] + 18), (mx - 116, my + 236), (mx - 44, g - 2), T, 0.95, 1.3)
    s.bez((A[0] + 10, A[1] + 22), (mx - 94, my + 244), (mx - 34, g - 14), (T[0] - 4, T[1] - 10), 0.95, 1.3)
    s.ln(T[0], T[1], T[0] - 4, T[1] - 10, 0.95, 1.2)
    s.rect(T[0] - 46, g - 6, 60, 6, 0.9, 0.7, fill=0.5)
    for k in range(1, 8):
        s.ln(T[0] - 46 + k * 7.5, g - 6, T[0] - 46 + k * 7.5, g, 0.4, 0.4)

    s.leader(mx - 134, my - 300, -130, -60, -110, "PACK", "CELLS AND CONTROLLER / 2.2 kg")
    s.leader(H[0] + 22, H[1] - 10, 230, -80, 110, "HIP DRIVE", None)
    s.leader(f1[0][0] * 0.5 + f1[1][0] * 0.5 - 12, f1[0][1] * 0.5 + f1[1][1] * 0.5 + 6, -230, 10, -110, "NERVE-SIGNAL CUFF",
             "READS THE COMMAND 60 ms EARLY")
    s.leader(f2[0][0] * 0.4 + f2[1][0] * 0.6, f2[0][1] * 0.4 + f2[1][1] * 0.6, 200, -30, 110, "MUSCLE BUNDLE", "NANOTUBE YARN / 3 PER LEG")
    s.leader(K[0] + 40, K[1] + 20, 150, 30, 100, "KNEE CAM", "VARIABLE LEVERAGE")
    s.leader(A[0] - 16, A[1] + 10, -220, -10, -110, "ANKLE PIVOT", None)
    s.leader(mx - 58, my + 262, -190, 20, -110, "SPRING BLADE", "RETURNS 96 % OF THE LANDING")
    s.leader(T[0] - 10, g - 3, 170, -50, 110, "SOLE", "SPIKED OR FLAT")
    s.dim(mx + 440, g, mx + 440, my - 332, "1.18 m", a=0.4)
    s.dim(mx - 330, g + 44, T[0], g + 44, "STRIDE 5.8 m", a=0.4)
    s.end_main()

    s.legend("BOUNDER", "MODEL B-4   /   POWERED LEGS FOR AUGMENTED ATHLETICS",
             "Powered legs for a new class of athletics. A runner reaches 62 km/h and clears a six-metre bar. "
             "The legs follow the athlete's own nerve signals, so the athlete still does the running.",
             [("MATERIALS SCIENCE", "Artificial muscle spun from carbon nanotube yarn: forty times the power of human muscle per kilogram, good for a hundred million strokes."),
              ("NEURAL ENGINEERING", "Sensors on the skin that read the nerve command to a muscle 60 ms before it moves, with no implant."),
              ("BIOMECHANICS", "Control that keeps the load on knees and spine below what an unaided sprinter takes."),
              ("COMPOSITES", "Spring blades that give back 96 % of each landing for a million cycles without cracking.")],
             "2064")
    if not s.wide:
        return s

    # high jump, with and without, left
    gy = 470
    s.ln(lx - 200, gy, lx + 200, gy, 0.8, 0.9)
    ax = lx - 190
    s.ln(ax, gy, ax, gy - 335, 0.5, 0.6)
    for m_ in range(0, 7):
        s.ln(ax, gy - m_ * 50, ax + (8 if m_ % 2 == 0 else 4), gy - m_ * 50, 0.6, 0.5)
        if m_ % 2 == 0:
            s.text(f"{m_} m", ax - 8, gy - m_ * 50 + 3, 6.5, a=0.7, align="r")
    for bx, h, half, col, lab, sub in ((lx - 80, 2.45, 46, WHITE, "2.45 m", "UNAIDED RECORD"), (lx + 90, 6.2, 70, ARC, "6.2 m", "WITH B-4")):
        top = gy - h * 50
        for sgn in (-1, 1):
            s.ln(bx + sgn * 26, gy, bx + sgn * 26, top - 8, 0.7, 0.7)
        s.ln(bx - 30, top, bx + 30, top, 0.95, 1.4, color=col)
        arc_pts = [(bx + u * half, top - 12 + (gy - top + 12) * u * u) for u in [i / 20.0 - 1 for i in range(41)]]
        s.poly(arc_pts, 0.7, 0.8, close=False, dash=[4, 3], color=col)
        s.text(lab, bx + 36, top + 2, 7.5, a=0.9, color=col)
        s.text(sub, bx + 36, top + 14, 6, a=0.5)
    s.view_label(lx, 520, "B", "HIGH JUMP", "THE SAME ATHLETE, WITHOUT AND WITH")

    # muscle yarn, right
    qx, qy = rx, 330
    s.detail_ring(qx, qy, 170)
    s.begin_clip_circle(qx, qy, 169)
    s.c.save()
    s.c.translate(qx, qy)
    s.c.rotate(math.radians(-28))
    for strand in range(6):
        pts = []
        for x in range(-200, 201, 3):
            y = 46 * math.sin(x / 38.0) + 15 * math.sin(x / 7.0 + strand * math.pi / 3)
            pts.append((x, y))
        s.poly(pts, 0.85 if strand % 2 == 0 else 0.5, 0.9, close=False, color=ARC if strand % 2 == 0 else WHITE)
    for off in (-64, 64):
        s.poly([(x, off + 46 * math.sin(x / 38.0)) for x in range(-200, 201, 4)], 0.25, 0.5, close=False, dash=[3, 3])
    s.c.restore()
    s.end_clip()
    s.ln(qx - 120, qy + 140, qx - 60, qy + 140, 0.9, 1.0)
    s.text("50 µm", qx - 90, qy + 132, 6.5, a=0.8, align="c")
    s.view_label(qx, qy + 210, "C", "MUSCLE YARN", "TWISTED, THEN COILED / SHORTENS WHEN CHARGED")

    def force(t):
        u = (t * 2.5) % 1.0
        return 0.04 + (0.9 * math.sin(math.pi * u / 0.34) if u < 0.34 else 0.0)
    s.chart(rx - 170, 600, 260, 150, "FORCE ON THE GROUND", force, "2.5 STRIDES", "kN")
    s.table(rx - 170, s.H - 190, [
        ("TOP SPEED", "62 km/h"), ("HIGH JUMP", "6.2 m"), ("PEAK POWER", "9 kW PER LEG"),
        ("MASS", "4.1 kg PER LEG"), ("RUN TIME", "45 min"),
    ], key_w=104)
    return s


SHEETS = [
    ("07-sky-racer", sky_racer),
    ("08-volumetric-stage", volumetric_stage),
    ("09-presence-rig", presence_rig),
    ("10-aroma-organ", aroma_organ),
    ("11-bounder", bounder),
]
