"""Eight new machines. Service views are actual subsets of their main models."""
from .kit import *
from . import kit
from .quality_geometry import gear


def ribs(p,size,count=9):
 for i in range(count):
  x=p[0]-size[0]/2+size[0]*(i+.5)/count
  box('cast cooling rib',(x,p[1],p[2]),(1.5,size[1],size[2]),.6,'detail')


def instrument(p,w=38,h=22):
 box('rounded instrument casting',p,(w,12,h),4)
 box('instrument bezel',(p[0],p[1]-7,p[2]),(w-5,2,h-5),2,'detail')
 for i in range(5):rod('engraved scale',(p[0]-w*.3+i*w*.15,p[1]-8,p[2]-3),(p[0]-w*.3+i*w*.15,p[1]-8,p[2]+3),.32,'accent')
 for x in (-w*.36,w*.36):cyl('face screw',(p[0]+x,p[1]-8,p[2]-h*.3),1.1,2,'detail',(0,-1,0),6)
 # Separate bezel, dial and service fasteners remain visible from the camera.
 for x in (-w*.36,w*.36):
  for z in (-h*.31,h*.31):
   cyl('bezel captive screw',(p[0]+x,p[1]-9,p[2]+z),.75,1.7,'detail',(0,-1,0),6)
 for xx in (-w*.22,w*.22):
  ring('instrument dial',(p[0]+xx,p[1]-9,p[2]),h*.22,1,1,(0,-1,0),'detail')
  rod('dial needle',(p[0]+xx,p[1]-11,p[2]),(p[0]+xx+h*.11,p[1]-11,p[2]+h*.1),.25,'accent')
 for i in range(5):box('case ventilation slot',(p[0]+w/2+.3,p[1]-3+i*1.5,p[2]),(1,.5,h*.35),.2,'detail')


def spring(a,b,r=5,turns=9):
 d=Vector(b)-Vector(a);axis=d.normalized();u=axis.cross(Vector((0,1,0)))
 if u.length<.1:u=axis.cross(Vector((1,0,0)))
 u.normalize();v=axis.cross(u)
 pts=[Vector(a)+d*(i/(turns*24))+r*(u*math.cos(T*i/24)+v*math.sin(T*i/24)) for i in range(turns*24+1)]
 g.wire('wound return spring',pts,.3,'detail')


def velvet_hammer():
 # Interrupted release ring: deliberately open for inspection, not a torus filler.
 views(B=(22,25),C=(32,33))
 for r in (91,104):ring('split carrier ring',(0,0,125),r,5,18,(0,-1,0),start=35,end=325)
 for a in range(45,326,35):
  x=98*math.cos(math.radians(a));z=125+98*math.sin(math.radians(a))
  joint((x,-23,z),6,(0,-1,0))
  rod('radial web',(x*.91,7,125+(z-125)*.91),(x*1.065,7,125+(z-125)*1.065),2,'detail')
 for i,a in enumerate((62,178,287)):
  with group('B') if i==0 else at():
   with at((96*math.cos(math.radians(a)),-17,125+96*math.sin(math.radians(a))),a-90,'Y'):
    box('load transfer saddle',(0,0,0),(43,30,18),6)
    for x in (-16,16):rod('cassette guide',(x,0,7),(x,0,42),2)
    ring('cam sector',(0,-5,25),15,5,8,(0,-1,0),start=15,end=270)
    joint((9,-17,30),4,(0,-1,0));rod('roller rocker',(9,-15,30),(20,-15,14),2)
    spring((-13,-18,10),(-13,-18,38),3,7)
    box('retaining jaw',(12,0,44),(22,16,9),3,'accent')
    cyl('release shaft',(0,-9,25),3,28,'detail',(0,1,0))
 with group('C'):
  instrument((62,-12,57),48,27)
  box('event strip magazine',(87,0,58),(20,29,32),4)
  for z in (48,57,66):box('record slot',(88,-16,z),(13,2,3),.5,'detail')
  tube('time-tag loom',[(60,0,47),(45,18,35),(5,20,30)],1)
  cyl('reset crown',(63,-15,35),5,5,'detail',(0,-1,0))
  # Paper feed and indexed spool expose the recorder's purpose.
  for x in (49,76):
   flange('paper roller bearing',(x,-20,51),5,(0,-1,0),2)
   cyl('paper roller',(x,-17,51),3,21,'detail',(0,1,0))
  for x in range(45,82,5):
   rod('time strip graduation',(x,-20,61),(x,-20,65 if x%10==0 else 63),.25,'detail')
  for z in range(47,72,4):box('spool case rib',(99,0,z),(2,23,1.5),.5,'detail')
  box('paper outlet',(60,-20,44),(25,3,5),1,'detail')
 for a in (35,325):
  x=98*math.cos(math.radians(a));z=125+98*math.sin(math.radians(a))
  box('split end termination',(x,-8,z),(14,27,14),4)
  cyl('end witness',(x,-24,z),3,3,'detail',(0,-1,0),6)
 mark('TRANSFER CAM',(-51,-14,172),'Takes the stored load before the jaw retracts.')
 mark('SPLIT RING',(-94,3,99),'Interrupted carrier; opening shown for inspection.')
 mark('RELEASE LOG',(68,-20,58),'Records the sequence, not a declaration of zero shock.')
 mark('RETAINING JAW',(50,-18,210),'A physical hold until the transfer path is engaged.')
 return 27,22


def bubble_bailiff():
 views(B=(25,40),C=(-22,26))
 # Thick sinuous channel walls with an open service side.
 path=[(-105,0,45),(-75,0,48),(-48,0,78),(30,0,95),(65,0,125),(35,0,158),(-42,0,177),(-62,0,207),(-22,0,229),(82,0,229)]
 for dy in (-14,14):organic_branch('formed channel rail',[(x,dy,z) for x,y,z in path],5)
 for i in range(1,len(path)-1):
  x,y,z=path[i];rod('channel cross rib',(x,-14,z),(x,14,z),2,'detail')
 for x,z in ((-100,45),(82,229)):flange('liquid line union',(x,0,z),13,(1,0,0));cyl('flow stub',(x,0,z),7,20,'structure',(1,0,0))
 with group('B'):
  box('membrane cassette',(-20,5,99),(73,38,15),6)
  for y in (-13,-6,1,8,15):rod('wick support',(-51,y,109),(12,y,109),.8,'detail')
  for x in range(-47,15,8):rod('capillary channel',(x,-15,110),(x,19,110),.4,'accent')
  for x in (-48,9):cyl('cassette retainer',(x,-13,111),2,3,'detail',n=6)
  flange('vent plenum outlet',(-18,21,99),8,(0,1,0))
 with group('C'):
  vessel('gas buffer',(63,30,25),20,49)
  flange('trap outlet',(63,30,78),9)
  cyl('isolation valve stem',(63,30,86),4,20,'detail')
  ring('manual vent wheel',(63,30,103),15,3,4)
  for a in (0,120,240):rod('wheel spoke',(63,30,105),(63+12*math.cos(math.radians(a)),30+12*math.sin(math.radians(a)),105),1,'detail')
  instrument((63,9,54),22,16)
 tube('gas-only riser',[(-18,29,99),(3,46,100),(51,49,95),(63,30,78)],1.2)
 for x,z in ((-74,49),(55,120)):
  box('isolated saddle foot',(x,8,15),(34,48,10),5)
  rod('channel support',(x,8,20),(x,8,z),3)
  flange('saddle adjuster',(x,8,22),6)
  rod('saddle brace',(x,8,z),(x,0,z),4)
 # Repeated formed ribs follow the actual channel rather than a bounding box.
 for a,b in zip(path,path[1:]):
  for f in (.25,.5,.75):
   q=Vector(a).lerp(Vector(b),f)
   rod('channel retention strap',(q.x,-14,q.z),(q.x,14,q.z),.9,'detail')
 mark('LIQUID PATH',(-83,0,49),'Sinuous wetted channel; cover omitted in this study.')
 mark('WICK CASSETTE',(-20,-10,108),'Surface chemistry is selected for this coolant.')
 mark('GAS BUFFER',(63,25,58),'Temporary gas hold before an authorised vent cycle.')
 mark('RETURN UNION',(82,0,229),'Bubble-free delivery is a target, not a certification.')
 return 27,18


def key_concord():
 views(B=(24,50),C=(-20,35))
 hull('waisted lock bed',[(-100,12,6,0),(-80,44,10,0),(0,32,10,0),(80,44,10,0),(100,12,6,0)])
 for x in (-64,64):
  cyl('equal authority barrel',(x,0,20),25,36)
  flange('barrel rim',(x,0,56),28)
  gear((x,0,63),23,20,axis=(0,0,1))
  box('key bow',(x,0,93),(30,9,24),8)
  rod('key shaft',(x,0,60),(x,0,88),3,'detail')
  for y in (-19,19):rod('carriage guide',(x-30,y,14),(x+30,y,14),2,'detail')
 with group('B'):
  box('coincidence yoke',(0,0,47),(46,28,12),5)
  for side in (-1,1):
   rod('equal-input lever',(side*17,0,52),(side*63,0,63),3)
   joint((side*17,-6,52),5,(0,1,0))
   box('blocking pawl',(side*10,-19,37),(9,12,16),2,'accent')
   spring((side*10,-20,26),(side*10,-20,41),2,6)
  cyl('coincidence pivot',(0,-18,47),5,36,'detail',(0,1,0))
 with group('C'):
  # Open casting exposes the bolt and return spring in A and C.
  for x in (-24,24):box('revocation side rail',(x,55,27),(6,64,22),3)
  for y in (27,83):box('revocation end bridge',(0,y,21),(50,8,12),3)
  box('witness bridge',(0,49,39),(45,8,7),2)
  for x in (-24,24):
   for y in (29,81):cyl('keeper fastener',(x,y,39),2,3,'detail',n=6)
  box('retractable bolt',(0,82,27),(21,48,12),3)
  for x in (-17,17):rod('return guide',(x,38,28),(x,88,28),2,'detail')
  spring((-17,43,28),(-17,76,28),4,8)
  cyl('manual return crown',(0,49,44),12,8,'detail')
  for a in range(0,360,45):rod('crown knurl',(10*math.cos(math.radians(a)),49+10*math.sin(math.radians(a)),44),(10*math.cos(math.radians(a)),49+10*math.sin(math.radians(a)),51),.6,'detail')
 rod('bolt transmission',(0,0,43),(0,54,43),4)
 for x in (-64,64):
  for z in (25,33,41):ring('barrel witness band',(x,0,z),25.3,.9,1,role='detail')
  for a in range(0,360,60):
   cyl('barrel mounting screw',(x+32*math.cos(math.radians(a)),32*math.sin(math.radians(a)),12),2,3,'detail',n=6)
  box('key identification inset',(x,-5,94),(17,1,11),3,'detail')
 mark('KEY ONE',(-64,0,89),'One input cannot manufacture the other person\'s consent.')
 mark('KEY TWO',(64,0,89),'Identical mechanical authority; no master cylinder.')
 mark('COINCIDENCE YOKE',(0,-10,50),'Both pawls must clear before the output can travel.')
 mark('WITHDRAWAL',(0,89,29),'Either input may withdraw before bolt release.')
 return 22,35


def metric_embassy():
 views(B=(28,33),C=(18,32))
 ring('open gauge carousel',(0,0,29),91,14,12,start=18,end=330)
 ring('carousel undercut',(0,0,17),82,6,10,start=18,end=330)
 for i,a in enumerate(range(40,330,40)):
  with at((73*math.cos(math.radians(a)),73*math.sin(math.radians(a)),42),a):
   with group('C') if i==0 else at():
    box('keyed adaptor shoe',(0,0,0),(26,30,8),4)
    cyl('coded connector',(0,0,5),10,20)
    ring('connector rim',(0,0,24),12,3,4)
    for j in range(5):cyl('contact pin',(5*math.cos(T*j/5),5*math.sin(T*j/5),27),.8,6,'detail',n=12)
    box('polarisation key',(10,0,17),(5,4,10),1,'accent')
    for z in (9,13,17):ring('thread crest',(0,0,z),10.6,.8,1,role='detail')
 gear((0,0,22),33,28,(0,0,1));cyl('carousel spindle',(0,0,0),12,46)
 for x,y in ((-62,-50),(63,-50),(0,70)):
  box('cast foot',(x,y,-8),(32,30,12),7)
  rod('carousel pedestal',(x,y,-2),(x,y,21),5)
  flange('pedestal collar',(x,y,0),9)
 # Actual radial spokes connect the index spindle to the interrupted rim.
 for a in (45,120,195,270):
  rod('carousel radial web',(25*math.cos(math.radians(a)),25*math.sin(math.radians(a)),23),(84*math.cos(math.radians(a)),84*math.sin(math.radians(a)),23),4,'detail')
 rod('scanner mast',(-92,24,5),(-92,24,139),7)
 organic_branch('arched measuring arm',[(-92,24,125),(-91,24,155),(-65,21,173),(-27,18,171),(9,8,150)],5)
 with group('B'):
  box('metrology head',(9,8,141),(48,31,27),8)
  for x in (-11,29):rod('probe slide',(x,8,126),(x,8,94),2,'detail')
  for x in (-11,29):box('three-wire jaw',(x,8,96),(13,20,7),2)
  for j in range(3):rod('reference wire',(-17+j*4,-1,99),(-17+j*4,17,99),.7,'accent')
  instrument((9,-10,145),35,19)
 tube('probe return loom',[(9,27,145),(-50,45,160),(-105,43,80),(-80,38,15)],1)
 mark('REFERENCE HEAD',(9,-6,144),'A fitted thread is not proof of electrical compatibility.')
 mark('ADAPTOR LIBRARY',(50,48,60),'Replaceable keyed cartridges, each with declared limits.')
 mark('GAUGE CAROUSEL',(-65,-34,37),'A physical sample precedes any software translation.')
 mark('DRIVE INDEX',(0,-8,25),'Indexing stops before the connector is presented.')
 return 28,28


def muon_customs():
 views(B=(23,24),C=(28,22))
 # Open-sided gantry. The absence of an emitter is intentional.
 for y in (-58,58):
  organic_branch('C frame casting',[(-118,y,30),(-139,y,42),(-144,y,92),(-144,y,224),(-130,y,265),(-97,y,280),(100,y,280)],9)
  box('stabilising shoe',(-127,y,12),(70,35,20),8)
 for z in (80,220):rod('gantry tie',(-145,-60,z),(-145,60,z),5)
 for level in (43,248):
  with group('B') if level==248 else at():
   for dz in (0,12):
    panel('tracking cassette',(0,0,level+dz),(207,119),nx=12,ny=4)
    for i in range(10):rod('scintillator strip',(-92+20*i,-53,level+dz+3),(-92+20*i,53,level+dz+3),1,'accent' if i%3==0 else 'detail')
    for x in (-109,109):box('readout spine',(x,0,level+dz),(9,122,9),2,'detail')
   for x in (-86,86):rod('drawer extraction bar',(x,-69,level+8),(x+15,-69,level+8),2,'detail')
 box('cargo pallet',(5,0,70),(160,102,14),5)
 box('sealed test crate',(10,0,122),(110,80,89),12,'shell')
 for x in (-36,55):box('cargo strap',(x,0,122),(4,83,92),1,'detail')
 with group('C'):
  box('coincidence clock rack',(-137,-82,137),(47,36,72),8)
  for z in (114,136,158):
   instrument((-137,-102,z),36,15)
   for x in (-148,-135,-122):cyl('timing connector',(x,-105,z-5),1.6,4,'detail',(0,-1,0))
  ribs((-137,-63,140),(34,5,57),8)
  tube('rack service pigtail',[(-124,-78,170),(-118,-74,181),(-107,-64,181)],1)
 tube('clock loom',[(-107,-64,181),(-108,-60,210),(-104,-61,250)],1)
 for y in (-58,58):
  for z in (43,253):rod('cassette attachment',(-145,y,z),(-104,y,z),4,'detail')
 for x in (-34,54):
  box('cargo strap buckle',(x,-43,131),(13,5,17),2,'detail')
  for z in (86,159):box('cargo edge protector',(10,-41,z),(93,3,6),2,'detail')
 box('manifest plate',(10,-44,128),(40,2,23),3,'detail')
 for i in range(6):rod('manifest code',(-3+i*5,-46,121),(-3+i*5,-46,135),.6,'detail')
 mark('UPPER TRACKER',(30,-40,262),'Two separated planes establish an incoming direction.')
 mark('LOWER TRACKER',(35,-40,46),'Outgoing track constrains scattering through cargo.')
 mark('CLOCK RACK',(-137,-104,139),'Event coincidence; the sky sets the arrival schedule.')
 mark('PASSIVE BAY',(10,-41,132),'Illustrative sealed test object. No X-ray emitter.')
 return 23,17


def resonance_tailor():
 views(B=(30,27),C=(-20,30))
 ring('split machine collar',(0,0,5),38,9,26,start=16,end=344)
 for x in (-38,38):box('clamp ear',(x,0,21),(22,27,13),4);cyl('clamp screw',(x,0,10),3,24,'detail')
 for x in (-57,57):rod('fork load spider',(0,9,30),(x,9,39),6)
 for i,(x,h) in enumerate(((-57,160),(0,205),(57,133))):
  with group('B') if i==1 else at():
   box('fork root',(x,9,44),(35,30,22),7)
   for dx in (-12,12):rod('parallel flexure',(x+dx,8,45),(x+dx,8,h),1.4,'detail')
   box('sliding mass',(x,8,h-24),(42,35,37),8)
   for y in (-12,28):box('mass cheek',(x,y,h-24),(45,4,28),2,'detail')
   cyl('tuning leadscrew',(x,8,51),2,h-37,'detail')
   for z in range(64,h,10):ring('screw witness',(x,8,z),2.9,.6,1,role='detail')
   instrument((x,-12,h-24),29,16)
   spring((x,23,53),(x,23,h-45),4,9)
   box('end stop',(x,8,h+7),(31,19,8),3)
 with group('C'):
  box('locking bridge',(0,-35,53),(61,32,14),5)
  for x in (-22,22):cyl('lock screw',(x,-35,55),3,24,'detail');ring('lock knob',(x,-35,78),9,3,4)
  rod('crossed flexure one',(-25,-54,30),(25,-54,67),1,'accent')
  rod('crossed flexure two',(25,-52,30),(-25,-52,67),1,'accent')
  box('travel stop',(0,-35,63),(14,18,11),2,'detail')
  for x in (-25,25):
   for z in (30,67):
    rod('flexure anchorage',(x,-54,z),(x,-35,53),2,'detail')
    cyl('flexure clamp',(x,-56,z),2.5,3,'detail',(0,-1,0),6)
 mark('CENTRE MASS',(0,-10,181),'Mass position changes the tuning of this branch.')
 mark('SHORT BRANCH',(57,8,109),'Three unequal branches target different narrow bands.')
 mark('LOCK BRIDGE',(0,-48,56),'Locking follows measurement, never a guess by ear.')
 mark('HOST CLAMP',(-35,-8,18),'Energy enters from the vibrating host structure.')
 return 27,21


def suture_loom():
 views(B=(18,39),C=(20,30))
 ring('open horseshoe',(0,0,42),91,12,15,start=12,end=327)
 ring('lower service track',(0,0,22),82,6,12,start=12,end=327)
 for a in (35,125,235,305):
  x=83*math.cos(math.radians(a));y=83*math.sin(math.radians(a));rod('track spacer',(x,y,23),(x,y,57),3)
 with group('B'):
  for side in (-1,1):
   motor((side*62,-16,53),11,24,(0,0,1))
   joint((side*52,-16,82),8,(0,0,1))
   rod('needle handoff arm',(side*52,-16,84),(side*12,-4,111),3)
   box('needle jaw',(side*10,-4,111),(12,14,9),3)
   for dx in (-3,3):rod('jaw finger',(side*10+dx,-4,112),(side*10+dx,6,119),.9,'detail')
  ring('test needle',(0,0,114),15,.8,1,(0,1,0),role='accent',start=12,end=168)
 with group('C'):
  cyl('thread spool',(61,57,60),21,31,'structure',(0,1,0))
  for y in (56,87):flange('spool cheek',(61,y,60),24,(0,1,0),3)
  for y in range(60,85,4):ring('wound thread',(61,y,60),21.3,.4,.6,(0,1,0),'detail')
  joint((31,70,82),6,(0,1,0));rod('dancer arm',(31,70,82),(22,70,103),2)
  spring((32,72,83),(47,72,102),2,6)
  instrument((64,42,81),29,17)
  box('spool bracket',(61,72,38),(52,38,8),4)
  rod('dancer pivot support',(31,70,40),(31,70,82),3)
  rod('spring return lug',(47,72,40),(47,72,102),1.5,'detail')
  rod('spool bearing pedestal',(61,73,38),(61,73,60),5)
 tube('tensioned thread',[(61,58,80),(24,70,104),(7,24,126),(0,0,127)],.35)
 panel('neutral test membrane',(0,5,89),(37,43),nx=5,ny=5,role='shell')
 for x in (-20,20):
  rod('membrane support',(x,63,50),(x,25,89),2,'detail')
  box('membrane clamp',(x,24,89),(6,12,7),2,'detail')
 for x,y in ((-68,43),(60,54),(-28,-72)):box('bench shoe',(x,y,5),(29,34,11),5);rod('bench stand',(x,y,10),(x,y,34),4)
 mark('DUAL NEEDLE GRIP',(-10,-4,114),'One gripper holds while the other repositions.')
 mark('THREAD DANCER',(25,70,101),'Slack is managed before the next transfer.')
 mark('TEST MEMBRANE',(0,5,89),'Neutral test sheet, not a claim of clinical readiness.')
 mark('OPEN SERVICE TRACK',(-78,0,49),'Cleaning access is part of the mechanism.')
 return 28,32


def round_bowl():
 profile=[(-38,22),(-36,28),(-32,34),(-25,40),(-15,43),(10,43),(23,41),(27,38)]
 n=96;vs=[(r*math.cos(T*j/n),r*math.sin(T*j/n),z) for z,r in profile for j in range(n)]
 fs=[(i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j) for i in range(len(profile)-1) for j in range(n)]
 fs.extend([tuple(reversed(range(n))),tuple(range((len(profile)-1)*n,len(profile)*n))])
 g.mesh('spun galley bowl',vs,fs)


def spin_table():
 views(B=(18,32),C=(15,36))
 for x in (-66,66):
  organic_branch('swept cradle leg',[(x,-38,5),(x,-32,30),(x,-15,65),(math.copysign(78,x),0,128)],6)
  box('magnetic galley foot',(x,-38,4),(47,38,12),8)
 ring('fixed gimbal hoop',(0,0,128),78,6,10,(0,1,0),start=0,end=360)
 with group('B'):
  joint((-79,-3,128),19,(1,0,0))
  motor((-114,-3,128),17,30,(1,0,0))
  gear((-78,-4,128),28,26,(1,0,0))
  instrument((-104,-24,106),29,18)
  rod('torque arm',(-97,-3,112),(-66,-15,70),3,'detail')
 with at((0,0,128),-26,'X'):
  # Spun round bowl; unlike a pump housing it has a circular food cavity.
  round_bowl()
  for z,r in ((-24,40),(10,43),(23,41)):
   ring('bowl rolled seam',(0,0,z),r+1,1.3,2,role='detail')
  for x in (-1,1):
   rod('rotor trunnion',(x*40,0,0),(x*78,0,0),7)
   flange('trunnion retainer',(x*67,0,0),12,(x,0,0))
  ring('inner stir boundary',(0,0,13),36,2,4,role='detail')
  with group('C'):
   ring('lid seal',(0,0,27),45,4,5)
   cyl('spun lid',(0,0,30),45,8)
   ring('lid rolled rim',(0,0,37),46,2,2,role='detail')
   for a in (25,145,265):
    rod('lid pressed rib',(19*math.cos(math.radians(a)),19*math.sin(math.radians(a)),39),(35*math.cos(math.radians(a)),35*math.sin(math.radians(a)),39),.6,'detail')
   for a in (0,120,240):
    with at((41*math.cos(math.radians(a)),41*math.sin(math.radians(a)),34),a):
     box('lid latch',(0,0,0),(17,10,12),3);joint((3,0,3),3,(0,1,0))
   ring('lid grip',(0,0,40),15,3,8,(0,1,0),start=0,end=180)
   cyl('pressure equalisation port',(22,0,40),4,7,'detail')
  rod('balance outrigger',(0,0,-34),(0,0,-102),5)
  for z in (-78,-87,-96):cyl('trim counterweight',(0,0,z),19,7,'detail')
 tube('cradle service cable',[(-106,8,121),(-99,26,73),(-66,20,28),(-66,-26,10)],1)
 mark('SEALED VESSEL',(0,-25,157),'A bowl-scale radial acceleration, not room gravity.')
 mark('DRIVE BEARING',(-100,-3,130),'Motor and opposing reaction return to the fixed cradle.')
 mark('BALANCE MASS',(0,-35,46),'Balance is checked with the declared ingredient load.')
 mark('LID INTERLOCK',(36,-14,162),'Transfer only after the rotor is stopped and isolated.')
 return 24,22

BUILDERS={101:velvet_hammer,103:bubble_bailiff,104:key_concord,105:metric_embassy,106:muon_customs,107:resonance_tailor,108:suture_loom,110:spin_table}
