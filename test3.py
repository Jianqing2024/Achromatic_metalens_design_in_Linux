import meep as mp
import numpy as np

# === 单位设为微米 ===
resolution = 50  # 每微米 50 像素，可调

# === 材料常数 ===
eps_sio2 = 2.1025
eps_tio2 = 6.25

# === 几何参数 ===
substrate_size = mp.Vector3(0.4, 0.4, 0.1)
cylinder_radius = 0.1
cylinder_height = 0.6

# === 计算区域 ===
dpml = 1.0
cell_z = dpml * 2 + 2  # 多加点空隙
cell = mp.Vector3(0.4, 0.4, 3)

# === 几何结构 ===
geometry = [
    mp.Block(
        size=substrate_size,
        center=mp.Vector3(z=-0.05),
        material=mp.Medium(epsilon=eps_sio2)
    ),
    mp.Cylinder(
        radius=cylinder_radius,
        height=cylinder_height,
        center=mp.Vector3(z=0.3),
        material=mp.Medium(epsilon=eps_tio2)
    )
]

# === 边界条件 ===
pml_layers = [mp.PML(dpml, direction=mp.Z)]

# === 源设置 ===
wavelength = 0.532
frequency = 1 / wavelength
source_z = -0.2

sources = [mp.Source(mp.ContinuousSource(frequency=frequency),
                     component=mp.Ez,
                     center=mp.Vector3(z=source_z),
                     amplitude=10,
                     size=mp.Vector3(substrate_size.x, substrate_size.y))]

# === 点相位监视器 ===
monitor_point = mp.Vector3(0, 0, 0.7)

sim = mp.Simulation(
    cell_size=cell,
    geometry=geometry,
    sources=sources,
    resolution=resolution,
    boundary_layers=pml_layers,
    default_material=mp.Medium(epsilon=1.0),
    dimensions=3,
    symmetries=[],
    k_point=mp.Vector3()  # 周期性方向设置为 Gamma 点
)

# 添加 DFT 点监视器
dft_point = sim.add_dft_fields([mp.Ez], [frequency], where=mp.Volume(center=monitor_point, size=mp.Vector3()))

# === 运行仿真 ===
sim.run(until=400)

# === 提取相位 ===
data = sim.get_dft_array(dft_point, num_freq=0, component=mp.Ez)
phase = np.angle(data)  # 只一个点
print(phase)