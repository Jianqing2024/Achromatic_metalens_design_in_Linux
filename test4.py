import meep as mp
import numpy as np

def medium_from_nk(n: float, kappa: float, frequency: float) -> mp.Medium:
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

def main(radius,index):
    # === 单位设为微米 ===
    resolution = 50  # 每微米 50 像素，可调

    # === 材料常数 ===
    nsio2 = 1.4608
    ntio2 = 2.35
    
    sio2=medium_from_nk(nsio2,0,1/0.532)
    tio2=medium_from_nk(ntio2,0,1/0.532)

    # === 几何参数 ===
    substrate_size = mp.Vector3(0.4, 0.4, 0.1)
    cylinder_radius = radius
    cylinder_height = np.float64(0.1)

    # === 计算区域 ===
    dpml = 0.5
    zmin=-1.5
    zmax=1.5
    cell = mp.Vector3(0.4, 0.4, dpml)
    cellCenter = mp.Vector3(z=(-dpml-0.3+0.7+dpml)/2)
    
    # === 边界条件 ===
    pml_layers = [mp.PML(dpml, direction=mp.Z)]
    
    # === source ===
    lcen = 0.5  # center wavelength
    fcen = 1 / lcen  # center frequency
    df = 0.2 * fcen  # frequency width
    
    sources = [
            mp.Source(
                mp.GaussianSource(fcen, fwidth=df),
                component=mp.Ex,
                center=mp.Vector3(z=-0.25),
                size=mp.Vector3(x=0.4,y=0.4),
            )
        ]
    
    # === monitor ===
    monitor_point = mp.Vector3(0, 0, 0.7)
    
    sim = mp.Simulation(
            resolution=resolution,
            cell_size=cell_size,
            boundary_layers=pml_layers,
            k_point=k_point,
            default_material=glass,
            sources=sources,
            symmetries=symmetries,
        )    
    