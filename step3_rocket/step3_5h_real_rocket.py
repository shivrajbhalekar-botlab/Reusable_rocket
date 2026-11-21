# Step 3.5h: REAL rocket numbers -- a Falcon 9-like first stage, flown straight up
# Same physics as Step 3.5g. NEW: only the NUMBERS change (approximate public data for Falcon 9 "Full Thrust").

import math
import numpy as np
import matplotlib.pyplot as plt
from atmosphere import us_standard_atmosphere, speed_of_sound

g = 9.82              # gravity [m/s^2]  (kept constant for now -- wrong up high, fixed in Step 3.6)
dt = 0.01             # time step [s]

# ---- the rocket: Falcon 9-like (approximate public numbers) ----
m0 = 549000.0                 # mass at liftoff, everything included [kg]
fuel = 395700.0               # first-stage propellant (kerosene + liquid oxygen) [kg]
dry_mass = m0 - fuel          # everything that is NOT first-stage fuel: empty 1st stage + full 2nd stage + payload [kg]

n_engines = 9                 # 9 Merlin 1D engines
thrust_vac_1 = 914000.0       # vacuum thrust of ONE engine [N]
isp_vac = 311.0               # vacuum Isp [s]   (Step 3.3: ve = Isp x 9.80665)
Ae_1 = 0.681                  # nozzle exit area of ONE engine [m^2]  (~0.93 m wide)

thrust_vac = n_engines * thrust_vac_1     # 8,226,000 N
ve_vac = isp_vac * 9.80665                # ~3050 m/s
mdot = thrust_vac / ve_vac                # ~2697 kg of propellant per second!
Ae = n_engines * Ae_1                     # all 9 nozzle openings [m^2]

radius = 1.85                 # rocket is 3.7 m wide [m]
A = math.pi * radius**2       # front area ~10.75 m^2

# drag curve (same typical slender-rocket table as Step 3.5f)
MACH_TABLE = [0.0,  0.6,  0.8,  0.9,  1.0,  1.1,  1.2,  1.5,  2.0,  3.0,  5.0]
CD_TABLE   = [0.30, 0.30, 0.32, 0.38, 0.50, 0.55, 0.54, 0.48, 0.40, 0.32, 0.25]

# ---- a few numbers BEFORE flying ----
thrust_liftoff = thrust_vac - 101325.0 * Ae
print("liftoff thrust =", round(thrust_liftoff / 1000), "kN,   thrust-to-weight =", round(thrust_liftoff / (m0 * g), 2))
print("burn rate =", round(mdot), "kg/s,   burn time =", round(fuel / mdot, 1), "s")
print("mass per front area: toy rocket =", round(1000.0 / (math.pi * 0.25**2)), "kg/m^2,   this rocket =", round(m0 / A), "kg/m^2")

# ---- start on the pad ----
h = 0.0
v = 0.0
t = 0.0
m = m0

ts, hs, qs, machs = [], [], [], []

# ---- PHASE 1: engine ON ----
burn_time = fuel / mdot
for i in range(round(burn_time / dt)):
    T, P, rho = us_standard_atmosphere(h)
    thrust = thrust_vac - P * Ae
    mach = v / speed_of_sound(T)
    Cd = np.interp(mach, MACH_TABLE, CD_TABLE)
    q = 0.5 * rho * v**2
    drag = q * Cd * A
    ts.append(t)
    hs.append(h / 1000)
    qs.append(q / 1000)
    machs.append(mach)
    a = (thrust - m * g - drag) / m
    v = v + a * dt
    h = h + v * dt
    m = m - mdot * dt
    t = t + dt

print("ENGINE OFF at t =", round(t), "s:  height =", round(h / 1000, 1), "km,  speed =", round(v), "m/s")

# ---- PHASE 2: engine OFF ----
while v > 0:
    T, P, rho = us_standard_atmosphere(h)
    mach = v / speed_of_sound(T)
    Cd = np.interp(mach, MACH_TABLE, CD_TABLE)
    q = 0.5 * rho * v**2
    drag = q * Cd * A
    ts.append(t)
    hs.append(h / 1000)
    qs.append(q / 1000)
    machs.append(mach)
    a = (- m * g - drag) / m
    v = v + a * dt
    h = h + v * dt
    t = t + dt

k = qs.index(max(qs))
print("MAX Q =", round(qs[k], 1), "kPa at t =", round(ts[k]), "s,  height =", round(hs[k], 1), "km,  Mach =", round(machs[k], 2))
print("TOP OF FLIGHT at t =", round(t), "s:  height =", round(h / 1000), "km")

# ---- PLOT: height (left) and q (right) ----
plt.subplot(1, 2, 1)
plt.plot(ts, hs)
plt.axvline(burn_time, color="gray", linestyle="--")
plt.xlabel("time [s]")
plt.ylabel("height [km]")
plt.grid()

plt.subplot(1, 2, 2)
plt.plot(ts, qs)
plt.plot(ts[k], qs[k], "ro")
plt.axvline(burn_time, color="gray", linestyle="--")
plt.xlabel("time [s]")
plt.ylabel("q [kPa]")
plt.title("Max Q")
plt.grid()

plt.savefig("step3_5h_real_rocket.png")
plt.show()
