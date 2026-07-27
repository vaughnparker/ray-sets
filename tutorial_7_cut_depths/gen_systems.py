#!/usr/bin/env python3
"""Emit all 16 axis systems, each as a list of orbits {label, rays}, to systems_data.js."""
import numpy as np, json
from jsonfmt import jdump
PHI=(1+5**0.5)/2
def Rmat(a,ang):
    a=np.array(a,float);a/=np.linalg.norm(a)
    K=np.array([[0,-a[2],a[1]],[a[2],0,-a[0]],[-a[1],a[0],0]])
    return np.eye(3)+np.sin(ang)*K+(1-np.cos(ang))*(K@K)
def mkey(M):return tuple(np.round(M,5).ravel())
def close(gens,cap=400):
    allg=list(gens)+[g.T for g in gens];E={mkey(np.eye(3)):np.eye(3)};fr=[np.eye(3)]
    while fr:
        nx=[]
        for M in fr:
            for g in allg:
                P=g@M;k=mkey(P)
                if k not in E:E[k]=P;nx.append(P)
                if len(E)>cap:return list(E.values())
        fr=nx
    return list(E.values())
O=close([Rmat([0,0,1],np.pi/2),Rmat([1,0,0],np.pi/2)])
T=close([Rmat([1,1,1],2*np.pi/3),Rmat([0,0,1],np.pi)])
I=close([Rmat([0,1,PHI],2*np.pi/5),Rmat([0,-1,PHI],2*np.pi/5)])
def axis_of(R):
    ang=np.arccos(np.clip((np.trace(R)-1)/2,-1,1))
    if ang<1e-6:return None
    if abs(ang-np.pi)<1e-4:
        M=(R+np.eye(3))/2;i=int(np.argmax(np.linalg.norm(M,axis=0)));v=M[:,i]
    else:v=np.array([R[2,1]-R[1,2],R[0,2]-R[2,0],R[1,0]-R[0,1]])
    return v/np.linalg.norm(v)
def vkey(v):return tuple(np.round(v,4))
def canon(v):
    for c in v:
        if abs(c)>1e-6:return v if c>0 else -v
    return v
def orbits(G):
    lines={}
    for R in G:
        v=axis_of(R)
        if v is None:continue
        cv=canon(v);lines[vkey(cv)]=cv
    rays=[]
    for cv in lines.values():rays+=[cv,-cv]
    orbs,seen=[],set()
    for u in rays:
        if vkey(u) in seen:continue
        orb={}
        for R in G:w=R@u;orb[vkey(w)]=w
        seen|=set(orb.keys());orbs.append(np.array(list(orb.values())))
    return sorted(orbs,key=len)          # ascending: faces, corners, edges
def rnd(o):return [[round(float(c),6) for c in v] for v in o]

Oo=orbits(O); Io=orbits(I); To=orbits(T)
# label by size within each family
NAME={"O":{6:"faces",8:"corners",12:"edges"},
      "I":{12:"faces",20:"corners",30:"edges"},
      "T":{4:"corners",6:"edges"}}
def orb(fam, sizes):
    src={"O":Oo,"I":Io,"T":To}[fam]
    out=[]
    for s in sorted(sizes):
        for o in src:
            if len(o)==s:
                out.append({"label":NAME[fam][s]+f" ({s})","rays":rnd(o)})
                break                      # one orbit per size (tetra has two size-4)
    return out

SYSTEMS={
 # elementary (names match piece_table.js keys for exact lookup)
 "Tetrahedron - corners (Pyraminx)": orb("T",{4}),
 "Cube - faces (Rubik's Cube)": orb("O",{6}),
 "Cube - corners (Skewb)": orb("O",{8}),
 "Cube - edges (Helicopter)": orb("O",{12}),
 "Dodecahedron - faces (Megaminx)": orb("I",{12}),
 "Dodecahedron - corners (Radiolarian)": orb("I",{20}),
 "Dodecahedron - edges": orb("I",{30}),
 # compound
 "Tetrahedron - corners + edges": orb("T",{4,6}),
 "Cube - faces + corners": orb("O",{6,8}),
 "Cube - faces + edges": orb("O",{6,12}),
 "Cube - corners + edges": orb("O",{8,12}),
 "Cube - faces + corners + edges": orb("O",{6,8,12}),
 "Dodeca - faces + corners": orb("I",{12,20}),
 "Dodeca - faces + edges": orb("I",{12,30}),
 "Dodeca - corners + edges": orb("I",{20,30}),
 "Dodeca - faces + corners + edges": orb("I",{12,20,30}),
}
for k,v in SYSTEMS.items():
    print(k, "->", [o["label"] for o in v], "=", sum(len(o["rays"]) for o in v),"rays")
with open("systems_data.js","w",encoding="utf-8") as f:
    f.write("const SYSTEMS = "+jdump(SYSTEMS)+";\n")
print("wrote systems_data.js")
