"""Independent poster-content interpretation: serviceable radial quantum engine."""
import json
from pathlib import Path
from functools import lru_cache
from sheet import WHITE,ARC,GOLD
@lru_cache(None)
def data(view):return json.loads((Path(__file__).resolve().parents[1]/'assets/radial-quantum'/f'{view}.json').read_text())

def paths(s,d,tx,ty,scale):
 c=s.c;c.save();c.translate(tx,ty);c.scale(scale,scale)
 styles={'shell':(.44,.5,WHITE),'plate':(.88,1.05,WHITE),'structure':(.87,.85,WHITE),'detail':(.5,.4,WHITE),'accent':(.88,.62,ARC),'cable':(.62,.43,GOLD),'fine':(.42,.28,ARC)}
 for p in d['paths']:
  pts=p['points'];c.new_path();c.move_to(*pts[0])
  for point in pts[1:]:c.line_to(*point)
  a,w,col=styles[p['role']];s._stroke(a,w,None,col)
 c.restore()

def main(s,mx,my):
 d=data('main');sc=1.03;dy=273
 paths(s,d,mx-22,my+dy,sc)
 labels=[('PULSE-TUBE COOLERS', 'CLOSED-CYCLE / NO LIQUID HELIUM',355,-400),('4 K CONTROLLERS','LOCAL CONTROL / SHORT COLD LINKS',365,-243),('OPTICAL INTERCONNECT','ENTANGLEMENT BETWEEN CRYOSTATS',370,-78),('COMPUTE CASSETTES','6 × 1 700 LOGICAL QUBITS',370,85),('8 mK MANIFOLD','COMMON COLD CORE',-360,97),('NESTED THERMAL SHIELDS','50 K / 4 K / 100 mK',-360,-309),('VACUUM ENCLOSURE','UPPER SECTOR REMOVED FOR CLARITY',-360,-112),('SERVICE CARRIAGE','WITHDRAW COMPLETE COLD ASSEMBLY',-320,364)]
 from label_layout import LABEL_OFFSETS
 for name,sub,ex,ey in labels:
  x,y=d['anchors'][name];x=x*sc-22;y=y*sc+dy
  ox,oy=LABEL_OFFSETS.get('quantum-simulator',{}).get(name,(0,0))
  s.leader(mx+x,my+y,ex-x-ox,ey-y-oy,90 if ex>0 else -90,name,sub)

def detail(s,qx,qy):
 d=data('detail');ps=[p for path in d['paths'] for p in path['points']];cx=(min(x for x,y in ps)+max(x for x,y in ps))/2;cy=(min(y for x,y in ps)+max(y for x,y in ps))/2
 sc=2.7;paths(s,d,qx-cx*sc,qy-cy*sc,sc)
 s.view_label(qx,qy+183,'C','COMPUTE CASSETTE','ONE OF SIX / COLD TILE + OPTICAL TERMINATION')
