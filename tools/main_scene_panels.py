"""Main-scene composition, with physical anchors and deterministic typography."""
import cairo,math
from sheet import WHITE,ARC,GOLD,RED
from hardware3d.family_drawing import data


def scene(s,name,cx,cy,width,height):
    d=data(name);pts=[p for path in d['paths'] for p in path['points']]
    x0=min(p[0] for p in pts);x1=max(p[0] for p in pts);y0=min(p[1] for p in pts);y1=max(p[1] for p in pts)
    k=min(width/(x1-x0),height/(y1-y0));ox=(x0+x1)/2;oy=(y0+y1)/2
    def point(p):return(cx+(p[0]-ox)*k,cy+(p[1]-oy)*k)
    for path in d['paths']:
        role=path['role'];a,w,col={'structure':(.86,.83,WHITE),'detail':(.65,.49,WHITE),'shell':(.38,.35,WHITE),'accent':(.8,.55,ARC),'cable':(.67,.48,GOLD)}.get(role,(.65,.5,WHITE))
        s.poly([point(p) for p in path['points']],a,w,close=False,color=col)
    return {key:point(p) for key,p in d['anchors'].items()}


def callout(s,p,x,y,side,title,sub,color=WHITE):
    s.dot(*p,1.5,.85,color)
    s.poly([p,(x,y),(x+side*116,y)],.48,.5,close=False,color=color)
    align='r' if side<0 else 'l';tx=x+side*5
    s.text(title,tx,y-8,7.3,track=.17,a=.85,align=align,color=color)
    s.text(sub,tx,y+12,5.7,track=.065,a=.62,align=align)


def proxy(s,mx,my):
    a=scene(s,'proxy-main-scene',mx,my-14,558,644)
    # The omitted head remains a symbol, visibly above the physical capped neck.
    from human_figures import absent_head
    hx,hy=a['HEAD'];absent_head(s,hx,hy-57)
    # Bib text belongs to the actual projected plane, not a second guessed pose.
    p,u,v=[a[key] for key in ('BIB0','BIBX','BIBY')]
    s.c.save();s.c.transform(cairo.Matrix((u[0]-p[0])/62,(u[1]-p[1])/62,(v[0]-p[0])/50,(v[1]-p[1])/50,p[0],p[1]))
    s.text('CITY 10K',31,12,5.2,track=.05,a=.85,align='c')
    s.text('114',31,39,24,track=.01,a=.95,align='c',bold=True)
    s.c.restore()
    info=[('HEAD',(hx,hy-57),1,-341,'NONE FITTED / NO TRACKER ASKS FOR ONE'),
          ('RACE NUMBER',a['BIB'],-1,-285,"ENTERED UNDER THE OWNER'S NAME"),
          ("OWNER'S WATCH",a['WATCH'],-1,-180,'THE ONLY PART THE INSURER SEES'),
          ('LEFT WRIST',a['WRIST'],-1,-74,'SKIN, WARMTH, PULSE AND LIGHT SWEAT'),
          ('CHEST',a['CHEST'],1,-139,'BARE ALUMINIUM / NOBODY CHECKS'),
          ('HAND',a['HAND'],1,-20,'WAVES AT NEIGHBOURS BETWEEN STRIDES'),
          ('RIGHT KNEE',a['KNEE'],-1,171,"COPIES THE OWNER'S LIMP FROM A 2041 SKI TRIP"),
          ('FOOT',a['FOOT'],1,280,"WEARS OUT THE OWNER'S OWN SHOES")]
    for title,p,side,dy,sub in info:callout(s,p,mx+side*321,my+dy,side,title,sub)
    x,y=mx+320,my+82
    s.poly([(x,y),(x+12,y),(x+18,y-8),(x+23,y+10),(x+30,y),(x+50,y)],.85,.7,close=False,color=GOLD)
    s.text('142 bpm',x+58,y+3,7,track=.06,a=.85,color=GOLD)


def truth(s,mx,my):
    a=scene(s,'truth-main-scene',mx,my+7,720,683)
    for key,color in [('GRANDMOTHER',ARC),('HOST',RED)]:
        x,y=a[key];s.circ(x,y,19,.6,.6,color=color,dash=[3,4])
    info=[('LAMP','LAMP',-1,-322,'GLOWS RED FOR THREE SECONDS. NOT DIMMABLE.'),
          ('SWITCH','OFF SWITCH',1,-350,'NEW IN VERSION 2'),
          ('MICROPHONES','MICROPHONE RING',-1,-207,'HEARS THE HALF SECOND BEFORE "OF COURSE NOT"'),
          ('CAMERAS','THERMAL CAMERAS',1,-212,'NOSES COOL BY 0.4 °C WHEN THEIR OWNERS LIE'),
          ('GRANDMOTHER','SEAT 1, GRANDMOTHER',-1,-85,'NEVER SETS IT OFF. SAYS WHAT SHE THINKS.'),
          ('HOST','SEAT 4',1,-53,'"NO, I LOVE IT. I\'LL WEAR IT ALL THE TIME."'),
          ('DINNER','DINNER',-1,278,'THE SUBJECT OF 31 % OF ALL DETECTIONS'),
          ('DOG','DOG',1,294,'HAS NEVER SET IT OFF EITHER')]
    for key,title,side,dy,sub in info:callout(s,a[key],mx+side*370,my+dy,side,title,sub)
