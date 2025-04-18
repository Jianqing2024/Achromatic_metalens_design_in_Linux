import meep as mp

# 设置一个简单的模拟：1 μm 正方体真空中传播的平面波
cell = mp.Vector3(1, 1, 0)
sources = [mp.Source(mp.ContinuousSource(frequency=1.0),
                     component=mp.Ez,
                     center=mp.Vector3())]
sim = mp.Simulation(cell_size=cell,
                    boundary_layers=[mp.PML(0.1)],
                    sources=sources,
                    resolution=10)

sim.run(until=10)