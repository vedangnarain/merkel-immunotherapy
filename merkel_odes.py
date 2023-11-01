#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Wed Nov  1 09:23:49 2023

@author: Vedang Narain (vedang.narain@msdtc.ox.ac.uk)

"""

# Import the libraries
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Define the system of ODEs
def system_of_odes(t, y):
    N = y[0]
    T = y[1]
    dydt = [r*(N/A-1)*(1-N/K)*N-zeta*N*T, 
            phiT+alpha*N*T-q*T]  # Example: y1' = y2, y2' = -2*y1 - y2
    return dydt

'''
# Define David's parameters
r = 0.01;  # cancer growth rate
K=1;  # carrying capacity
A = 0.1;  # Allee effect
#zeta = 0.007;  # immune killing 
phiT = 0.01;  # natural immune influx
alpha = 0.01;  # cancer-induced recruitment 
q = 0.01;  # natural immune cell death
epsilon = 0.5;  # zeta for type-2 killing
'''

# Define the literature parameters
r = 0.514;  # cancer growth rate
#K=1/1.02e-09;  # carrying capacity
#zeta = 0.007;  # immune killing 
q = 2.0e-2+3.42e-10;  # natural immune cell death
#epsilon = 0.5;  # zeta for type-2 killing

# Think about other parameters
K=1/1.02e-09;  # carrying capacity
A = 0.1*K;  # Allee effect
phiT = r;  # natural immune influx
alpha = 0;  # cancer-induced recruitment 

# Define the initial conditions
N0 = 7*K/10  # initial Merkel cell population
T0 = 0  # initial immune cell population
initial_conditions = [N0, T0]  # Initial values for y1 and y2

# Define the time span over which you want to integrate
start = 0
stop = 3000
steps = 1000
t_span = [start, stop]


# Define z_values
zeta_values = np.logspace(-4, -1, 10)

# Plot the solution
#plt.plot(t, immune, label='immune')
plt.xlabel('days')
plt.ylabel('number of cancer cells')
for i, zeta in enumerate(zeta_values):
    print(i)
    solution = solve_ivp(system_of_odes, t_span, initial_conditions, t_eval=np.linspace(start, stop, steps))
    t = solution.t
    cancer = solution.y[0]
    immune = solution.y[1]
    plt.plot(t, cancer, label= round(zeta,4))

#plt.ylim(0,1)
plt.xlim(start, stop)
plt.legend()
plt.show()
