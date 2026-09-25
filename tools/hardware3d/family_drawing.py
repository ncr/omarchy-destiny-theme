"""Shared page composition for individually modeled hardware assemblies."""
import os,json
from pathlib import Path
from functools import lru_cache
from sheet import WHITE,ARC,GOLD
ROOT=Path(__file__).resolve().parents[1]/'assets/hardware-family'
SUBJECTS={'greener','sky-racer','organ-foundry','air-refinery','aroma-organ','cortical-mesh','tether-climber','fusion-transport','volumetric-stage','bounder'}
def enabled(name):return name in SUBJECTS and os.environ.get('DESTINY_HARDWARE_SET','retro')=='retro'
@lru_cache(None)
def data(name):return json.loads((ROOT/(name+'.json')).read_text())
@lru_cache(None)
def labels():return json.loads((ROOT/'labels.json').read_text())
def draw(s,name,mx,my):
 d=data(name);pts=[p for path in d['paths'] for p in path['points']];x0=min(x for x,y in pts);x1=max(x for x,y in pts);y0=min(y for x,y in pts);y1=max(y for x,y in pts)
 scale=min(620/(x1-x0),695/(y1-y0));dx=-(x0+x1)/2*scale;dy=-(y0+y1)/2*scale-25
 c=s.c;c.save();c.translate(mx+dx,my+dy);c.scale(scale,scale)
 styles={'shell':(.39,.47,WHITE),'plate':(.87,1,WHITE),'structure':(.85,.86,WHITE),'detail':(.53,.43,WHITE),'accent':(.88,.65,ARC),'cable':(.57,.42,GOLD),'fine':(.40,.28,ARC),'hologram':(.60,.40,ARC),'figure':(.95,.95,WHITE),'grass':(.76,.60,WHITE),'radiator':(.66,.35,ARC)}
 for p in d['paths']:
  c.new_path();c.move_to(*p['points'][0])
  for point in p['points'][1:]:c.line_to(*point)
  a,w,col=styles[p['role']];s._stroke(a,w/max(.75,scale**.35),None,col)
 c.restore()
 annotation={v[0]:v[1] if len(v)>1 else None for v in labels()[name]}
 positions={lab:(x*scale+dx,y*scale+dy) for lab,(x,y) in d['anchors'].items()}
 ordered=sorted(positions,key=lambda lab:positions[lab][0]);split=len(ordered)//2
 from label_layout import LABEL_OFFSETS,COMPACT_OFFSETS
 for side,group in [(-1,ordered[:split]),(1,ordered[split:])]:
  group.sort(key=lambda lab:positions[lab][1])
  for i,lab in enumerate(group):
   x,y=positions[lab];ex=side*383;ey=-345+i*(550 if side<0 else 635)/max(1,len(group)-1)
   if name=='cortical-mesh' and lab=='MESH THREAD':ey-=22
   ox,oy=LABEL_OFFSETS.get(name,{}).get(lab,(0,0))
   if not s.wide:
    cx,cy=COMPACT_OFFSETS.get(name,{}).get(lab,(0,0));ox+=cx;oy+=cy
   s.leader(mx+x,my+y,ex-x-ox,ey-y-oy,side*95,lab,annotation.get(lab))
