# Step 3.5g: Thrust changes with altitude -- the outside air pushes back on the nozzle
# Same flight as Step 3.5f. NEW: thrust = vacuum thrust - (outside air pressure x nozzle exit area)

import math
import numpy as np
import matplotlib.pyplot as plt
from atmosphere import us_standard_atmosphere, speed_of_sound

g = 9.82              # gravity [m/s^2]  (kept constant for now)
dt = 0.01             # time step [s]

# ---- the rocket ----
dry_mass = 200.0      # empty rocket [kg]
fuel = 800.0          # fuel [kg]
mdot = 10.0           # burn rate [kg/s]

# NEW: the engine is now described the way real engine data sheets do it
ve_vac = 1656.0                    # exhaust speed in VACUUM [m/s]
thrust_vac = mdot * ve_vac         # thrust in vacuum = 16560 N
exit_radius = 0.07                 # radius of the nozzle's opening [m]  (14 cm wide)
Ae = math.pi * exit_radius**2      # nozzle exit area = 0.0154 m^2

radius = 0.25                 # [m]
A = math.pi * radius**2       # front area [m^2]

# drag curve (same as Step 3.5f)
MACH_TABLE = [0.0,  0.6,  0.8,  0.9,  1.0,  1.1,  1.2,  1.5,  2.0,  3.0,  5.0]
CD_TABLE   = [0.30, 0.30, 0.32, 0.38, 0.50, 0.55, 0.54, 0.48, 0.40, 0.32, 0.25]

# ---- start on the pad ----
h = 0.0
v = 0.0
t = 0.0
m = dry_mass + fuel

ts, thrusts = [], []

# ---- PHASE 1: engine ON ----
burn_time = fuel / mdot
for i in range(round(burn_time / dt)):
    T, P, rho = us_standard_atmosphere(h)
    thrust = thrust_vac - P * Ae                  # NEW: outside air pressure P pushes back on the nozzle opening
    mach = v / speed_of_sound(T)
    Cd = np.interp(mach, MACH_TABLE, CD_TABLE)
    drag = 0.5 * rho * v**2 * Cd * A
    ts.append(t)
    thrusts.append(thrust / 1000)                 # in kN (1 kN = 1000 N)
    a = (thrust - m * g - drag) / m
    v = v + a * dt
    h = h + v * dt
    m = m - mdot * dt
    t = t + dt

print("thrust at liftoff  =", round(thrusts[0], 2), "kN")
print("thrust at engine off =", round(thrusts[-1], 2), "kN")
print("ENGINE OFF at t =", round(t), "s:  height =", round(h / 1000, 1), "km,  speed =", round(v), "m/s")

# ---- PHASE 2: engine OFF (no thrust, so nothing new here) ----
while v > 0:
    T, P, rho = us_standard_atmosphere(h)
    mach = v / speed_of_sound(T)
    Cd = np.interp(mach, MACH_TABLE, CD_TABLE)
    drag = 0.5 * rho * v**2 * Cd * A
    a = (- m * g - drag) / m
    v = v + a * dt
    h = h + v * dt
    t = t + dt

print("TOP OF FLIGHT at t =", round(t), "s:  height =", round(h / 1000, 1), "km")

# ---- PLOT: thrust vs time ----
plt.plot(ts, thrusts)
plt.xlabel("time [s]")
plt.ylabel("thrust [kN]")
plt.title("Step 3.5g: thrust grows as the air thins")
plt.grid()
plt.savefig("step3_5g_thrust_altitude.png")
plt.show()
