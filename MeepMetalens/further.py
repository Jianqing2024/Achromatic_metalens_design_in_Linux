import meep as mp
import numpy as np

def fishnetset(materialBasic, materialStructure, p, h, l, w, r):
    basicHight=1
    basicCenter=mp.Vector3(x=0,y=0,z=(-basicHight+0)/2)
    basitSize= mp.Vector3(p, p, 1)
    
    structurecenter=mp.Vector3(x=0,y=0,z=(h+0)/2)
    
    basic=mp.Block(
        size=basitSize,
        center=basicCenter,
        material=materialBasic
    )
    
    cylinder=mp.Cylinder(
        center=structurecenter,
        radius=r,
        height=h,
        material=materialStructure
    )
    
    blockX=mp.Block(
        center=structurecenter,
        size=mp.Vector3(l,w,h),
        material=materialStructure
    )
    
    blockY=mp.Block(
        center=structurecenter,
        size=mp.Vector3(w,l,h),
        material=materialStructure
    )
    
    geometry = [basic,cylinder,blockX,blockY]
    
    return geometry