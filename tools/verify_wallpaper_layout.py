"""Audit glyph bounds against a render without text, before grain/bloom.

Grid/frame are the comparison baseline. Intentional identifiers inside their
own filled symbols are listed explicitly; no callout or legend is exempt.
Run from the repository root. Output includes every measured text string.
"""
import argparse,json,math,sys
from pathlib import Path
import numpy as np
ap=argparse.ArgumentParser();ap.add_argument('--size',default='5120x2160');ap.add_argument('--source',default='tools');ap.add_argument('--out',required=True);ap.add_argument('--style',default='starmap',choices=['starmap','original']);args=ap.parse_args()
sys.path.insert(0,str(Path('tools').resolve()));sys.path.insert(0,str(Path(args.source).resolve()))
import devices,foibles,leisure
from sheet import Sheet
from order import ORDER
size=tuple(map(int,args.size.split('x')));width,height=size
if abs(width/height-16/9)<.01:Sheet.side_inset=150
original_start=devices.start;original_leader=Sheet.leader;original_legend=Sheet.legend
labels=[];kind='text'
def text(self,t,x,y,size=8,track=.22,a=.7,align='l',bold=False,color=(.95,.965,.98),rot=0):
    glyphs=self._glyphs(t,size);adv=self._advances(glyphs,bold)
    w=sum(adv)+track*size*(len(glyphs)-1)
    px=-{'l':0,'r':w,'c':w/2}[align];m=self.c.get_matrix();m.translate(x,y);m.rotate(math.radians(rot));pts=[]
    for (ch,fs,dy),aw in zip(glyphs,adv):
        self.c.set_font_size(fs);e=self.c.text_extents(ch)
        if e.width and e.height:
            pts += [m.transform_point(u,v) for u in (px+e.x_bearing,px+e.x_bearing+e.width) for v in (dy+e.y_bearing,dy+e.y_bearing+e.height)]
        px+=aw+track*size
    if pts:labels.append({'text':t,'kind':kind,'box':[min(p[0] for p in pts),min(p[1] for p in pts),max(p[0] for p in pts),max(p[1] for p in pts)]})
    return w
def leader(self,*a,**kw):
    global kind
    before=kind;kind='callout';original_leader(self,*a,**kw);kind=before
def legend(self,*a,**kw):
    global kind
    before=kind;kind='legend';original_legend(self,*a,**kw);kind=before
def start(*a,**kw):
    s=original_start(*a,**kw);s.surface.flush()
    s._audit_base=np.frombuffer(s.surface.get_data(),np.uint8).reshape(height,width,4).copy()
    labels.clear();return s
Sheet.text=text;Sheet.leader=leader;Sheet.legend=legend
devices.start=start;foibles.start=start;leisure.start=start
inside_own_symbol={
 'air-refinery':{'AIR','CONTACTOR','WATER','ELECTROLYSER','SUNLIGHT','RECEIVER','ENZYME BEDS','CATALYST BEDS','JET FUEL'},
 'truth-lamp':{'14','9','0','22','17','11'},
 'organ-foundry':{'1','2','3','4','5','6'},
 'proxy':{'114','CITY 10K'},
}
fns=dict(devices.SHEETS+foibles.SHEETS+leisure.SHEETS);report=[]
if args.style=='starmap':
    from starmap import install
    install()
for name,_ in ORDER:
    labels=[];s=fns[name](size);s.surface.flush()
    arr=np.frombuffer(s.surface.get_data(),np.uint8).reshape(height,width,4)
    mask=np.abs(arr[:,:,:3].astype(np.int16)-s._audit_base[:,:,:3].astype(np.int16)).max(axis=2)>5
    issues=[];intentional=[];out_of_bounds=[]
    for t in labels:
        x0,y0,x1,y1=t['box']
        if x0<0 or y0<0 or x1>width or y1>height:out_of_bounds.append(t)
        hits=int(mask[max(0,math.floor(y0)):min(height,math.ceil(y1)),max(0,math.floor(x0)):min(width,math.ceil(x1))].sum())
        if hits:
            item=dict(t,geometry_pixels=hits)
            if t['kind']=='text' and t['text'] in inside_own_symbol.get(name,set()):intentional.append(item)
            else:issues.append(item)
    pairs=[]
    for i,a in enumerate(labels):
        for b in labels[i+1:]:
            if a['box'][0]<b['box'][2] and a['box'][2]>b['box'][0] and a['box'][1]<b['box'][3] and a['box'][3]>b['box'][1]:pairs.append([a['text'],b['text']])
    report.append({'name':name,'geometry_collisions':issues,'text_collisions':pairs,'out_of_bounds':out_of_bounds,'intentional_symbol_fills':intentional,'texts':labels})
    print(name,'geometry:',[(t['text'],t['geometry_pixels']) for t in issues],'text:',pairs,'outside:',len(out_of_bounds),flush=True)
Path(args.out).write_text(json.dumps({'size':size,'threshold':5,'sheets':report},indent=2)+'\n')
if any(s[k] for s in report for k in ('geometry_collisions','text_collisions','out_of_bounds')):
    sys.exit(1)
