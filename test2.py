import meep as mp
import numpy as np

# === 仿真参数 ===
resolution = 30  # 每微米像素数
dpml = 1.0       # z方向 PML 厚度
cell_x = 0.4     # 单元 x 周期
cell_y = 0.4     # 单元 y 周期
cell_z = dpml * 2 + 2.0  # z方向: PML + 结构 + 空隙

cell = mp.Vector3(cell_x, cell_y, cell_z)

# === 材料 ===
eps_sio2 = 2.1025
eps_tio2 = 6.25

# === 几何结构 ===
geometry = [
    mp.Block(size=mp.Vector3(cell_x, cell_y, 0.1),
             center=mp.Vector3(z=-0.05),
             material=mp.Medium(epsilon=eps_sio2)),
    mp.Cylinder(radius=0.01, height=0.6,
                center=mp.Vector3(z=0.3),
                material=mp.Medium(epsilon=eps_tio2))
]

# === 边界条件 ===
boundary_layers = [mp.PML(dpml, direction=mp.Z)]
# x/y方向默认是 periodic（不设置默认也是 periodic）

# === 源 ===
wavelength = 0.532
frequency = 1 / wavelength
source = mp.Source(mp.ContinuousSource(frequency=frequency),
                   component=mp.Ez,
                   center=mp.Vector3(z=-0.2),
                   size=mp.Vector3(cell_x, cell_y))

# === 创建仿真 ===
sim = mp.Simulation(
    cell_size=cell,
    boundary_layers=boundary_layers,
    geometry=geometry,
    sources=[source],
    resolution=resolution,
    default_material=mp.Medium(epsilon=1.0),
    dimensions=3,  # 明确声明 3D
    k_point=mp.Vector3()  # Gamma 点，即非倾斜入射
)

# === 添加监视器 ===
monitor_z = 0.8  # 柱子上方
monitor_size = mp.Vector3(cell_x, cell_y, 0)  # xy 面

sim.add_dft_fields([mp.Ez], [frequency],
                   where=mp.Volume(center=mp.Vector3(z=monitor_z), size=monitor_size))

# === 运行 ===
sim.run(until=400)

# === 提取 DFT 数据 ===
dft_obj = sim.add_dft_fields(
    [mp.Ez],
    [frequency],
    where=mp.Volume(center=mp.Vector3(z=monitor_z), size=monitor_size)
)

sim.run(until=400)

# 使用 dft_obj 来获取数据（不是 mp.Ez）
data = sim.get_dft_array(dft_obj, num_freq=0, component=mp.Ez)

amplitude = np.abs(data)
phase = np.angle(data)

print("相位范围:", phase.min(), "~", phase.max())