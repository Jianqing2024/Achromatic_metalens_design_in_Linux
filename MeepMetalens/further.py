import meep as mp
import numpy as np
from .basic import *

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


class Fishnet(mp.Simulation):
    def __init__(self, parameter, wavelength):
        p, h, l, w, r=parameter
        nsio2 = 1.4608
        ntio2 = 2.35
        sio2=medium_from_nk(nsio2,0,1/wavelength)
        tio2=medium_from_nk(ntio2,0,1/wavelength)
        
        pml_layers = [mp.PML(1, direction=mp.Z)]
        
        geometry=fishnetset(sio2, tio2, p, h, l, w, r)
    
        frequency = 1 / wavelength
        sources = [mp.Source(mp.ContinuousSource(frequency=frequency),
                            component=mp.Ex,
                            center=mp.Vector3(z=-0.5),
                            amplitude=1,
                            size=mp.Vector3(p, p))]

        super().__init__(
            cell_size=mp.Vector3(p, p, 4),
            geometry=geometry,
            sources=sources,
            resolution=50,
            boundary_layers=pml_layers,
            default_material=mp.Medium(epsilon=1.0),
            dimensions=3,
            symmetries=[],
            k_point=mp.Vector3())
        self.parameter=parameter
        self.wavelength=wavelength
        
    def benchmarkComputation(self):
        p=self.parameter[0]
        sources = [mp.Source(mp.ContinuousSource(frequency=1/self.wavelength),
                            component=mp.Ex,
                            center=mp.Vector3(z=-0.5),
                            amplitude=1,
                            size=mp.Vector3(p, p))]
        pml_layers = [mp.PML(1, direction=mp.Z)]
        
        sim=mp.Simulation(
            cell_size=mp.Vector3(p, p, 4),
            geometry=[],
            sources=sources,
            resolution=50,
            boundary_layers=pml_layers,
            default_material=mp.Medium(epsilon=1.0),
            dimensions=3,
            symmetries=[],
            k_point=mp.Vector3())
        
        point_monitor, plane_monitor=classicMonitorGroup(sim,self.parameter[0],1,self.wavelength)
        
        sim.run(until=100)
        
        data = sim.get_dft_array(point_monitor, num_freq=0, component=mp.Ex)
        phase = np.angle(data)
    
        flux_val = mp.get_fluxes(plane_monitor)
        
        return phase, flux_val
        
    def Computation(self):
        point_monitor, plane_monitor=classicMonitorGroup(self,self.parameter[0],1,self.wavelength)
        self.run(until=100)
        
        data = self.get_dft_array(point_monitor, num_freq=0, component=mp.Ex)
        phase = np.angle(data)
    
        flux_val = mp.get_fluxes(plane_monitor)
        
        return phase, flux_val