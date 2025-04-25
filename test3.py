import meep as mp
import numpy as np

def medium_from_nk(n: float, kappa: float, frequency: float):
    """
    根据复折射率 n + i*kappa 和频率，返回对应的 Meep 材料对象。

    参数:
        n        -- 实部折射率
        kappa    -- 虚部折射率（表示吸收）
        frequency -- 仿真频率 (单位与 Meep 仿真单位一致，通常是 1/μm)

    返回:
        mp.Medium 对象，包含等效的 epsilon 和 D_conductivity。
    """
    eps_complex = (n + 1j * kappa)**2
    eps_real = eps_complex.real
    eps_imag = eps_complex.imag
    D_cond = 2 * mp.pi * frequency * eps_imag

    return mp.Medium(epsilon=eps_real, D_conductivity=D_cond)

def mainfunction(radius, index):
    # === 单位设为微米 ===
    resolution = 80  # 每微米 50 像素，可调

    # === 材料常数 ===
    nsio2 = 1.4608
    ntio2 = 2.35
    
    sio2=medium_from_nk(nsio2,0,1/0.532)
    tio2=medium_from_nk(ntio2,0,1/0.532)

    # === 几何参数 ===
    substrate_size = mp.Vector3(0.4, 0.4, 0.1)
    cylinder_radius = radius
    cylinder_height = np.float64(0.6)

    # === 计算区域 ===
    dpml = 0.5
    zmin=-1.5
    zmax=1.5
    cell = mp.Vector3(0.4, 0.4, 5)

    # === 几何结构 ===
    if index==1:
        geometry = [
            mp.Block(
                size=substrate_size,
                center=mp.Vector3(z=-0.05),
                material=sio2
            ),
            mp.Cylinder(
                radius=cylinder_radius,
                height=cylinder_height,
                center=mp.Vector3(z=0.3),
                material=tio2
            )
        ]
    elif index==0:
        geometry = []

    # === 边界条件 ===
    pml_layers = [mp.PML(dpml, direction=mp.Z)]

    # === 源设置 ===
    wavelength = 0.532
    frequency = 1 / wavelength
    source_z = -0.1

    sources = [mp.Source(mp.ContinuousSource(frequency=frequency),
                         component=mp.Ex,
                         center=mp.Vector3(z=source_z),
                         amplitude=10,
                         size=mp.Vector3(substrate_size.x, substrate_size.y))]

    # === 点相位监视器 ===
    monitor_point = mp.Vector3(0, 0, 1)

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
    dft_point = sim.add_dft_fields([mp.Ex], [frequency], where=mp.Volume(center=monitor_point, size=mp.Vector3()))

    # === 运行仿真 ===
    sim.run(until=100)

    # === 提取相位 ===
    data = sim.get_dft_array(dft_point, num_freq=0, component=mp.Ex)
    phase = np.angle(data)  # 只一个点

    print(phase)
    return phase

radius=np.linspace(0.02,0.18,100)

referencePhase=mainfunction(0,0)
p=np.zeros_like(radius)
for i in range(len(radius)):
    p[i]=mainfunction(radius[i],1)-referencePhase
    
for i in range(len(p)):
    print(f"{p[i]};\n")