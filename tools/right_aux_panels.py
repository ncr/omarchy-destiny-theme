"""Right-side spatial studies, with labels kept outside the drawing envelope."""
from sheet import WHITE, ARC, GOLD
from hardware3d.secondary_drawing import view


def owner(s,rx):
    a=view(s,'proxy-sleeping-owner',rx,321,347,268)
    s.text('06:40',rx+169,166,18,track=.04,a=.9,align='r')
    s.text('10.0 km / DONE',rx+169,184,7,track=.07,a=.85,align='r',color=ARC)
    s.text('HUMAN OWNER',rx-174,170,7,track=.09,a=.85)
    s.text('STAND-IN; STILL ASLEEP',rx-174,185,5.6,track=.08,a=.58)
    x,y=a['HUMAN']
    s.poly([(rx-145,194),(rx-145,207),(x,y)],.4,.5,close=False)
    s.dot(x,y,1.2,.65)
    s.text('EFFORT SUCCESSFULLY DELEGATED',rx,480,6.4,a=.6,track=.11,align='c')
    s.view_label(rx,540,'C','THE OWNER','06:40, THE SAME MORNING')


def course(s,rx):
    a=view(s,'sky-racer-course',rx,318,348,314)
    # Number labels follow the projection but sit off each physical gate.
    offsets={1:(24,-18),2:(-8,-26),3:(-9,-24),4:(-15,-22),5:(-24,-5),6:(-24,14),7:(-10,28),8:(14,24),9:(90,-18)}
    for j in range(1,10):
        x,y=a[f'G{j}'];dx,dy=offsets[j]
        s.text(f'{j:02}',x+dx,y+dy,7,track=.04,a=.9,align='c',color=GOLD if j==1 else WHITE)
    s.text('START / FINISH',rx-176,159,6.1,track=.08,a=.8,color=GOLD)
    s.text('ALTITUDE DATUM: GROUND',rx-176,493,6.1,track=.08,a=.65)
    s.text('SCHEMATIC / HEIGHT EXAGGERATED',rx-176,510,5.6,track=.08,a=.45)
    s.view_label(rx,548,'C','COURSE','9 GATES / 2.4 km / 30 – 180 m ABOVE GROUND')


def kidney(s,rx):
    a=view(s,'foundry-renal-section',rx,318,292,298)
    # Numbered leaders terminate in dedicated side gutters. The key below is
    # physically separate, so captions never sit on vessels or tissue hatching.
    for key,num,tx,ty in [('CORTEX','01',rx-170,210),('MEDULLA','02',rx-170,376),('SUPPLY','03',rx+170,261),('DRAIN','04',rx+170,444)]:
        x,y=a[key];side=-1 if tx<rx else 1
        s.poly([(x,y),(tx-side*17,ty-2),(tx-side*8,ty-2)],.48,.5,close=False)
        s.dot(x,y,1.3,.7)
        s.text(num,tx,ty,6.7,track=.05,a=.9,align='c')
    for num,label,x,y,color in [('01','CORTEX',rx-171,490,WHITE),('02','MEDULLARY PYRAMIDS',rx-171,508,WHITE),('03','VASCULAR SUPPLY',rx+8,490,ARC),('04','COLLECTING SYSTEM',rx+8,508,GOLD)]:
        s.text(num,x,y,6.3,track=.06,a=.6)
        s.text(label,x+21,y,6.3,track=.07,a=.86,color=color)
    s.view_label(rx,548,'C','RENAL SECTION','CORONAL CUTAWAY / PRINT CONCEPT')


def node(s,rx):
    a=view(s,'cortical-node-exploded',rx-17,312,298,286)
    for key,num,ty in [('CONTACT','01',194),('WINDOW','02',267),('ROUTING','03',345),('CARRIER','04',422)]:
        x,y=a[key];tx=rx+169
        s.poly([(x,y),(tx-22,ty-2),(tx-8,ty-2)],.48,.5,close=False)
        s.dot(x,y,1.2,.7)
        s.text(num,tx,ty,6.7,track=.05,a=.9,align='c')
    for num,label,x,y,color in [('01','POROUS CONTACT',rx-171,480,WHITE),('02','PASSIVATION WINDOW',rx+8,480,WHITE),('03','METAL ROUTING',rx-171,498,GOLD),('04','FLEXIBLE CARRIER',rx+8,498,WHITE)]:
        s.text(num,x,y,6.3,track=.06,a=.6)
        s.text(label,x+21,y,6.3,track=.07,a=.86,color=color)
    s.view_label(rx,540,'C','ONE NODE','EXPLODED FILMS / THICKNESS EXAGGERATED')


def street(s,rx):
    a=view(s,'greener-street',rx,324,348,324)
    for no in (2,6,10,14,3,7,11,15):
        x,y=a[f'N{no}'];dy=-12 if no%2==0 else 14
        s.text(str(no),x,y+dy,7,track=.06,a=.9,align='c',color=GOLD if no==14 else WHITE)
    s.text('14 / FIRST INSTALLATION',rx-174,518,6.2,track=.07,a=.8,color=GOLD)
    s.text('7 / LAWN PAVED OVER',rx+12,518,6.2,track=.07,a=.8)
    s.view_label(rx,552,'C','THE STREET, YEAR SIX','No. 14 BOUGHT THE FIRST ONE. No. 7 PAVED THE LAWN.')
