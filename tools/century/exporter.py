"""Century hidden-line export with endpoint-complete visibility clipping.

Derived from the existing hardware family exporter. Keep the legacy collection
unchanged; Century fixes transitions in the final sampled interval of each edge.
"""
import bpy,math,json
from mathutils import Vector
from mathutils.bvhtree import BVHTree
import family_core as g

def export(name,az=27,el=20):
 parts,wires,anchors,OUT,STUDY=g.parts,g.wires,g.anchors,g.OUT,g.STUDY
 bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();vv=[];ff=[];owners=[];meshes=[]
 for o,role in parts:
  eo=o.evaluated_get(deps);m=eo.to_mesh();v=[o.matrix_world@p.co for p in m.vertices];f=[list(p.vertices) for p in m.polygons];off=len(vv)
  vv.extend(v);ff.extend([tuple(off+i for i in face) for face in f]);owners.extend([o.name]*len(f));meshes.append((o.name,role,v,f));eo.to_mesh_clear()
 bvh=BVHTree.FromPolygons(vv,ff,all_triangles=False)
 a,e=math.radians(az),math.radians(el);right=Vector((math.cos(a),math.sin(a),0));toward=Vector((math.sin(a)*math.cos(e),-math.cos(a)*math.cos(e),math.sin(e)));up=toward.cross(right)
 def xy(p):return [round(p.dot(right),4),round(-p.dot(up),4)]
 def seen(p,owner):
  hit=bvh.ray_cast(p+toward*3000,-toward,3002)
  return hit[0] is None or owners[hit[2]]==owner or (hit[0]-p).length<.35
 paths=[]
 def line(owner,pts,role):
  chain=[]
  def flush():
   if len(chain)>1:paths.append(dict(name=owner,points=chain.copy(),role=role))
  previous=None;state=False
  samples=[]
  for a,b in zip(pts,pts[1:]):
   n=max(1,math.ceil((b-a).length/1.1))
   samples.extend(a.lerp(b,k/n) for k in range(n))
  samples.append(pts[-1])
  for p in samples:
    visible=seen(p,owner)
    if previous is not None and visible!=state:
     lo,hi=previous,p
     for _ in range(8):
      mid=(lo+hi)*.5
      if seen(mid,owner)==state:lo=mid
      else:hi=mid
     q=xy((lo+hi)*.5)
     if state:chain.append(q);flush();chain=[]
     else:chain=[q]
    if visible:chain.append(xy(p))
    previous=p;state=visible
  flush()
 for owner,role,v,f in meshes:
  if role=='tube':continue
  edges={}
  for poly in f:
   normal=sum(((v[poly[j]]-v[poly[0]]).cross(v[poly[j+1]]-v[poly[0]]) for j in range(1,len(poly)-1)),Vector()).normalized()
   for a,b in zip(poly,poly[1:]+poly[:1]):edges.setdefault(tuple(sorted((a,b))),[]).append(normal)
  for (a,b),nn in edges.items():
   front=[n.dot(toward)>1e-6 for n in nn]
   if len(nn)==1 or any(front)!=all(front) or (len(nn)>1 and nn[0].dot(nn[1])<.75 and any(front)):line(owner,[v[a],v[b]],role)
 for owner,pts,role in wires:line(owner,pts,role)
 data=dict(paths=paths,anchors={label:xy(Vector(p)) for label,p in anchors.items()})
 (OUT/(name+'.json')).write_text(json.dumps(data,separators=(',',':'))+'\n')
 bpy.ops.object.camera_add(location=toward*1600+Vector((0,0,250)));cam=bpy.context.object;cam.rotation_euler=(-toward).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=900;bpy.context.scene.camera=cam
 bpy.ops.wm.save_as_mainfile(filepath=str(STUDY/(name+'.blend')))
 print(name,len(parts),'parts',len(paths),'paths',flush=True)
