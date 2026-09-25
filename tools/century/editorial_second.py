"""Second ten: individual plots, mechanism diagrams and fictional service records."""
import math
from sheet import WHITE,ARC,GOLD
from collection_layout import note_box
from .editorial import tx,arrow,header,axes,curve,dossier

DATA={
2:dict(title='THE TIDE DOES NOT TAKE REQUESTS',kind='current',scope='KINETIC FLUX / FIXED AREA AND DENSITY',
 fact='Available flow power scales with speed cubed. Output also depends on extraction efficiency.',
 note='THE MOON HAS DECLINED YOUR SLA.',process=('CURRENT','ROTOR','GRID'),
 rows=[('MODEL','P / P0 = |v / v0|³'),('SLACK WATER','NO FLOW POWER'),('FISH','NOT A FUEL SOURCE')],foot='Available flux only; not a turbine output curve.'),
6:dict(title='THE HULL WOULD LIKE SOME SPACE',kind='foil',scope='IDEAL LIFT RATIO / FIXED AREA, DENSITY AND CL',
 fact='Lift depends on speed squared at fixed lift coefficient. Foil control must still hold ride height.',
 note='SEASICKNESS HAS NOT ACCEPTED THE PATCH.',process=('ACCELERATE','TRIM','RETRACT'),
 rows=[('MODEL','L / L0 = (v / v0)²'),('AT THE DOCK','FOILS RETRACTED'),('CAVITATION','NOT MODELLED')],foot='Fully submerged foil idealisation; not a ferry speed rating.'),
17:dict(title='YOUR PASSWORD DID NOT FOSSILISE',kind='archive',scope='SYMBOLIC CELL MAP / NOT A STORAGE FORMAT',
 fact='Ultrafast pulses can write structures inside glass. Reading requires the right optical system.',
 note='README INCLUDED. CIVILISATION NOT INCLUDED.',process=('WRITE','VERIFY','DECODE'),
 rows=[('MEDIUM','GLASS'),('DECODER','STORED BESIDE IT'),('FAMILY SECRETS','STILL BACKED UP')],foot='Orientation glyphs explain encoding; no capacity claim.'),
18:dict(title='DUST HAS NO CABIN PRIVILEGES',kind='suitport',scope='CONTAMINATION BOUNDARY / SCHEMATIC',
 fact='A suitport keeps the suit outside. Seals and servicing still need dust control.',
 note='PLEASE WIPE YOUR PLANET BEFORE ENTERING.',process=('DOCK','CHECK','ENTER'),
 rows=[('SUIT','EXTERIOR'),('SEAL','TEST BEFORE ENTRY'),('EMERGENCY','SEPARATE EGRESS')],foot='NASA suitport principle; no claim of perfect isolation.'),
25:dict(title='DIRECTION IS A MATERIAL PROPERTY',kind='braid',scope='IDEAL HELIX / FIXED CARRIER TANGENTIAL SPEED',
 fact='Faster axial take-up reduces braid angle in this geometric model. Strength also depends on layup.',
 note='UNLIKE THE COMMITTEE, THE FIBRES HAVE DIRECTION.',process=('TENSION','CROSS','TAKE UP'),
 rows=[('ANGLE','TO MANDREL AXIS'),('MODEL','tan(angle) = vt / vz'),('FAMILIES','OPPOSITE HANDEDNESS')],foot='Kinematic illustration; no composite strength prediction.'),
38:dict(title='ACCESS IS NOT A SIDE QUEST',kind='access',scope='SCRIPTED INTERLOCK SEQUENCE / NOT CERTIFICATION',
 fact='Treads level while empty. The locked level deck then lifts together after entry gates engage.',
 note='CLAUDE CALLED THIS LABEL LOAD-BEARING. THE LATCH DISAGREES.',process=('LEVEL','LOCK','LIFT'),
 rows=[('ACCESS','SAME PUBLIC ROUTE'),('LEVELLING','EMPTY DECK'),('RELEASE','MANUAL OVERRIDE')],foot='Fixed tread positions; independent vertical screws. Concept, not certification.'),
42:dict(title='YOU ALSO HAVE TO REEL IT BACK',kind='kite',scope='ILLUSTRATIVE FORCE / PAID-OUT LENGTH CYCLE',
 fact='Reeling out at higher tension than reeling in creates net mechanical work over a cycle.',
 note='STORM MODE: LAND. DO NOT NEGOTIATE.',process=('REEL OUT','DEPOWER','REEL IN'),
 rows=[('WORK','LOOP AREA'),('RETURN','CONSUMES ENERGY'),('NET ELECTRIC','AFTER LOSSES')],foot='Normalised example; transitions and losses omitted.'),
65:dict(title='A CIRCLE IS NOT A CERTIFICATE',kind='weld',scope='FICTIONAL INSPECTION LOG / TWELVE SECTORS',
 fact='Completing a weld path and accepting the joint are separate decisions. Inspection can stop release.',
 note='THE DEADLINE IS NOT A WELDING PARAMETER.',process=('PREPARE','WELD','INSPECT'),
 rows=[('ACCEPT','9 SECTORS'),('HOLD','2 SECTORS'),('REWORK','1 SECTOR')],foot='Illustrative disposition map; not defect or sensor data.'),
70:dict(title='FIVE MINUTES, SINCE LAST TUESDAY',kind='queue',scope='FICTIONAL EVENT LOG / SIX COMPLETED POSITIONS',
 fact='Each leaf records a completed position. It does not predict when your turn will arrive.',
 note='PLEASE HOLD. YOUR PATIENCE IS IMPORTANT TO US.',process=('TICKET','EVENT','LEAF'),
 rows=[('LEAVES','6 COMPLETIONS'),('CLOCK','NOT A FORECAST'),('ESTIMATE','INSUFFICIENT EVIDENCE')],foot='Events at 2, 5, 9, 14, 20, 27 min; not queue performance.'),
80:dict(title='AMAZING HAS FAILED INSPECTION',kind='praise',scope='FICTIONAL REVIEW LOG / TWELVE CANDIDATES',
 fact='A defensible compliment needs an observation. Enthusiasm is not a measurement.',
 note='FLATTERY CARTRIDGE: EMPTY BY DESIGN.',process=('INSPECT','CITE','PRINT'),
 rows=[('SPECIFIC','3 APPROVED'),('GENERIC','7 REJECTED'),('UNSUPPORTED','2 REJECTED')],foot='Example receipt: Your three mounting holes are aligned.')
}


def plot(s,d,x,y,w):
    header(s,d,x,y,w);y+=40;h=97;k=d['kind'];px=x+26;pw=w-28
    if k in ('current','foil','braid'):
        axes(s,px,y,pw,h,{'current':'CURRENT / v0','foil':'SPEED / v0','braid':'AXIAL SPEED / vt'}[k], '90°' if k=='braid' else '1.0' if k=='current' else '4.0')
        points=[]
        for i in range(121):
            t=i/120
            if k=='current':value=abs(2*t-1)**3
            elif k=='foil':value=(2*t)**2/4
            else:value=math.atan2(1,.25+3.75*t)/(math.pi/2)
            points.append((px+pw*t,y+h*(1-value)))
        curve(s,points)
        ticks=[(0,'-1'),(.5,'0'),(1,'+1')] if k=='current' else [(0,'0'),(.5,'1'),(1,'2')] if k=='foil' else [(0,'0.25'),(.2,'1'),(.467,'2'),(1,'4')]
        for t,label in ticks:tx(s,label,px+pw*t,y+h+9,5.5,.65,align='c')
    elif k=='archive':
        # Four symbolic orientations, laid on four real-looking indexed rows.
        for row in range(4):
            tx(s,str(row).zfill(2),x,y+13+row*22,6,.5)
            for col in range(9):
                xx=x+40+col*24;yy=y+10+row*22;a=((row*5+col*3)%4)*math.pi/4
                s.circ(xx,yy,5,.22,.35)
                s.ln(xx-4*math.cos(a),yy-4*math.sin(a),xx+4*math.cos(a),yy+4*math.sin(a),.8,.9,color=ARC)
        tx(s,'ORIENTATION',x+w,y+10,6,.6,align='r')
        for i,word in enumerate(('00 / —','01 / /','10 / |','11 / \\')):tx(s,word,x+w,y+29+i*18,7,.8,align='r')
        tx(s,'READING KEY TRAVELS WITH THE PLATE',x,y+119,6,.5)
    elif k=='suitport':
        boundary=x+238
        s.ln(boundary,y+4,boundary,y+102,.65,.7)
        s.ln(boundary+5,y+4,boundary+5,y+102,.32,.4)
        tx(s,'EXTERIOR',x+40,y+8,6,.65);tx(s,'CABIN',x+w-25,y+8,6,.65,align='r')
        # Dust samples stop before the pressure boundary; occupants pass a tested interface.
        for dx,dy in ((12,25),(51,47),(88,32),(136,68),(38,77),(111,85),(172,38)):
            s.diamond(x+dx,y+dy,2,.55,.5,color=GOLD)
        tx(s,'DUSTY SUIT',x+35,y+109,6,.62)
        s.poly([(boundary-35,y+29),(boundary-14,y+29),(boundary-14,y+77),(boundary-35,y+77)],.7,.6,close=False)
        arrow(s,(boundary-8,y+53),(x+w-29,y+53),ARC)
        tx(s,'REAR ENTRY',x+w-20,y+78,6,.6,align='r')
        tx(s,'TESTED SEAL',boundary,y+122,6,.66,align='c')
    elif k=='access':
        # Elevation of the exact model's four fixed-x, independently driven treads.
        # Three states, common scale. No fictitious diagonal four-bar mechanism.
        for n,(name,heights) in enumerate((('01 / STAIR',[16,33,50,67]),('02 / LEVEL LOW',[16]*4),('03 / LEVEL HIGH',[67]*4))):
            xx=x+n*151;floor=y+86
            for j,z in enumerate(heights):
                left=xx+j*28;top=floor-z*.82
                s.poly([(left,top),(left+27,top),(left+27,top+4),(left,top+4)],.8,.7,close=True)
                s.ln(left+13,top+5,left+13,floor,.3,.5)
            s.ln(xx,floor+2,xx+111,floor+2,.28,.5)
            tx(s,name,xx,y+106,5.7,.73)
            if n<2:arrow(s,(xx+116,y+48),(xx+139,y+48),ARC)
        tx(s,'EMPTY TO LEVEL / LOCK TREADS / THEN PLATFORM LIFT',x,y+127,5.7,.55)
    elif k=='kite':
        axes(s,px,y,pw,h,'PAID-OUT LENGTH / NORMALISED')
        a=(px+pw*.13,y+h*.17);b=(px+pw*.87,y+h*.17);c=(b[0],y+h*.79);d0=(a[0],c[1])
        s.poly([a,b,c,d0],.7,.6,close=True,color=GOLD)
        arrow(s,a,b,ARC);arrow(s,c,d0,WHITE)
        tx(s,'HIGH TENSION / REEL OUT',px+pw/2,y+6,6,.72,align='c')
        # Loop area is explained in the adjacent dossier; keep grid free of text.
        tx(s,'LOW TENSION / RETURN',px+pw/2,y+92,6,.65,align='c')
    elif k=='weld':
        cx=x+91;cy=y+54;r=43
        for j in range(12):
            col=ARC if j<9 else GOLD
            pts=[(cx+r*math.cos(math.radians(-90+j*30+a)),cy+r*math.sin(math.radians(-90+j*30+a))) for a in range(3,28,3)]
            s.poly(pts,.8,2.1 if j==11 else 1,close=False,color=col)
            if j==11:
                a=math.radians(-90+j*30+15);xx=cx+r*math.cos(a);yy=cy+r*math.sin(a)
                s.ln(xx-3,yy-3,xx+3,yy+3,.8,.6);s.ln(xx+3,yy-3,xx-3,yy+3,.8,.6)
        tx(s,'12',cx,cy+4,11,.8,align='c');tx(s,'SECTORS',cx,cy+18,5.5,.5,align='c')
        for i,(label,count) in enumerate((('ACCEPT',9),('HOLD',2),('REWORK',1))):
            yy=y+20+i*30;s.ln(x+170,yy-3,x+193,yy-3,.8,1,color=ARC if i==0 else GOLD)
            tx(s,label,x+208,yy,6.5,.72);tx(s,str(count),x+w,yy,7,.8,align='r')
    elif k=='queue':
        axes(s,px,y,pw,h,'ELAPSED MINUTES','6','0');pts=[(px,y+h)]
        for i,t in enumerate((2,5,9,14,20,27)):
            xx=px+pw*t/30;pts.extend([(xx,y+h*(1-i/6)),(xx,y+h*(1-(i+1)/6))])
        pts.append((px+pw,y));curve(s,pts,ARC)
        for t in (0,10,20,30):tx(s,str(t),px+pw*t/30,y+h+9,5.5,.6,align='c')
    elif k=='praise':
        for i,(label,v) in enumerate((('SPECIFIC',3),('GENERIC',7),('UNSUPPORTED',2))):
            yy=y+18+i*32;tx(s,label,x,yy,6.3,.7)
            for j in range(7):
                xx=x+132+j*30
                if j<v:s.ln(xx,yy-3,xx+17,yy-3,.85,3,color=ARC if i==0 else GOLD)
                else:s.ln(xx,yy-3,xx+17,yy-3,.17,.6)
            tx(s,str(v),x+w,yy,7,.8,align='r')
    tx(s,d['foot'],x,y+145,5.9,.6)


def draw(s,entry):
    d=DATA.get(entry['number'])
    if not d:return
    from triptych import extra, diagram, punchline, diagram_y, register_section
    with s.layer('section'):
        y=diagram_y(s,'left',187)
        plot(s,d,140,y,440)
        register_section(s,'left',y-16,y+187)
        s.diagram_slots={'left'}
        diagram(s,'right')
        dossier(s,d,*note_box(s))
        punchline(s,d['note'])
