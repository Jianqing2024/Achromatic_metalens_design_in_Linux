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

def classicMonitorGroup(sim,xsize,z,waveLength):
    frequency=1/waveLength
    center = mp.Vector3(0, 0, z)
    plane = mp.Vector3(xsize,xsize)
    
    point_monitor = sim.add_dft_fields(
    [mp.Ex],        # 默认x方向极化
    [frequency],    # 单波长 
    where=mp.Volume(center=center, size=mp.Vector3()))
    
    plane_monitor = sim.add_flux(
    frequency,      # 中心频率
    0,              # 频宽（单频）
    1,              # 频率个数（N=1 表示单频）
    mp.FluxRegion(
    center=center,  # 放在结构之后的某一平面上
    size=plane      # 横向截面尺寸
    ))
    return point_monitor, plane_monitor

