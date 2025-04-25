import meep as mp
import numpy as np
import MeepMetalens as mm

def mainfunction(radius, index):
    # === 单位设为微米 ===
    resolution = 80  # 每微米 50 像素，可调

    # === 材料常数 ===
    nsio2 = 1.4608
    ntio2 = 2.35
    sio2=mm.medium_from_nk(nsio2,0,1/0.532)
    tio2=mm.medium_from_nk(ntio2,0,1/0.532)

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
    
    # === 点相位监视器 ===
    monitor_point = mp.Vector3(0, 0, 1)
    dft_point = sim.add_dft_fields([mp.Ex], [frequency], where=mp.Volume(center=monitor_point, size=mp.Vector3()))
    flux_obj = sim.add_flux(
    frequency,  # 中心频率
    0,    # 频宽
    1,     # 频率个数（N=1 表示单频）
    mp.FluxRegion(
        center=mp.Vector3(z=1),           # 放在结构之后的某一平面上
        size=mp.Vector3(x=0.4, y=0.4)  # 横向截面尺寸
    )
)

    # === 运行仿真 ===
    sim.run(until=100)

    # === 提取相位 ===
    data = sim.get_dft_array(dft_point, num_freq=0, component=mp.Ex)
    phase = np.angle(data)  # 只一个点

    print(phase)
    return phase

radius=np.linspace(0.02,0.18,10)

referencePhase=mainfunction(0,0)
p=np.zeros_like(radius)
for i in range(len(radius)):
    p[i]=mainfunction(radius[i],1)-referencePhase
    
for i in range(len(p)):
    print(f"{p[i]};\n")