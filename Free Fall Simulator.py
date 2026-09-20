import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt

import matplotlib.animation as animation

fig, ax = plt.subplots(num="Free Fall Simulation")

# Controls Start

C_d = 0.34 # Drag Coefficient
rho = 1.225 # Fluid Density (kg/m^3)
M = 0.149 # Mass (kg)
r = 0.037338 # Radius (m)
A = np.pi * r**2 # Cross-Sectional Area (m^2)
g = 9.81 # Gravity (m/s^2)
z_0 = 0.0 # Initial Position (m)

Initial_Velocity = 10 # IDK What To Tell You, It's In The Name.

# Controls End
dz_dt = Initial_Velocity
v_t = np.sqrt(2 * M * g / (C_d * A * rho)) # Terminal Velocity (m/s)
z_peak = v_t**2 * np.log(np.abs(1 + dz_dt**2 / v_t**2))  / (2 * g) + z_0 # Maximum Height Of The Arc (m)
t_peak = v_t * np.arctan(dz_dt / v_t) / g # Time At The Peak Of The Arc (sec)
t_f = v_t * np.arccosh(np.exp(g * z_peak / v_t**2)) / g + t_peak # Time Of Impact (sec)

t_max = np.ceil(t_f + 0.2) # Run Time Of The Simulation (sec)

t = np.linspace(0, t_max, int(t_max * 24)) # Time (sec)

z_d = -v_t**2 * np.log(np.abs(np.cosh((t - t_peak) * g / v_t))) / g + z_peak # Position Along The z-Axis For Negative Motion
z_u = v_t**2 * np.log(np.abs(np.cos(np.arctan(dz_dt / v_t) - g * t / v_t)/ np.cos(np.arctan(dz_dt / v_t)))) / g + z_0 # Position Along The z-Axis For Positive Motion
z = np.where(t < t_peak, z_u, z_d) # Combines The Upward & Downward Motion

line = ax.plot(t[0], z[0], label=f'Drag Coefficient = {np.round(C_d,2)}\nInitial Velocity (z) = {np.round(dz_dt,2)}m/s\nInitial Height = {np.round(z_0,2)}m\nTime Of Impact = {np.round(t_f,2)}s\nMass = {np.round(M,2)}kg\nTerminal Velocity = {np.round(v_t,2)}m/s\n Maximum Height = {np.round(z_peak,2)}m')[0]
ax.set(xlim=(0, np.ceil(t_f * 1.2)), ylim=(0, 10 if np.ceil(z_peak * 1.25) < 10 else np.ceil(1.25 * z_peak)), xlabel='Time (s)', ylabel='Height (m)', title='Position-Time Graph')
ax.legend(fontsize="x-small")

def update(frame):
    
    line.set_xdata(t[:frame])
    line.set_ydata(z[:frame])
    return line

ani = animation.FuncAnimation(fig=fig, func=update, frames=int(t_max * 24), interval=24)
plt.show()