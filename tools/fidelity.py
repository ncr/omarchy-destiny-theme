"""Authored contours and construction details, in the original design units.

No raster sources or generated lettering. Each assembly has its own detail
pass; fasteners, seams and section lines follow the geometry they describe.
"""

import math
from sheet import WHITE, ARC, GOLD, polar

# Warm optical targets remain recognizable across the original sheet palettes.
TARGET = (.93, .73, .34)


def optical_target(s, x, y, r=7, angle=0):
    """Four alternating quadrants used as an optical tracking motif."""
    c=s.c
    c.new_path()
    c.arc(x,y,r,0,math.tau)
    s.knockout()
    s._stroke(.8,.55,None,TARGET)
    for k in (0,2):
        a=math.radians(angle+k*90)
        c.move_to(x,y)
        c.arc(x,y,r-.9,a,a+math.pi/2)
        c.close_path()
        s._ink(.78,TARGET)
        c.fill()
    s.ln(x-r,y,x+r,y,.5,.35,color=TARGET)
    s.ln(x,y-r,x,y+r,.5,.35,color=TARGET)
    s.circ(x,y,r+1.9,.27,.4)


def dummy_pivot(s, x, y, r=8, target=False):
    """A recessed pivot cap; a few caps also carry tracking targets."""
    s.circ(x,y,r,.55,.55)
    s.arc(x,y,r+2,35,145,.3,.4)
    s.arc(x,y,r+2,215,325,.3,.4)
    if target:
        optical_target(s,x,y,r*.65)
    else:
        s.circ(x,y,r*.36,.65,.45,color=TARGET)
        s.ln(x-r*.2,y,x+r*.2,y,.55,.4)


def dummy_side_shell(s):
    """Shell parting lines and joint covers, in seated-figure coordinates."""
    for x,y,r,target in ((5,61,10,True),(21,128,7,False),
                          (3,185,11,True),(120,199,10,True),(121,321,6,False)):
        dummy_pivot(s,x,y,r,target)
    # Back/abdomen interface, pelvic shell and removable shin cover.
    s.bez((-24,143),(-11,148),(10,148),(28,143),.5,.55)
    s.bez((-24,147),(-11,152),(10,152),(28,147),.25,.4)
    s.bez((-21,196),(-12,204),(13,202),(28,198),.45,.5)
    s.bez((36,177),(57,178),(86,181),(103,186),.4,.45)
    contour(s,[("M",121,243),("C",117,261,118,287,119,304),
        ("L",126,302),("C",125,286,130,261,130,245)],a=.38,w=.45,close=True)
    for yy in (249,298):
        bolt(s,123,yy,1.4,.5)
    for k in range(4):
        s.ln(-25+k*2.1,114,-25+k*2.1,126,.5,.65,color=TARGET)


def dummy_front_shell(s):
    """Thoracic jacket seams, shoulder caps and a sternum tracking target."""
    for sign in (-1,1):
        dummy_pivot(s,sign*44,62,7,False)
        dummy_pivot(s,sign*48,120,5,False)
        s.bez((sign*24,57),(sign*19,69),(sign*20,91),(sign*23,105),.4,.45)
        for yy in (61,103):
            bolt(s,sign*20,yy,1.25,.5)
    s.bez((-27,110),(-12,115),(12,115),(27,110),.5,.5)
    s.bez((-27,114),(-12,119),(12,119),(27,114),.25,.4)
    optical_target(s,0,77,7)
    for k in range(4):
        s.ln(-7+k*3,96,-7+k*3,102,.5,.65,color=TARGET)


def contour(s, commands, a=.85, w=.85, fill=0, close=False, color=WHITE):
    c = s.c
    c.new_path()
    for op, *v in commands:
        {"M": c.move_to, "L": c.line_to, "C": c.curve_to}[op](*v)
    if close:
        c.close_path()
    if fill:
        s.knockout()
        s._ink(fill, color)
        c.fill_preserve()
    s._stroke(a, w, None, color)


def bolt(s, x, y, r=2.4, a=.65):
    s.circ(x, y, r, a, .45)
    s.poly([polar(x, y, r*.53, k*60+30) for k in range(6)], a, .35)


def bearing(s, x, y, r, n=8):
    for rr, aa in ((r*.94, .7), (r*.77, .45), (r*.36, .75), (r*.23, .4)):
        s.circ(x, y, rr, aa, .5)
    for k in range(n):
        bolt(s, *polar(x, y, r*.59, k*360/n), min(2, r*.075))
    s.arc(x, y, r*.85, 205, 290, .7, .8, color=ARC)


def panel(s, x, y, w, h, vents=0):
    s.rect(x, y, w, h, .5, .5)
    for xx in (x+4, x+w-4):
        for yy in (y+4, y+h-4):
            bolt(s, xx, yy, 1.45)
    for k in range(vents):
        yy = y+10+k*4
        if yy < y+h-7:
            s.ln(x+10, yy, x+w-10, yy, .45, .65)


def cable(s, p0, p1, p2, p3, spacing=2.4):
    for off in (-spacing/2, spacing/2):
        s.bez((p0[0]+off,p0[1]), (p1[0]+off,p1[1]),
              (p2[0]+off,p2[1]), (p3[0]+off,p3[1]), .52, .45)


def dummy_neck(s, left, right, top):
    """Recessed neck shaft with separate curved elastomer/metal collars."""
    contour(s,[("M",left+2,top),("L",right-2,top),
        ("L",right-2,37),("L",left+2,37)],a=.48,w=.5,fill=.008,close=True)
    for yy in range(top+2,36,5):
        contour(s,[("M",left,yy),("C",left+5,yy+1.8,right-5,yy+1.8,right,yy),
            ("L",right,yy+2),("C",right-5,yy+3.8,left+5,yy+3.8,left,yy+2)],
            a=.58,w=.5,fill=.02,close=True)


def head(s, x, y, scale=1, facing=1):
    """Smooth dummy shell; a single nose cue preserves the lateral reading."""
    s.c.save()
    s.c.translate(x, y)
    s.c.scale(scale*facing, scale)
    dummy_neck(s,-14,9,13)
    # A rigid head shell ends above the rear neck instead of blending into it.
    contour(s, [("M",-20,13),
        ("C",-27,3,-29,-10,-25,-22),("C",-21,-34,-7,-38,5,-35),
        ("C",17,-33,22,-24,22,-15),
        ("C",22,-7,25,-1,27,3),("L",22,6),
        ("C",22,17,17,23,9,26),
        ("C",5,27,2,26,0,22),("L",-4,13),("L",-20,13)],
        a=.73,w=.75,fill=.012,close=True)
    # One rear access-cap seam, subordinate to the blank shell and target.
    s.bez((-15,-33),(-21,-22),(-21,1),(-17,13),.37,.45)
    optical_target(s,-8,-3,8.5)
    s.c.restore()


def front_head(s, x, y, scale=1):
    """Featureless tapered shell with a tracking target and neck rings."""
    s.c.save()
    s.c.translate(x,y)
    s.c.scale(scale,scale)
    dummy_neck(s,-12,12,23)
    contour(s,[("M",0,24),("C",-17,24,-24,9,-24,-10),
        ("C",-24,-27,-15,-36,0,-36),
        ("C",15,-36,24,-27,24,-10),
        ("C",24,9,17,24,0,24)],a=.7,w=.75,fill=.012,close=True)
    optical_target(s,0,-23,6.2)
    s.c.restore()


def joint_chain(s, points):
    """Body-segment axes, subordinate to the external envelope."""
    s.poly(points,.24,.4,close=False,dash=[7,3,1,3],color=GOLD)
    for x,y in points:
        s.circ(x,y,2.6,.5,.45,color=GOLD)


def anatomical_segment(s, p1, p2, r1, r2, kind, a=.68, w=.75, ghost=False):
    """Asymmetric muscle envelope following proximal/distal joint landmarks."""
    dx, dy = p2[0]-p1[0], p2[1]-p1[1]
    length = math.hypot(dx,dy)
    if length == 0:
        return
    bulge, peak = {
        "upper-arm": (1.08,.38), "forearm": (1.15,.23),
        "thigh": (1.13,.28), "calf": (1.34,.32),
    }[kind]
    s.c.save()
    s.c.translate(*p1)
    s.c.rotate(math.atan2(dy,dx)-math.pi/2)
    c=s.c
    c.move_to(-r1,0)
    c.curve_to(-r1*bulge,length*peak,-r2*1.1,length*.74,-r2,length)
    c.curve_to(-r2*.45,length*1.015,r2*.45,length*1.015,r2,length)
    c.curve_to(r2*.92,length*.74,r1*(bulge+.12),length*peak,r1,0)
    c.curve_to(r1*.45,-length*.025,-r1*.45,-length*.025,-r1,0)
    c.close_path()
    if not ghost:
        s.knockout()
        s._ink(.012,WHITE)
        c.fill_preserve()
    s._stroke(a,w,[6,3] if ghost else None,WHITE)
    if not ghost:
        s.bez((r1*.5,length*.13),(r1*.8,length*peak),
              (r2*.35,length*.65),(r2*.45,length*.82),a*.35,.4)
    s.c.restore()


def hand(s, x, y, scale=1, rot=0, a=.72):
    """Relaxed grouped fingers and thumb web, rather than a splayed icon."""
    s.c.save()
    s.c.translate(x,y)
    s.c.rotate(math.radians(rot))
    s.c.scale(scale,scale)
    contour(s,[("M",-7,-12),("C",-7,-2,-10,3,-11,8),
        ("L",-18,21),("C",-19,25,-15,26,-12,22),("L",-7,15),
        ("C",-5,20,-4,34,-2,39),("C",-1,43,2,43,3,39),
        ("C",5,44,8,42,8,39),("C",12,40,13,36,12,32),
        ("C",16,32,17,29,15,23),("L",10,9),
        ("C",9,1,7,-4,7,-12)],a=a,w=.7,fill=.012)
    for xx,yy in ((2,24),(7,23),(11,22)):
        s.bez((xx,yy),(xx+1,yy+5),(xx+1,yy+10),(xx+1,yy+15),a*.45,.4)
    s.bez((-6,6),(-2,8),(2,9),(6,8),a*.4,.4)
    s.c.restore()


def seated(s, x, y, facing=1):
    """Seated lateral envelope with anatomically shaped trunk and lower leg.

    Landmarks share a floor at y+346 and table surface at y+133. This is an
    authored visual study, not a percentile-certified anthropometric model.
    """
    s.c.save()
    s.c.translate(x,y)
    s.c.scale(facing,1)
    # Chair is separate from the human contour, with a true supporting seat.
    contour(s,[("M",-42,346),("L",-42,91),("L",-36,91),
        ("L",-34,216),("L",86,216),("L",92,346)],a=.47,w=.7)
    s.rect(-34,210,118,6,.42,.55)
    s.ln(-42,283,89,283,.24,.4)
    head(s,0,0)
    # Far leg: offset enough to read the paired limbs in a lateral projection.
    contour(s,[("M",10,177),("C",47,177,91,177,109,190),
        ("C",122,202,125,218,121,239),("C",115,266,114,294,116,322),
        ("L",143,337),("C",150,341,151,345,144,346),
        ("L",104,346),("C",99,345,98,339,101,330),
        ("C",97,304,98,273,96,249),("L",90,216)],a=.3,w=.55)
    # Nape, scapula, lumbar hollow, supported pelvis, thigh, patella, calf, heel.
    contour(s,[("M",-14,35),("C",-24,43,-31,56,-32,76),
        ("C",-32,97,-28,115,-23,133),("C",-19,147,-21,160,-26,177),
        ("C",-33,195,-29,205,-15,209),("C",4,213,22,206,43,208),
        ("C",65,210,86,211,105,212),("C",106,226,110,236,110,246),
        ("C",108,274,110,300,112,325),("C",108,330,108,340,113,344),
        ("L",159,344),("C",166,343,164,338,157,336),
        ("C",142,332,137,323,132,320),("C",127,291,141,271,140,250),
        ("C",140,238,134,225,134,214),("C",139,199,132,185,119,180),
        ("C",91,170,56,170,33,169),("C",28,153,30,137,32,120),
        ("C",36,97,32,78,27,64),("C",24,49,16,44,9,37)],a=.73,w=.8,fill=.012)
    # Small internal landmarks describe anatomy rather than cloth folds.
    s.bez((-19,64),(-15,79),(-15,98),(-20,113),.3,.45)
    s.bez((1,176),(13,169),(23,173),(29,188),.32,.45)
    s.bez((114,194),(124,191),(131,200),(128,207),.32,.45)
    s.bez((126,238),(132,251),(125,269),(122,286),.27,.4)
    s.bez((116,320),(121,324),(128,326),(134,329),.27,.4)
    # Deltoid, upper arm, olecranon, forearm taper and supported wrist.
    contour(s,[("M",-6,52),("C",4,45,17,50,20,63),
        ("C",23,79,19,106,25,117),("C",43,117,63,117,83,122),
        ("L",85,133),("C",64,135,43,138,25,138),
        ("C",12,140,9,127,7,112),("C",3,94,-4,81,-7,69)],a=.73,w=.75,fill=.012)
    s.bez((1,63),(5,72),(8,89),(10,99),.28,.45)
    s.bez((22,130),(37,129),(56,128),(74,129),.25,.4)
    # Side-on hand resting on the tabletop, with overlapping fingers.
    contour(s,[("M",83,122),("C",92,121,100,120,106,123),
        ("L",117,127),("C",123,129,122,132,118,132),
        ("L",96,132),("L",85,133)],a=.7,w=.65,fill=.012)
    s.bez((98,126),(105,127),(111,128),(117,129),.35,.4)
    joint_chain(s,[(5,61),(21,128),(85,127)])
    joint_chain(s,[(5,61),(3,185),(120,199),(121,321)])
    # No numeric angle is invented: the arc indicates the shown pose only.
    s.arc(120,199,21,95,185,.28,.45,color=GOLD)
    dummy_side_shell(s)
    s.c.restore()


def diner(s,x,y,variant=0):
    """Neutral front elevation of a seated subject, cropped at table height."""
    s.c.save()
    s.c.translate(x,y)
    # Mild width differences express body variation without character design.
    s.c.scale((.95,1.04,1)[variant%3],1)
    front_head(s,0,0)
    contour(s,[("M",-12,33),("C",-18,43,-31,44,-44,50),
        ("C",-59,58,-62,76,-61,94),("L",-60,122),
        ("C",-65,128,-59,133,-49,133),("L",-21,132),
        ("C",-26,112,-24,95,-26,77),
        ("M",12,33),("C",18,43,31,44,44,50),
        ("C",59,58,62,76,61,94),("L",60,122),
        ("C",65,128,59,133,49,133),("L",21,132),
        ("C",26,112,24,95,26,77)],a=.7,w=.75)
    # Torso is a single closed silhouette behind the arms and table settings.
    contour(s,[("M",-12,33),("C",-18,43,-35,44,-43,51),
        ("C",-37,69,-31,89,-30,108),("L",-33,132),
        ("L",33,132),("L",30,108),("C",31,89,37,69,43,51),
        ("C",35,44,18,43,12,33)],a=.65,w=.7,fill=.01)
    for sign in (-1,1):
        s.bez((sign*11,36),(sign*12,48),(sign*17,53),(sign*27,55),.32,.45)
        s.bez((sign*6,57),(sign*16,53),(sign*27,54),(sign*34,58),.3,.45)
        s.bez((sign*30,68),(sign*41,67),(sign*45,72),(sign*44,81),.3,.45)
        s.poly([(sign*44,62),(sign*48,120),(sign*18,126)],.2,.4,close=False,dash=[5,3,1,3],color=GOLD)
        for px,py in ((sign*44,62),(sign*48,120)):
            s.circ(px,py,2.3,.43,.4,color=GOLD)
        s.bez((sign*52,119),(sign*39,120),(sign*30,125),(sign*20,125),.65,.65)
        s.bez((sign*20,125),(sign*12,121),(sign*6,129),(sign*2,130),.6,.55)
        s.ln(sign*3,132,sign*21,131,.45,.45)
    s.ln(0,43,0,112,.18,.4,dash=[8,3,1,3])
    dummy_front_shell(s)
    s.c.restore()


def dog(s,x,y):
    s.c.save(); s.c.translate(x,y)
    contour(s,[("M",-43,-8),("C",-62,-21,-66,-46,-59,-54),
        ("C",-79,-39,-70,-9,-49,2),("C",-49,13,-44,20,-39,24),
        ("L",-40,42),("L",-29,44),("C",-23,42,-30,39,-31,36),
        ("L",-25,19),("C",-7,27,14,20,25,17),
        ("L",30,41),("L",43,44),("C",50,40,38,39,38,35),
        ("L",39,12),("C",51,6,51,-6,56,-10),
        ("C",69,-8,81,-13,82,-18),("L",69,-25),
        ("C",65,-39,53,-39,47,-31),("C",37,-23,38,-17,31,-16),
        ("C",6,-24,-25,-24,-43,-8)],w=1.0,fill=.04,close=True)
    contour(s,[("M",51,-30),("C",37,-37,43,-7,51,-10),
        ("C",58,-14,57,-27,51,-30)],a=.8,w=.75)
    contour(s,[("M",-26,20),("L",-18,38),("L",-9,40)],a=.55,w=.65)
    contour(s,[("M",21,20),("L",19,38),("L",26,40)],a=.55,w=.65)
    s.dot(65,-26,1.5,.9); s.dot(80,-18,1.8,.8)
    s.bez((43,1),(49,3),(51,-2),(54,-7),.75,1,color=ARC)
    for k in range(10):
        s.bez((-37+k*5,-10),(-37+k*5,-16),(-29+k*5,-18),(-25+k*5,-16),.25,.4)
    s.c.restore()


def enrich(s, name, mx, my):
    """Details stay inside their parent assemblies and below annotations."""
    s.c.save(); s.c.translate(mx,my)
    if name == "truth-lamp":
        # Section through layered optical housing, heat sink and suspension.
        s.poly([(-34,-247),(34,-247),(111,-178),(-111,-178)],.45,.5)
        for k in range(-9,10):
            x=k*10
            yy=-241+abs(x)*.82
            s.ln(x,yy,x,-181,.34,.45)
        panel(s,-26,-231,52,23,2)
        for x in (-104,-78,-52,52,78,104):
            bolt(s,x,-175,2)
        for k in range(9):
            x=-108+k*27
            s.circ(x,-165.5,5.2,.65,.45)
            s.circ(x,-165.5,1.4,.8,.4,color=ARC)
        for y in range(-402,-251,9):
            s.ln(-2,y,2,y+2,.45,.4)
        for x in (-250,250):
            panel(s,x-6,109,12,24)
            s.ln(x-4,133,x-4,288,.3,.45)
        s.ln(-334,98,334,98,.45,.5)
        for k in range(5):
            x=-264+k*132
            s.ellipse(x,83,25,3,a=.45,w=.45)
            s.ellipse(x+46,43,10,2.3,a=.55,w=.5)
            s.ellipse(x+46,67,7,2,a=.5,w=.4)
            s.ellipse(x+46,85,8,1.5,a=.6,w=.45)
            s.ln(x-40,76,x-39,85,.7,.55)
            for j in range(4):
                s.ln(x-43+j*2,73,x-42+j*2,77,.6,.4)
    elif name == "quantum-simulator":
        # Formed coaxial service loops thermally anchored at every cold plate.
        for k in range(7):
            x=-102+k*13
            for yy in (-380,-290,-195,-105,-25):
                s.bez((x,yy),(x-12,yy+22),(x+18,yy+43),(x,yy+65),.5,.45,color=GOLD)
        for k in range(3):
            s.bez((180+k*5,-391),(222+k*5,-360),(194+k*5,-350),(184+k*5,-308),.55,.6)
        for y,hw in [(-390,230),(-300,210),(-205,186),(-115,160),(-35,140),(45,124)]:
            for sign in (-1,1):
                bolt(s,sign*(hw-8),y,3)
                s.rect(sign*(hw-20)-3,y+4,6,12,.55,.45)
            for x in range(-hw+30,hw-20,18):
                s.ln(x,y-3,x+4,y+3,.24,.4)
        for k in range(6):
            y=84+k*28
            for x in range(-74,42,7):
                s.rect(x,y-3,3,3,.6,.35,color=GOLD)
            panel(s,-67,y+2,24,6)
        panel(s,102,-464,87,49,7)
        for k in range(12):
            y=-369+k*5
            s.ellipse(-167,y,17,3,a=.5,w=.5,color=GOLD)
        cable(s,(-167,-307),(-202,-253),(-202,-165),(-147,-121))
        for y in range(-375,351,22):
            bolt(s,-235,y,1.7); bolt(s,235,y,1.7)
    elif name == "organ-foundry":
        for k in range(6):
            x=-150+k*60
            for y in (-400,-396,-392):
                s.ln(x-14,y,x+14,y,.6,.45)
            for y in range(-380,-348,5):
                s.ln(x+8,y,x+14,y,.5,.4)
            s.ellipse(x,-345,10,2,a=.6,w=.4)
        for x in range(-174,180,24):
            bolt(s,x,-282,1.7)
        panel(s,12,-294,68,24,2)
        for x in (-180,180):
            for y in range(-300,124,36):
                bolt(s,x,y,2)
        bearing(s,-190,218,24)
        panel(s,154,180,76,56,7)
        for k in range(20):
            s.ln(-125+k*4,191,-125+k*4,243,.3,.4)
        # Cartridge supply bundle, with individual routes to the moving head.
        for k in range(6):
            s.bez((-150+k*60,-327),(-140+k*60,-310),(20+k*4,-330),(26+k*5,-295),.4,.45,color=GOLD)
        for x in (-191,191):
            s.ln(x,-306,x,112,.45,.6)
            for y in (-300,106):
                s.rect(x-3,y,6,14,.6,.5)
    elif name == "tether-climber":
        for sign in (-1,1):
            for y in (-66,-6,54,114):
                bearing(s,sign*31,y,22,6)
            for y in range(-86,151,24):
                bolt(s,sign*126,y,2)
            for j in range(3):
                x=18 if sign>0 else -102
                y=-265+j*52
                for k in range(12):
                    s.ln(x+k*6,y+4,x+k*6,y+33,.34,.45)
        for x in range(-376,377,16):
            s.ln(x,258,x,269,.35,.4,color=ARC)
        for x in (-380,-300,-220,-140,140,220,300,380):
            bolt(s,x,265,2)
    elif name == "cortical-mesh":
        panel(s,-22,-22,44,44)
        for row in range(5):
            for col in range(5):
                s.rect(-15+col*6,-15+row*6,3.8,3.8,.42,.35,color=GOLD)
        for k in range(24):
            p=polar(0,0,68,k*15); q=polar(0,0,74,k*15)
            s.ln(*p,*q,.6,.5)
        for k in range(48):
            # Bond pads where each radial thread enters the sealed decoder.
            x,y=polar(0,0,82,k*7.5)
            s.ellipse(x,y,3,1.4,rot=k*7.5,a=.6,w=.4,color=GOLD)
        # Lithographic fan-out on the ceramic carrier, between die and coil.
        for side in range(4):
            s.c.save();s.c.rotate(side*math.pi/2)
            for k in range(9):
                x=-20+k*5
                s.poly([(x,-28),(x,-34),(x*1.6,-43),(x*1.6,-49)],.5,.4,close=False,color=GOLD)
                s.rect(x-1,-31,2,3,.6,.35)
            s.c.restore()
    elif name == "fusion-transport":
        panel(s,-492,-14,94,18,1)
        for k in range(3):
            for sign in (-1,1):
                x,y=-250+k*104,sign*62
                s.arc(x,y,43,25,150,.55,.55)
                bearing(s,x,y,8,4)
                for a in range(0,360,30):
                    s.ln(*polar(x,y,42,a),*polar(x,y,46,a),.6,.5)
        for x in range(414,605,28):
            for y in range(-39,40,6):
                s.ln(x,y,x+12,y,.4,.45)
            bolt(s,x+6,-42,2); bolt(s,x+6,42,2)
        for y in range(-168,169,20):
            panel(s,-369,y,24,13)
        for off in (-3,3):
            s.bez((350,off),(370,off),(366,76+off),(412,76+off),.6,.5)
        for sign in (-1,1):
            for k in range(5):
                s.bez((613,sign*(10+k*5)),(639,sign*(15+k*9)),(681,sign*(80+k*8)),(716,sign*(85+k*8)),.38,.45,color=GOLD)
            for x in range(-296,310,26):
                bolt(s,x,sign*11,1.3)
    elif name == "air-refinery":
        for y in range(-206,227,72):
            for sign in (-1,1):
                bolt(s,sign*56,y+15,2.4)
            s.circ(33,y+44,6,.7,.6)
            s.ln(33,y+44,36,y+40,.7,.5)
        for x in (-144,0,144):
            for off in (-5,0,5):
                s.ellipse(x,-378,33,7+off*.3,a=.38,w=.4)
            for dx in (-40,40):
                bolt(s,x+dx,-389,1.8)
        for x in range(-215,216,24):
            for y in (-358,-256):
                bolt(s,x,y,1.5)
        for x,r in ((176,46),(280,38)):
            y=314-r
            bearing(s,x,y,10,4)
            s.arc(x,y,r-4,190,330,.45,.5)
        cable(s,(65,250),(89,245),(92,302),(128,298))
    elif name == "sky-racer":
        for x,y,r in [(-215,-185,88),(215,-185,88),(-305,15,98),(305,15,98),(-215,215,88),(215,215,88)]:
            bearing(s,x,y,14,6)
            for k in range(18):
                a=k*20
                bolt(s,*polar(x,y,r-4,a),1.6)
            s.arc(x,y,r-13,195,320,.5,.45)
        for sign in (-1,1):
            s.bez((sign*21,-167),(sign*66,-113),(sign*52,58),(sign*28,140),.5,.55)
            for y in range(55,136,8):
                s.ln(sign*14,y,sign*28,y-3,.45,.45)
        panel(s,-15,145,30,15)
    elif name == "volumetric-stage":
        for sign in (-1,1):
            x=sign*412
            for y in range(-332,245,30):
                bolt(s,x-12,y,1.5); bolt(s,x+12,y,1.5)
            for k in range(5):
                y=-290+k*112
                s.ellipse(sign*376,y,3.5,5,a=.7,w=.6,color=ARC)
                for off in (-5,0,5):
                    s.ln(sign*391,y+off,sign*381,y+off,.5,.4)
            s.bez((x+sign*10,-338),(x+sign*22,-170),(x+sign*22,70),(x+sign*10,243),.4,.6)
        for x in range(-320,321,80):
            panel(s,x-10,240,20,7)
        for x in range(-400,401,40):
            s.ln(x,252,x,264,.4,.5)
    elif name == "presence-rig":
        panel(s,-18,-210,36,48)
        for sign in (-1,1):
            s.bez((sign*67,-236),(sign*80,-201),(sign*48,-150),(sign*48,-85),.65,.65)
            s.bez((sign*48,-85),(sign*36,-60),(sign*52,-50),(sign*56,-32),.5,.55)
            for k in range(7):
                y=-150+k*11
                s.bez((sign*10,y),(sign*18,y+4),(sign*26,y+4),(sign*37,y),.35,.45)
            for y in range(-366,263,32):
                bolt(s,sign*430,y,2)
            panel(s,sign*430-7,-170,14,60,9)
        s.ellipse(0,-300,28,25,a0=192,a1=348,a=.55,w=.5)
        for x in range(-380,381,20):
            s.circ(x,264,2,.5,.4)
        # Flexible textile around the clavicles, abdomen and pelvis.
        for sign in (-1,1):
            for k in range(4):
                s.bez((sign*12,-242+k*6),(sign*32,-247+k*6),(sign*55,-239+k*6),(sign*72,-230+k*6),.38,.5)
            s.bez((sign*10,-76),(sign*22,-86),(sign*50,-72),(sign*55,-45),.5,.65)
            for k in range(4):
                s.bez((sign*12,-65+k*6),(sign*25,-58+k*6),(sign*39,-62+k*5),(sign*46,-44+k*4),.3,.45)
        for x,y in ((-86,-236),(36,-30),(-50,104),(62,96)):
            optical_target(s,x,y,6)
        optical_target(s,0,-232,6.5)
    elif name == "aroma-organ":
        for k in range(96):
            a=k*3.75; r=338 if k%2==0 else 292
            x,y=polar(0,0,r,a)
            s.circ(x,y,9 if k%2==0 else 7,.5,.45)
            for off in (-2,2):
                p=polar(x,y,7,a+90+off*8);q=polar(x,y,7,a-90-off*8)
                s.ln(*p,*q,.3,.35)
        for k in range(24):
            bolt(s,*polar(0,0,375,k*15),2.8)
        for x in range(-72,73,12):
            for y in (-79,79):
                s.rect(x-2,y-2,4,4,.6,.45,color=GOLD)
        for x in range(-119,120,7):
            s.ln(x,398,x,458,.28,.4)
    elif name == "bounder":
        for x,y,r in ((-10,-250,31),(84,-36,25),(18,172,18)):
            bearing(s,x,y,r)
        optical_target(s,-10,-250,7)
        optical_target(s,84,-36,6)
        panel(s,-161,-349,54,101,14)
        for y in (-323,-306,-289):
            bolt(s,62,y,2)
        for off in range(-3,4):
            s.bez((10+off,191),(-81+off,210),(-84+off,278),(52+off,315),.25,.4)
        cable(s,(-127,-242),(-116,-195),(-43,-213),(-27,-239))
    elif name == "proxy":
        for x,y,r in ((34,-178,13),(104,-104,9),(-6,20,14),(112,96,11),(74,226,8)):
            bearing(s,x,y,r,6)
        for x,y,r in ((34,-178,6),(-6,20,6),(112,96,5)):
            optical_target(s,x,y,r)
        for sign in (-1,1):
            s.bez((16+sign*32,-158),(8+sign*45,-115),(sign*39,-61),(-4+sign*35,-8),.55,.55)
        for y in range(-156,-124,7):
            s.ln(10,y,37,y+6,.5,.5)
        cable(s,(120,115),(131,168),(95,193),(80,211))
        for k in range(8):
            s.ln(115+k*4,246+k*.3,113+k*4,251+k*.3,.6,.6)
    elif name == "greener":
        g=150
        for x,h,sgn in ((-64,318,1),(76,336,-1)):
            for y in range(g-h+24,g-12,40):
                s.rect(x-5,y,10,5,.6,.5)
                bolt(s,x,y+2.5,1.3)
            for k in range(6):
                xx=x+sgn*(k*4-6)
                s.ln(xx,g-h-13,xx,g-h-4,.55,.5)
            cable(s,(x+6,g-h+4),(x+15,g-h+30),(x+10,g-20),(x+15,g))
        for y in range(g-226,g-6,14):
            s.ln(-466,y,-390,y,.25,.45)
        for k in range(26):
            yy=g-20-k*5;xx=65+27*math.sin(k*1.7)
            s.bez((76,g),(62,yy+30),(xx,yy+4),(xx+14,yy),.25,.5)
            s.ellipse(xx+10,yy+2,8,2.8,rot=-25,a=.45,w=.45)
    else:
        raise ValueError(f"No construction pass for {name}")
    s.c.restore()
