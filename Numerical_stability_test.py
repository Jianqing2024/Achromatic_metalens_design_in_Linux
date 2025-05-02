import MeepMetalens as mm
import meep as mp
import numpy as np
import sqlite3
import os

def main(parameter,index):
    p, h, l, w, r=parameter[0], parameter[1], parameter[2], parameter[3], parameter[4]
    nsio2 = 1.4608
    ntio2 = 2.35
    sio2=mm.medium_from_nk(nsio2,0,1/0.532)
    tio2=mm.medium_from_nk(ntio2,0,1/0.532)
    
    if index==1:  
        geometry=mm.fishnetset(sio2, tio2, p, h, l, w, r)
    elif index==0:
        geometry=[]

    dpml = 1
    pml_layers = [mp.PML(dpml, direction=mp.Z)]

    wavelength = 0.532
    frequency = 1 / wavelength
    source_z = -0.1

    sources = [mp.Source(mp.ContinuousSource(frequency=frequency),
                        component=mp.Ex,
                        center=mp.Vector3(z=source_z),
                        amplitude=1,
                        size=mp.Vector3(p, p)
                        )
               ]
    sim = mp.Simulation(cell_size=mp.Vector3(p,p,4),
                        geometry=geometry,
                        sources=sources,
                        resolution=50,
                        boundary_layers=pml_layers,
                        default_material=mp.Medium(epsilon=1.0),
                        dimensions=3,
                        symmetries=[],
                        k_point=mp.Vector3()  # 周期性方向设置为 Gamma 点
                        )

    point_monitor, plane_monitor=mm.classicMonitorGroup(sim,p,0.8,wavelength)
    sim.run(until=100)

    data = sim.get_dft_array(point_monitor, num_freq=0, component=mp.Ex)
    phase = np.angle(data)
    flux_val = mp.get_fluxes(plane_monitor)

    return phase, flux_val
def findDataBase():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    data_dir = os.path.join(parent_dir, "data")
    db_path = os.path.join(data_dir, "structures.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    return cursor

cursor=findDataBase()
