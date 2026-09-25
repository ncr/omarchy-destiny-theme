#!/usr/bin/env python3
"""Native-size Century sheets. All lettering remains deterministic Cairo type."""
import sys,json,math,time,argparse,os
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
from sheet import Sheet,WHITE,ARC,GOLD
from starmap_study import StudySheet
from PIL import Image
from century.registry import update
ASSETS=ROOT/'tools/assets/century';CAT=ROOT/'docs/century/catalog.json';OUT=ROOT/'concepts/century'

class CenturySheet(StudySheet):
    def primary_focus(self,gx,gy):
        shift=max(0,self.H-1080)*.35
        return self.role=='main' and abs(gx-self.cx)<215 and 240+shift<gy<600+shift
    def end_main(self):
        x,y=self._main_origin
        self.c.restore();self.role='secondary'
        self.view_label(self.cx,88,'A',self.entry['view_A'])
    def frame(self,sheet_no,total=100,code='NCR'):
        # Shared physical frame, three-digit collection numbering in the text layer.
        old=self.text
        def number_text(t,*a,**kw):
            if t==f'{code}-{sheet_no:02d}':t=f'{code}-{sheet_no:03d}'
            if t==f'SHEET {sheet_no:02d} / {total:02d}':t=f'SHEET {sheet_no:03d} / {total:03d}'
            return old(t,*a,**kw)
        self.text=number_text
        try:super().frame(sheet_no,total,code)
        finally:self.text=old


def draw_view(s,entry,key,cx,cy,width,height):
    d=json.loads((ASSETS/(entry['slug']+'-'+key+'.json')).read_text())
    # An authored camera roll presents elongated service rails diagonally,
    # without changing their geometry or shrinking their useful details.
    roll=math.radians(entry.get('view_'+key+'_roll',0))
    def turn(v):return [v[0]*math.cos(roll)-v[1]*math.sin(roll),v[0]*math.sin(roll)+v[1]*math.cos(roll)]
    if roll:
        for path in d['paths']:path['points']=[turn(v) for v in path['points']]
        d['anchors']={k:turn(v) for k,v in d.get('anchors',{}).items()}
    pts=[p for path in d['paths'] for p in path['points']]
    x0=min(x for x,y in pts);x1=max(x for x,y in pts);y0=min(y for x,y in pts);y1=max(y for x,y in pts)
    k=min(width/(x1-x0),height/(y1-y0));ox=(x0+x1)/2;oy=(y0+y1)/2
    def p(v):return(cx+(v[0]-ox)*k,cy+(v[1]-oy)*k)
    styles={'structure':(.89,.85,WHITE),'detail':(.69,.47,WHITE),'shell':(.48,.36,WHITE),
            'accent':(.86,.62,ARC),'cable':(.64,.47,GOLD),'figure':(.90,.80,WHITE)}
    from century.editorial import DATA
    from century.editorial_second import DATA as SECOND
    if entry['number'] in DATA or entry['number'] in SECOND or entry['number']>100:
        styles['detail']=(.79,.54,WHITE)
        styles['shell']=(.52,.38,WHITE)
    for path in d['paths']:
        a,w,col=styles.get(path['role'],(.56,.45,WHITE))
        s.poly([p(v) for v in path['points']],a,w,close=False,color=col)
    return {name:p(v) for name,v in d.get('anchors',{}).items()}


def callouts(s,entry,anchors,mx,my):
    notes=json.loads((ASSETS/(entry['slug']+'-meta.json')).read_text())['notes']
    order=sorted(anchors,key=lambda key:anchors[key][0]);n=len(order)//2
    for side,keys in ((-1,order[:n]),(1,order[n:])):
        keys.sort(key=lambda key:anchors[key][1])
        for i,key in enumerate(keys):
            x=mx+side*374;y=my-260+i*420/max(1,len(keys)-1)
            px,py=anchors[key]
            s.dot(px,py,1.35,.85)
            s.poly([(px,py),(x,y),(x+side*103,y)],.4,.43,close=False)
            align='r' if side<0 else 'l';tx=x+side*5
            s.text(key,tx,y-8,7.3,track=.14,a=.85,align=align)
            lines=s.wrap(notes[key],227,6,.035)
            for j,line in enumerate(lines):s.text(line,tx,y+13+j*10,6,track=.035,a=.62,align=align)


def compose(entry,size=(5120,2160),audit_hook=None):
    Sheet.side_inset=150 if size[0]/size[1]<2 else 0
    s=CenturySheet(*size,seed=entry['seed']);s.entry=entry;s.subject=entry['slug'];s.set_palette(entry['palette'])
    s.background();s.begin_lines();s.grid();s.frame(entry['number'],entry.get('series_total',100))
    if audit_hook:audit_hook(s)
    mx,my=s.cx-70,505
    s.begin_main(mx,my)
    anchors=draw_view(s,entry,'A',mx,my-15,660,665)
    callouts(s,entry,anchors,mx,my)
    s.end_main()
    if s.wide:
        from triptych import extra,caption_y,measured_illustration
        ex=extra(s);lx=390;rx=s.W-405
        with measured_illustration(s,'left'):
            draw_view(s,entry,'B',lx,241+ex*.225,370,290+ex*.25)
        s.view_label(lx,caption_y(s,'left'),'B',entry['view_B'],entry.get('view_B_note'))
        with measured_illustration(s,'right'):
            draw_view(s,entry,'C',rx,241+ex*.225,370,290+ex*.25)
        s.view_label(rx,caption_y(s,'right'),'C',entry['view_C'],entry.get('view_C_note'))
    enabled=[('FOUNDATION',entry['real_basis']),('STILL NEEDED',entry['required_breakthroughs'])]
    s.legend(entry['title'],entry['purpose'],entry['narrative'],enabled,entry['service_year'])
    from century.editorial import draw as draw_editorial
    draw_editorial(s,entry)
    from century.editorial_second import draw as draw_second
    draw_second(s,entry)
    from century.extension_editorial import draw as draw_extension
    draw_extension(s,entry)
    s.end_lines()
    return s


def main():
    p=argparse.ArgumentParser();p.add_argument('--ids',default='');p.add_argument('--domain');p.add_argument('--format',choices=['wide','16-9','both'],default='both');p.add_argument('--force',action='store_true');p.add_argument('--maintenance',action='store_true',help='Explicit later revision; bypass the one-night production deadline');a=p.parse_args()
    ids={int(x) for x in a.ids.split(',') if x};entries=json.loads(CAT.read_text())
    for entry in entries:
        if not ids and entry.get('curation',{}).get('status')=='rejected':continue
        if ids and entry['number'] not in ids:continue
        if a.domain and entry['domain']!=a.domain:continue
        if not entry.get('built'):continue
        for fmt,size in [('wide',(5120,2160)),('16-9',(5120,2880))]:
            if a.format not in (fmt,'both'):continue
            file=OUT/fmt/f"{entry['number']:03d}-{entry['slug']}.webp"
            if file.exists() and not a.force:continue
            if not a.maintenance and datetime.now(timezone.utc)>=datetime(2026,9,25,6,tzinfo=timezone.utc):print('DEADLINE',flush=True);return
            t=time.time();s=compose(entry,size)
            temporary=file.with_name('.'+file.stem+f'.{os.getpid()}.webp')
            s.save(temporary,glow=.15,grain=1.8);temporary.replace(file)
            im=Image.open(file);im.thumbnail((1600,900));im.save(OUT/'previews'/f"{entry['number']:03d}-{entry['slug']}-{fmt}.jpg",quality=92)
            entry.setdefault('rendered',{})[fmt]={'file':str(file.relative_to(ROOT)),'size':list(size),'seconds':round(time.time()-t,2)}
            entry['status']='rendered' if len(entry['rendered'])==2 else 'partially-rendered'
            update(entry['number'],{'rendered':entry['rendered'],'status':entry['status']})
            print('RENDERED',entry['number'],fmt,round(time.time()-t,2),flush=True)
if __name__=='__main__':main()
