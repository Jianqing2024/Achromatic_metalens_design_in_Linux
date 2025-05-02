import MeepMetalens as mm
import numpy as np

parameter=[0.4, 0.6, 0.3, 0.11, 0.12]
wav=0.532

fish=mm.Fishnet(parameter=parameter,wavelength=wav)
phase1, flux_val1=fish.benchmarkComputation()
phase2, flux_val2=fish.Computation()