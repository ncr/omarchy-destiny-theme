"""Sixteen subject-specific figures: declared idealisations, never synthetic data."""
import math
from sheet import WHITE,ARC,GOLD
from .editorial import tx,arrow,header,axes,curve
from collection_layout import field_notes
from triptych import diagram_y,register_section,punchline

DATA={
101:dict(kind='release',fact='Non-pyrotechnic does not mean zero shock. Stored bolt strain still has to go somewhere.',rows=[('PRELOAD','TRANSFER BEFORE RELEASE'),('PYROTECHNICS','NONE IN THIS CONCEPT'),('SHOCK','REQUIRES MEASUREMENT')],note='EXPLOSIVE PERSONALITY: NOT INSTALLED.',left=('HAND OVER THE LOAD FIRST','SCRIPTED RELEASE STATES / TIME NOT TO SCALE'),right=('THE RECORD IS NOT THE EVENT','FICTIONAL RECORDER STRIP / FOUR CONTACTS')),
103:dict(kind='capillarity',fact='A wetted membrane can retain gas below its bubble point. The result depends on pore size and coolant chemistry.',rows=[('SURFACE','MATCHED TO COOLANT'),('GAS INVENTORY','BUFFERED BEFORE VENT'),('GRAVITY','NOT THE SEPARATOR')],note='ALL BUBBLES MUST DECLARE THEIR INTENTIONS.',left=('SMALL PORES, LARGE CONSEQUENCES','IDEAL CAPILLARY PRESSURE / FIXED WETTING'),right=('KEEP THE INTERFACE WET','MEMBRANE CROSS-SECTION / NOT TO SCALE')),
104:dict(kind='consent',fact='Both independent inputs must be present. This is a mechanical logic concept, not a certified security lock.',rows=[('LOGIC','KEY ONE AND KEY TWO'),('SENIORITY','NO BYPASS'),('EMERGENCY','SEPARATE PROCEDURE')],note='ADMINISTRATOR IS NOT A THIRD PERSON.',left=('AUTHORITY DOES NOT ADD UP','BOOLEAN PERMISSION TABLE / NO MASTER INPUT'),right=('CONSENT HAS AN EXPIRY','SCRIPTED WITHDRAWAL / BEFORE BOLT RELEASE')),
105:dict(kind='metrology',fact='Pitch and diameter can identify a thread. Neither establishes voltage, pressure rating or polarity.',rows=[('MECHANICAL','MEASURE BEFORE MATING'),('ELECTRICAL','SEPARATE VERIFICATION'),('ADAPTER','DECLARED LIMITS ONLY')],note='THE THREAD FITS. THAT IS NOT A TREATY.',left=('SAME DIAMETER, WRONG CONVERSATION','TWO THREAD PROFILES / SYMBOLIC PITCH'),right=('PASS IS A SMALLER SET','FICTIONAL ACCEPTANCE REGISTER / 12 ARRIVALS')),
106:dict(kind='scattering',fact='Track deflection carries information about the cargo. Sparse cosmic arrivals limit how quickly an image forms.',rows=[('SOURCE','NATURAL COSMIC MUONS'),('MEASURED','INCOMING / OUTGOING TRACK'),('DENSITY MAP','RECONSTRUCTION REQUIRED')],note='EXPRESS LANE SUBJECT TO COSMIC AVAILABILITY.',left=('A BEND LEAVES A CLUE','SINGLE ILLUSTRATIVE TRACK / NO EVENT DATA'),right=('THE SKY SETS THE SAMPLE SIZE','IDEAL POISSON COUNT UNCERTAINTY / 1 OVER ROOT N')),
107:dict(kind='resonance',fact='A tuned absorber acts near selected frequencies. Changing the host or load can move the resonance away.',rows=[('TUNING','MEASURE, MOVE, LOCK'),('MODEL','f = ROOT(k / m) / 2 PI'),('SILENCE','NOT A WARRANTY')],note='GOOD VIBRATIONS ARE STILL VIBRATIONS.',left=('MORE MASS, LOWER NOTE','IDEAL NATURAL FREQUENCY / FIXED STIFFNESS'),right=('THE HOST AND ITS UNINVITED GUEST','TWO COUPLED OSCILLATORS / LUMPED MODEL')),
108:dict(kind='handoff',fact='The needle must remain controlled through each transfer. The drawing uses a neutral test sheet, not clinical tissue.',rows=[('SUBSTRATE','TEST MEMBRANE'),('HOLD','AT LEAST ONE GRIPPER'),('CLINICAL STATUS','NOT ESTABLISHED')],note='KNOTS SHOULD BE IN THE THREAD, NOT THE PLAN.',left=('DO NOT DROP THE NEEDLE','SCRIPTED GRIPPER STATES / NO CLINICAL DATA'),right=('SLACK NEEDS SOMEWHERE TO GO','DANCER GEOMETRY / SYMBOLIC THREAD RESERVE')),
110:dict(kind='rotation',fact='Radial acceleration grows with speed squared. The bowl rotates; the rest of the galley remains weightless.',rows=[('MODEL','a = OMEGA SQUARED TIMES r'),('LID','OPEN ONLY WHEN STOPPED'),('HUMANS','NOT AN INGREDIENT')],note='ARTIFICIAL GRAVITY. AUTHENTIC LEFTOVERS.',left=('DOUBLE THE SPEED, FOUR TIMES THE MESS','IDEAL RADIAL ACCELERATION / FIXED RADIUS'),right=('BALANCE IS PART OF THE RECIPE','STATIC FIRST-MOMENT BALANCE / IDEAL PAIR')),
}

def capsule(s,x,y,w,h,r=7,color=WHITE,a=.7):
 pts=[]
 for cx,cy,a0 in ((x+w-r,y+r,-90),(x+w-r,y+h-r,0),(x+r,y+h-r,90),(x+r,y+r,180)):
  pts.extend((cx+r*math.cos(math.radians(a0+j*90/8)),cy+r*math.sin(math.radians(a0+j*90/8))) for j in range(9))
 s.poly(pts,a,.65,close=True,color=color)

def waveform(s,x,y,w,h,fn,xlabel,top='1',ticks=()):
 axes(s,x+25,y,w-35,h,xlabel,top)
 curve(s,[(x+25+(w-35)*i/120,y+h*(1-fn(i/120))) for i in range(121)],ARC)
 for t,label in ticks:tx(s,label,x+25+(w-35)*t,y+h+11,7,.7,align='c')

def trace_rows(s,x,y,labels,states,w=440):
 """Three discrete contact records with explicit disjoint row captions."""
 left=x+128;step=(w-145)/len(states[0])
 for r,(label,row) in enumerate(zip(labels,states)):
  yy=y+13+r*31;tx(s,label,x,yy+4,7)
  s.ln(left,yy+9,x+w,yy+9,.18,.4)
  pts=[]
  for j,on in enumerate(row):
   if j:pts.append((left+j*step,yy-(10 if row[j-1] else 0)))
   pts.extend([(left+j*step,yy-(10 if on else 0)),(left+(j+1)*step,yy-(10 if on else 0))])
  curve(s,pts,ARC if r!=2 else GOLD)


def figure(s,n,side,x,y,w):
 d=DATA[n];title,scope=d[side];header(s,dict(title=title,scope=scope),x,y,w)
 body=y+39;foot=''
 if side=='left':
  if n==101:
   trace_rows(s,x,body,('PRIMARY HOLD','TRANSFER CAM','JAW OPEN'),((1,1,0,0,0),(0,1,1,1,0),(0,0,0,1,1)))
   tx(s,'HOLD',x+128,body+113);tx(s,'HANDOFF',x+260,body+113);tx(s,'RELEASE',x+w,body+113,align='r')
   foot='Contact states only; no invented shock attenuation curve.'
  elif n==103:
   waveform(s,x,body,w,91,lambda t:1/(1+3*t),'PORE RADIUS / r0','1',((0,'1'),(1/3,'2'),(1,'4')))
   foot='Pressure ratio = r0 / r; surface tension and angle fixed.'
  elif n==104:
   tx(s,'KEY ONE',x+20,body);tx(s,'KEY TWO',x+135,body);tx(s,'PERMISSION',x+265,body)
   for i,(a,b) in enumerate(((0,0),(0,1),(1,0),(1,1))):
    yy=body+26+i*23
    tx(s,str(a),x+43,yy);tx(s,str(b),x+158,yy)
    s.circ(x+257,yy-3,3,.8,.7,color=ARC if a*b else WHITE)
    tx(s,'RELEASE' if a*b else 'HOLD',x+275,yy,color=ARC if a*b else WHITE)
   foot='Equal inputs. Neither key can impersonate the other.'
  elif n==105:
   for j,pitch in enumerate((24,38)):
    yy=body+22+j*55;capsule(s,x+24,yy-15,310,31,7)
    # Rounded thread crests; straight flanks are physical geometry.
    pts=[]
    for k in range(113):
     xx=x+32+k*2.6;v=(xx-x-32)/pitch
     zz=7*math.cos(math.tau*v)
     pts.append((xx,yy+zz))
    curve(s,pts,WHITE);tx(s,'PITCH '+('p' if j==0 else '1.6p'),x+351,yy+4)
   foot='Nominal diameter agrees; axial engagement does not.'
  elif n==106:
   for yy in (body+6,body+24,body+92,body+110):capsule(s,x+47,yy,280,5,2,a=.5)
   capsule(s,x+144,body+40,88,40,9,a=.35)
   s.poly([(x+146,body-2),(x+189,body+59),(x+232,body+125)],.85,.9,close=False,color=ARC)
   s.poly([(x+189,body+59),(x+165,body+125)],.7,.8,close=False,color=GOLD)
   tx(s,'IN',x+344,body+20);tx(s,'CARGO',x+344,body+65);tx(s,'OUT',x+344,body+109)
   foot='One scattering example. Not a reconstructed density map.'
  elif n==107:
   waveform(s,x,body,w,91,lambda t:1/math.sqrt(1+3*t),'MOVING MASS / m0','1',((0,'1'),(1/3,'2'),(1,'4')))
   foot='Frequency ratio = root(m0 / m); one ideal branch.'
  elif n==108:
   trace_rows(s,x,body,('LEFT GRIP','RIGHT GRIP','NEEDLE HELD'),((1,1,0,0,1),(0,1,1,1,1),(1,1,1,1,1)))
   tx(s,'HOLD',x+128,body+113);tx(s,'OVERLAP',x+251,body+113);tx(s,'TRANSFER',x+w,body+113,align='r')
   foot='Overlap is intentional; this chart does not prove a safe grip.'
  elif n==110:
   waveform(s,x,body,w,91,lambda t:t*t,'ANGULAR SPEED / OMEGA0','4',((0,'0'),(.5,'1'),(1,'2')))
   foot='a / a0 = (omega / omega0)² at the same radius.'
 else:
  if n==101:
   for i,(label,start,end) in enumerate((('ARM',0,3),('CAM',1,4),('JAW',3,5),('CLEAR',4,5))):
    yy=body+8+i*27;tx(s,label,x,yy+3)
    for j in range(6):s.ln(x+95+j*53,yy-10,x+95+j*53,yy+9,.16,.5)
    capsule(s,x+95+start*53,yy-5,(end-start)*53,8,3,ARC)
   foot='Order of contacts, not a calibrated time or vibration trace.'
  elif n==103:
   capsule(s,x+30,body+28,320,62,15)
   for xx in range(70,320,25):
    s.ln(x+xx,body+31,x+xx,body+88,.35,.7)
    s.circ(x+xx-7,body+59,2,.7,.6,color=ARC)
   for xx,r in ((80,10),(155,13),(245,9)):s.circ(x+xx,body+12,r,.72,.7,color=GOLD)
   arrow(s,(x+10,body+114),(x+345,body+114),ARC)
   tx(s,'GAS',x+370,body+17);tx(s,'WET PORE',x+370,body+61);tx(s,'LIQUID',x+370,body+118)
   foot='Gas is excluded below bubble point; fouling changes behaviour.'
  elif n==104:
   trace_rows(s,x,body,('KEY ONE','KEY TWO','PERMISSION'),((1,1,1,1,1),(0,1,1,0,0),(0,1,1,0,0)))
   tx(s,'SECOND KEY WITHDRAWN',x+128,body+114)
   foot='Pre-release permission falls when either input is removed.'
  elif n==105:
   for i,(label,count) in enumerate((('ARRIVED',12),('THREAD FIT',8),('FULL MATCH',3))):
    yy=body+13+i*38;tx(s,label,x,yy+4)
    for j in range(12):
     xx=x+145+j*22;capsule(s,xx,yy-8,12,16,4,ARC if j<count else WHITE,.8 if j<count else .18)
   foot='Example register only: 12 arrivals, 8 fits, 3 authorised.'
  elif n==106:
   waveform(s,x,body,w,91,lambda t:1/math.sqrt(1+99*t),'DETECTED COUNT / N','1',((0,'1'),(.24,'25'),(1,'100')))
   foot='Count uncertainty only; image resolution has other limits.'
  elif n==107:
   s.ln(x+30,body+100,x+390,body+100,.5,.6)
   capsule(s,x+87,body+29,130,58,12)
   capsule(s,x+292,body+43,61,30,8,color=ARC)
   for start,end,yy in ((x+28,x+87,body+58),(x+217,x+292,body+58)):
    pts=[(start,yy)]+[(start+(end-start)*i/80,yy+6*math.sin(i*math.tau/16)) for i in range(81)]
    curve(s,pts,WHITE)
   tx(s,'HOST MASS',x+152,body+19,align='c');tx(s,'ABSORBER',x+324,body+22,align='c')
   tx(s,'M / K',x+152,body+117,align='c');tx(s,'m / k',x+324,body+117,align='c')
   foot='Coupled motion, not broadband cancellation or silence.'
  elif n==108:
   for xx in (80,340):s.circ(x+xx,body+15,12,.7,.7)
   s.circ(x+210,body+83,15,.75,.7,color=ARC)
   s.poly([(x+68,body+15),(x+197,body+83),(x+223,body+83),(x+352,body+15)],.7,.7,close=False,color=GOLD)
   arrow(s,(x+210,body+35),(x+210,body+61),ARC)
   tx(s,'SUPPLY',x+80,body-5,align='c');tx(s,'NEEDLE',x+340,body-5,align='c')
   tx(s,'MOVING DANCER / TWO THREAD LEGS',x+210,body+119,align='c')
   foot='For parallel legs, reserve change is twice dancer travel.'
  elif n==110:
   s.ln(x+50,body+70,x+384,body+70,.65,1)
   s.circ(x+224,body+70,10,.8,.8)
   capsule(s,x+61,body+49,43,42,8,color=GOLD)
   capsule(s,x+338,body+56,29,28,6,color=ARC)
   arrow(s,(x+215,body+100),(x+85,body+100));arrow(s,(x+233,body+100),(x+351,body+100))
   tx(s,'m1',x+83,body+37,align='c');tx(s,'m2',x+353,body+44,align='c')
   tx(s,'r1',x+143,body+116,align='c');tx(s,'r2',x+292,body+116,align='c')
   foot='m1 × r1 = m2 × r2; real rotor also needs dynamic balance.'
 tx(s,foot,x,y+184,7,.67)


def draw(s,entry):
 n=entry['number'];d=DATA.get(n)
 if not d:return
 with s.layer('section'):
  for side,x in (('left',140),('right',s.W-650)):
   y=diagram_y(s,side,187);figure(s,n,side,x,y,440);register_section(s,side,y-16,y+187)
  s.diagram_slots={'left','right'}
  field_notes(s,d);punchline(s,d['note'])
