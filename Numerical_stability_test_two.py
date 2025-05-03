import MeepMetalens as mm
import numpy as np
from scipy.io import savemat

parameter=[0.4, 0.6, 0.3, 0.11, 0.12]
wav=0.800

fish=mm.Fishnet(parameter=parameter,wavelength=wav)
phase1, flux_val1=fish.benchmarkComputation()

L=np.linspace(0.1,0.15,10)
phase532=np.zeros_like(L)
trans532=np.zeros_like(L)

for i,l in enumerate(L):
    parameter[4]=l
    fish=mm.Fishnet(parameter=parameter,wavelength=wav)
    phase2, flux_val2=fish.Computation()
    phase532[i]=phase2-phase1
    trans532[i]=flux_val2[0]/flux_val1[0]

data = {'phase800_py': phase532, 'trans800_py': trans532}

# 保存为 .mat 文件
savemat('/mnt/d/WORK/Achromatic_metalens_design_in_Windows/Numerical_stability_test/py_r_800.mat', data)