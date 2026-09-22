"""Continuous human-factors envelopes for the wearable equipment plates."""
import math
from fidelity import contour, front_head, optical_target, bolt
from sheet import WHITE, ARC, GOLD


def absent_head(s,x,y):
    """Dashed head envelope and a cancellation stroke above a capped mount."""
    s.c.save();s.c.translate(x,y)
    c=s.c
    c.move_to(0,23)
    c.curve_to(-15,23,-23,9,-23,-8)
    c.curve_to(-23,-26,-14,-34,0,-34)
    c.curve_to(14,-34,23,-26,23,-8)
    c.curve_to(23,9,15,23,0,23)
    s._stroke(.64,.75,[4,3],WHITE)
    s.ln(-28,27,28,-38,.85,.9)
    # Symbol only. The physical neck is part of proxy_body's connected shell.
    s.c.restore()


def muscle_sleeve(s,p1,p2,r1,r2):
    """A longitudinal textile actuator with curved retaining cuffs."""
    dx,dy=p2[0]-p1[0],p2[1]-p1[1]
    length=math.hypot(dx,dy)
    s.c.save();s.c.translate(*p1);s.c.rotate(math.atan2(dy,dx)-math.pi/2)
    for k in range(5):
        x=(k-2)*2.5
        s.bez((x,length*.24),(x+2,length*.40),(x+1,length*.60),(x,length*.76),.43,.42,color=ARC)
    for t in (.22,.77):
        y=length*t;r=(r1*(1-t)+r2*t)*.93
        contour(s,[("M",-r,y),("C",-r*.4,y+4,r*.4,y+4,r,y),
            ("L",r,y+5),("C",r*.4,y+9,-r*.4,y+9,-r,y+5)],
            a=.65,w=.6,fill=.025,close=True,color=ARC)
        s.rect(r-4,y+1,5,4,.68,.4,fill=.09,color=ARC)
    s.c.restore()


def dummy_joint(s,p,r=12,target=False,a=.8):
    """Recessed load-cell cover and exposed steel pin, without gear ornament."""
    x,y=p
    s.circ(x,y,r,a,.7,fill=.025)
    s.arc(x,y,r-3,25,155,a*.55,.5)
    s.arc(x,y,r-3,205,335,a*.55,.5)
    if target:optical_target(s,x,y,r*.52)
    else:
        s.circ(x,y,r*.35,a*.8,.5)
        s.ln(x-r*.2,y,x+r*.2,y,a*.8,.4)


def dummy_segment(s,p1,p2,r1,r2,j1,j2,a=.8):
    """Moulded limb with recessed end sockets and a removable side cover."""
    dx,dy=p2[0]-p1[0],p2[1]-p1[1];length=math.hypot(dx,dy)
    s.c.save();s.c.translate(*p1);s.c.rotate(math.atan2(dy,dx)-math.pi/2)
    start,end=j1*.8,length-j2*.8
    # The narrow central member bridges each shell to the joint centre.
    s.rect(-4,0,8,length,a*.48,.45,fill=.008)
    contour(s,[("M",-r1*.77,start),
        ("C",-r1*1.07,start+16,-r1*1.05,length*.33,-r2*1.1,end-19),
        ("C",-r2*1.03,end-9,-r2,end-3,-r2*.8,end),
        ("C",-r2*.4,end+2,r2*.4,end+2,r2*.8,end),
        ("C",r2,end-3,r2*1.03,end-9,r2*1.1,end-19),
        ("C",r1*.98,length*.33,r1*1.02,start+16,r1*.77,start),
        ("C",r1*.4,start-2,-r1*.4,start-2,-r1*.77,start)],
        a=a,w=.8,fill=.02,close=True)
    s.bez((-r1*.72,start+6),(-r1*.3,start+9),(r1*.3,start+9),(r1*.72,start+6),a*.6,.5)
    s.bez((-r2*.74,end-5),(-r2*.3,end-2),(r2*.3,end-2),(r2*.74,end-5),a*.6,.5)
    s.bez((r1*.5,start+14),(r1*.7,length*.34),(r2*.53,end-23),(r2*.45,end-13),a*.43,.45)
    for x,y in ((r1*.5,start+15),(r2*.45,end-13)):bolt(s,x,y,1.45,a*.66)
    s.c.restore()


def dummy_foot(s,p,side=1,angle=0,a=.78):
    """One rigid 72 x 29 shoe; only rotation/reflection may differ by side."""
    x,y=p;s.c.save();s.c.translate(x,y);s.c.scale(side,1)
    s.c.rotate(math.radians(angle))
    contour(s,[("M",-10,-1),("L",10,-1),
        ("C",13,8,20,15,37,18),("C",49,20,58,21,58,25),
        ("L",58,28),("L",-12,28),("C",-14,26,-14,17,-12,11),("L",-10,-1)],
        a=a,w=.8,fill=.025,close=True)
    s.ln(-11,24,57,24,a*.6,.5)
    s.bez((1,9),(12,11),(23,17),(35,18),a*.45,.45)
    for x in (12,18,24):s.ln(x,15,x+2,19,a*.5,.45)
    dummy_joint(s,(0,0),8,False,a)
    s.c.restore()


def dummy_hand(s,p,angle=0,side=1,a=.78):
    """Rigid moulded hand envelope, grouped fingers and an integral thumb.

    The origin is the wrist pivot. Every instance shares this unscaled path;
    a mirrored casting or a different wrist angle does not alter its size.
    """
    s.c.save();s.c.translate(*p);s.c.rotate(math.radians(angle));s.c.scale(side,1)
    # A short metal spigot overlaps the wrist pivot and the moulded cuff.
    s.rect(-5,-2,10,12,a*.65,.5,fill=.025)
    contour(s,[("M",-7,7),("L",7,7),
        ("C",8,12,11,15,11,22),("L",10,33),
        ("C",10,37,7,39,3,39),("L",-3,38),
        ("C",-7,38,-9,35,-9,31),("L",-9,26),
        ("C",-13,28,-17,26,-16,22),
        ("C",-15,17,-10,14,-9,11),("L",-7,7)],
        a=a,w=.75,fill=.022,close=True)
    s.bez((-8,12),(-3,14),(3,14),(8,12),a*.55,.5)
    # One mould seam, without individual digits or anatomical palm creases.
    s.bez((7,19),(8,26),(7,33),(3,35),a*.35,.4)
    s.c.restore()


def dummy_foot_front(s,p,side=1,a=.78):
    """Front elevation of the shoe, with slight outward toe splay.

    The sole is 26 units below the ankle, at the roller crowns in Presence
    Rig. Both sides use the same casting, reflected across the body axis.
    """
    s.c.save();s.c.translate(*p);s.c.scale(side,1)
    contour(s,[("M",-9,-1),("L",9,-1),
        ("C",10,7,13,11,17,17),("L",20,21),
        ("C",22,24,20,26,17,26),("L",-14,26),
        ("C",-18,26,-19,23,-17,20),("L",-13,12),
        ("C",-11,8,-10,4,-9,-1)],a=a,w=.8,fill=.025,close=True)
    s.bez((-16,22),(-7,24),(9,24),(19,22),a*.6,.5)
    s.bez((-10,12),(-4,15),(6,15),(12,12),a*.45,.45)
    for y in (8,11):s.ln(-4,y,6,y,a*.5,.45)
    dummy_joint(s,(0,0),8,False,a)
    s.c.restore()


def paired_joint(root,tip,length1,length2,hint):
    """Two rigid links; choose the joint solution nearest the authored pose."""
    dx,dy=tip[0]-root[0],tip[1]-root[1];d=math.hypot(dx,dy)
    assert abs(length1-length2)<=d<=length1+length2
    along=(length1**2-length2**2+d*d)/(2*d)
    height=math.sqrt(max(0,length1**2-along**2))
    center=(root[0]+dx*along/d,root[1]+dy*along/d)
    candidates=[(center[0]-sign*dy*height/d,center[1]+sign*dx*height/d) for sign in (-1,1)]
    return min(candidates,key=lambda p:math.dist(p,hint))


# One component definition per type, used by BOTH sides of the running dummy.
# length, proximal radius, distal radius, proximal joint, distal joint
PROXY_PARTS={'upper_arm':(116,21,14,16,11),'forearm':(88,16,10,11,8),
             'thigh':(146,31,22,18,15),'calf':(140,23,12,15,8)}


def proxy_pose():
    sh=(34,-178);hip=(-6,20)
    pose={'shoulder':sh,'hip':hip}
    for side,wrist,ankle,elbow_hint,knee_hint in (
            ('far',(-108,-48),(-178,236),(-100,-140),(-64,138)),
            ('near',(172,-160),(74,226),(104,-104),(112,96))):
        pose[side]={'wrist':wrist,'ankle':ankle,
            'elbow':paired_joint(sh,wrist,PROXY_PARTS['upper_arm'][0],PROXY_PARTS['forearm'][0],elbow_hint),
            'knee':paired_joint(hip,ankle,PROXY_PARTS['thigh'][0],PROXY_PARTS['calf'][0],knee_hint),
            'foot_angle':12 if side=='near' else math.degrees(
                math.asin((300-ankle[1])/math.hypot(58,28))-math.atan2(28,58))}
        elbow=pose[side]['elbow']
        pose[side]['hand_angle']=math.degrees(math.atan2(wrist[1]-elbow[1],wrist[0]-elbow[0]))-90
    return pose


def presence_body(s,mx,my):
    """A front-view instrumented crash dummy wearing the original VR apparatus."""
    s.c.save();s.c.translate(mx,my)
    shoulders=((-86,-236),(86,-236));elbows=((-126,-118),(126,-118))
    wrists=((-150,-6),(150,-6));hips=((-36,-30),(36,-30))
    knees=((-50,104),(50,104));ankles=((-52,220),(52,220))
    for i in range(2):
        dummy_segment(s,shoulders[i],elbows[i],21,15,16,11)
        dummy_segment(s,elbows[i],wrists[i],17,11,11,8)
        dummy_segment(s,hips[i],knees[i],32,23,17,16)
        dummy_segment(s,knees[i],ankles[i],24,12,16,8)
        for p,r,t in ((shoulders[i],16,True),(elbows[i],11,False),
                      (knees[i],16,True),(wrists[i],8,False)):
            dummy_joint(s,p,r,t)
        dummy_foot_front(s,ankles[i],side=-1 if i==0 else 1)
    # Visible flexible lumbar member connects the rib jacket to the pelvic casting.
    contour(s,[("M",-37,-119),("L",37,-119),("L",38,-59),("L",-38,-59)],
        a=.55,w=.6,fill=.01,close=True)
    for y in range(-112,-61,8):
        s.bez((-38,y),(-15,y+5),(15,y+5),(38,y),.49,.55)
    # One rib-jacket shell, shaped shoulders, lower edge above the lumbar bellows.
    contour(s,[("M",-15,-258),("L",15,-258),
        ("C",28,-255,44,-251,59,-249),("C",77,-247,82,-240,83,-228),
        ("C",76,-213,71,-199,69,-181),("C",65,-149,60,-126,49,-112),
        ("C",29,-106,-29,-106,-49,-112),
        ("C",-60,-126,-65,-149,-69,-181),
        ("C",-71,-199,-76,-213,-83,-228),
        ("C",-82,-240,-77,-247,-59,-249),("C",-44,-251,-28,-255,-15,-258)],
        a=.89,w=.95,fill=.022,close=True)
    for sign in (-1,1):
        s.bez((sign*14,-248),(sign*34,-242),(sign*51,-246),(sign*66,-233),.58,.55)
        s.bez((sign*50,-229),(sign*58,-207),(sign*46,-158),(sign*39,-125),.48,.5)
        for k in range(4):
            y=-209+k*21
            s.bez((sign*30,y),(sign*39,y+4),(sign*48,y+3),(sign*55,y-1),.32,.45)
        for y in (-223,-129):bolt(s,sign*43,y,1.8,.6)
    s.bez((-46,-117),(-25,-112),(25,-112),(46,-117),.5,.5)
    # Pelvis with projecting hip sockets and a separate lower access seam.
    contour(s,[("M",-37,-69),("C",-53,-66,-67,-58,-69,-42),
        ("C",-72,-24,-59,-6,-43,1),("C",-27,4,-17,-2,0,-2),
        ("C",17,-2,27,4,43,1),("C",59,-6,72,-24,69,-42),
        ("C",67,-58,53,-66,37,-69),("C",18,-64,-18,-64,-37,-69)],
        a=.82,w=.85,fill=.024,close=True)
    s.bez((-56,-49),(-31,-42),(31,-42),(56,-49),.5,.55)
    s.bez((-31,-10),(-18,-17),(18,-17),(31,-10),.4,.5)
    for i in range(2):dummy_joint(s,hips[i],15,True)
    # The neck ends exactly in the collar seat at y=-258.
    s.ellipse(0,-256,20,5,a=.8,w=.65)
    front_head(s,0,-304,1.25)
    contour(s,[("M",-31,-316),("C",-17,-321,17,-321,31,-316),
        ("L",29,-300),("C",17,-296,-17,-296,-29,-300)],
        a=.86,w=.8,fill=.045,close=True,color=ARC)
    for sign in (-1,1):
        s.rect(sign*34-3,-302,6,14,.75,.55,fill=.2,color=GOLD)
        s.bez((sign*36,-288),(sign*34,-274),(sign*34,-263),(sign*45,-253),.4,.5)
    contour(s,[("M",-21,-214),("L",21,-214),("L",24,-208),("L",24,-164),
        ("L",18,-158),("L",-18,-158),("L",-24,-164),("L",-24,-208)],
        a=.72,w=.65,fill=.028,close=True)
    s.rect(-13,-201,26,25,.62,.5,color=ARC)
    for x in (-17,17):
        for y in (-207,-165):bolt(s,x,y,1.4,.5)
    for i in range(2):
        for p1,p2,r1,r2 in ((shoulders[i],elbows[i],21,15),(elbows[i],wrists[i],17,11),
                            (hips[i],knees[i],32,23),(knees[i],ankles[i],24,12)):
            muscle_sleeve(s,p1,p2,r1,r2)
    optical_target(s,0,-234,7)
    dummy_hand(s,wrists[0],angle=9)
    dummy_hand(s,wrists[1],angle=-9,side=-1)
    s.c.restore()


def proxy_body(s,mx,my):
    """One set of rigid dummy components, posed twice with no per-side stretching."""
    from leisure import cuff
    s.c.save();s.c.translate(mx,my)
    pose=proxy_pose();sh=pose['shoulder'];hip=pose['hip']

    def side_parts(side,a):
        q=pose[side]
        segments=(('upper_arm',sh,q['elbow']),('forearm',q['elbow'],q['wrist']),
                  ('thigh',hip,q['knee']),('calf',q['knee'],q['ankle']))
        for name,p1,p2 in segments:
            length,r1,r2,j1,j2=PROXY_PARTS[name]
            assert abs(math.dist(p1,p2)-length)<1e-8
            dummy_segment(s,p1,p2,r1,r2,j1,j2,a)
        for point,r,target in ((q['elbow'],11,False),(q['knee'],15,True)):
            dummy_joint(s,point,r,target,a)
        dummy_foot(s,q['ankle'],angle=q['foot_angle'],a=a)

    side_parts('far',.55)
    dummy_hand(s,pose['far']['wrist'],angle=pose['far']['hand_angle'],side=-1,a=.55)
    for r in (20,28,36):s.arc(-116,-40,r,140,220,.4,.5)
    # Lumbar stack follows the same forward lean as the rib jacket.
    contour(s,[("M",-28,-69),("L",49,-53),("L",37,-11),("L",-32,-24)],
        a=.57,w=.6,fill=.012,close=True)
    for k in range(5):
        y=-57+k*7;s.bez((-28,y),(-5,y+7),(20,y+10),(44,y+14),.49,.5)
    contour(s,[("M",-30,-27),("C",-48,-21,-53,1,-49,23),
        ("C",-46,43,-21,57,1,56),("C",22,54,38,35,44,16),
        ("C",49,0,39,-13,30,-17),("L",-30,-27)],a=.83,w=.9,fill=.022,close=True)
    s.bez((-38,-7),(-18,-5),(12,1),(28,9),.46,.5)

    # Rib cage in its own rigid, tilted frame. Convex sternum, flatter back,
    # sloping clavicle and a distinct collar seat replace the bottle outline.
    s.c.save();s.c.translate(20,-129);s.c.rotate(math.radians(11.4))
    contour(s,[("M",-14,-81),("L",14,-81),
        ("C",25,-78,41,-70,47,-57),("C",58,-38,61,-14,55,7),
        ("C",51,23,42,47,35,66),("C",18,73,-8,75,-32,67),
        ("C",-38,49,-41,28,-42,6),("C",-44,-15,-45,-38,-38,-57),
        ("C",-33,-71,-23,-76,-14,-81)],a=.9,w=.95,fill=.022,close=True)
    # The neck overlaps the socket by three units; it cannot float above it.
    contour(s,[("M",-12,-110),("L",12,-110),("L",14,-78),("L",-14,-78)],
        a=.76,w=.7,fill=.015,close=True)
    for y in (-105,-99,-93,-87):
        s.bez((-12,y),(-5,y+2),(5,y+2),(12,y),.62,.55)
    s.rect(-16,-114,32,5,.82,.7,fill=.03)
    for x in (-10,10):bolt(s,x,-111,1.4,.6)
    s.bez((-22,-66),(-34,-42),(-30,-2),(-28,21),.5,.5)
    s.bez((28,-65),(42,-48),(44,-18),(38,7),.5,.5)
    for k in range(4):
        y=-43+k*17;s.bez((18,y),(30,y+5),(41,y+5),(48,y),.4,.5)
    s.bez((-29,61),(-12,67),(13,66),(31,61),.52,.5)
    for x,y in ((-28,-52),(36,-49),(-26,50),(28,49)):bolt(s,x,y,1.7,.56)
    s.c.restore()

    side_parts('near',.8)
    dummy_joint(s,sh,16,True);dummy_joint(s,hip,18,True)
    e,w=pose['near']['elbow'],pose['near']['wrist']
    cuff(s,e,w,.52,.98,14,fill=.10,color=ARC)
    cuff(s,e,w,.70,.86,17,fill=.45,color=GOLD)
    dummy_hand(s,w,angle=-135,side=-1)
    s.c.restore()
