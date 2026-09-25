#!/usr/bin/env python3
"""Ship both verified native formats in either branch, without raster resizing."""
import argparse,hashlib,json,shutil
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--source-root',type=Path,default=ROOT)
 a=p.parse_args();root=a.root.resolve();source=a.source_root.resolve()
 cat=json.loads((root/'docs/collection/catalog.json').read_text())
 release=json.loads((root/'docs/collection/release.json').read_text());default=release['format'];profiles=[]
 for fmt,size in [('wide',(5120,2160)),('16-9',(5120,2880))]:
  directory=root/'backgrounds' if fmt==default else root/'wallpaper-variants'/fmt
  directory.mkdir(parents=True,exist_ok=True);records=[]
  for e in cat['finalized']:
   src=source/e['source']
   if fmt=='16-9':src=src.parent/'16-9'/src.name if e['id'].startswith('o') else src.parent.parent/'16-9'/src.name
   dst=directory/src.name
   assert src.is_relative_to(source) and src.is_file(),src
   with Image.open(src) as im:assert im.size==size;im.verify()
   if not dst.exists() or sha(dst)!=sha(src):shutil.copy2(src,dst)
   records.append({'id':e['id'],'file':str(dst.relative_to(root)),'sha256':sha(dst)})
  profiles.append({'id':fmt,'label':'Ultrawide · 5K' if fmt=='wide' else '16:9 · 5K','size':list(size),'min_text_px':14,'layout':'full-triptych','readability_status':'native-resolution-reviewed','files':records})
 manifest={'version':1,'default':default,'count':len(cat['finalized']),'profiles':profiles,'pending_profiles':['1080p-readable','1440p-readable'],'note':'Current profiles preserve the full native 5K composition. Small-screen reflow is not yet published; do not imply that downscaling guarantees text legibility.'}
 (root/'docs/collection/profiles.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(f"PACKAGED: {len(profiles)} profiles × {len(cat['finalized'])} wallpapers; default {default}")
if __name__=='__main__':main()
