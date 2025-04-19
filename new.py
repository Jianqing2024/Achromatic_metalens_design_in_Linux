import meep as mp
import numpy as np

# 定义仿真参数
resolution = 10  # 空间分辨率
cell_size = mp.Vector3(10, 10, 0)  # 仿真区域尺寸
pml_layers = [mp.PML(1.0)]  # 完美匹配层

# 定义材料
Si = mp.Medium(epsilon=12.0)

# 定义几何结构
geometry = [mp.Block(mp.Vector3(1, 1, mp.inf),
                     center=mp.Vector3(0, 0),
                     material=Si)]

# 定义源
sources = [mp.Source(mp.ContinuousSource(frequency=1.0),
                     component=mp.Ez,
                     center=mp.Vector3(-3, 0))]

# 定义仿真对象
sim = mp.Simulation(cell_size=cell_size,
                    boundary_layers=pml_layers,
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution)

# 运行仿真
sim.run(until=200)

# 获取仿真结果
ez_data = sim.get_array(center=mp.Vector3(0, 0), size=cell_size, component=mp.Ez)

# 可视化结果
import matplotlib.pyplot as plt
plt.imshow(np.abs(ez_data), cmap='hot')
plt.colorbar()
plt.show()