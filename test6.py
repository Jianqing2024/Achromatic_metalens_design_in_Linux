import MeepMetalens as mm
import numpy as np

parameter=[0.4, 0.6, 0.3, 0.11, 0.12]
wav=0.532

fish=mm.Fishnet(parameter=parameter,wavelength=wav)
phase1, flux_val1=fish.benchmarkComputation()

L=np.linspace(0.25,0.4,10)
phase532=np.zeros_like(L)
trans532=np.zeros_like(L)

for i,l in enumerate(L):
    parameter[2]=l
    fish=mm.Fishnet(parameter=parameter,wavelength=wav)
    phase2, flux_val2=fish.Computation()
    phase532[i]=phase2-phase1
    trans532[i]=flux_val2[0]/flux_val1[0]

print(f'phase: {phase532}    trans532: {trans532}')