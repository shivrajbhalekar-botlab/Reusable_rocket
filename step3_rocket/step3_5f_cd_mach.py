# Step 3.5f: Cd changes with Mach -- the real "drag curve"
# Same flight as Step 3.5e. NEW: Cd is no longer fixed at 0.5; we read it from a table of Cd vs Mach.

import math
import numpy as np
import matplotlib.pyplot as plt
from atmosphere import us_standard_atmosphere, speed_of_sound

g = 9.82              # gravity [m/s^2]  (kept constant for now)
dt = 0.01             # time step [s]

# ---- the rocket (same as Step 3.5e) ----
dry_mass = 200.0      # empty rocket [kg]
fuel = 800.0          # fuel [kg]
mdot = 10.0           # burn rate [kg/s]
ve = 1500.0           # exhaust speed [m/s]
thrust = mdot * ve    # 15000 N

radius = 0.25                 # [m]
A = math.pi * radius**2       # front area [m^2]

# NEW: the drag curve -- Cd at a few Mach numbers (typical slender rocket; real ones come from wind tunnels / CFD)
MACH_TABLE = [0.0,  0.6,  0.8,  0.9,  1.0,  1.1,  1.2,  1.5,  2.0,  3.0,  5.0]
CD_TABLE   = [0.30, 0.30, 0.32, 0.38, 0.50, 0.55, 0.54, 0.48, 0.40, 0.32, 0.25]

# ---- start on the pad ----
h = 0.0
v = 0.0
t = 0.0
m = dry_mass + fuel

ts, qs, machs, cds = [], [], [], []

# ---- PHASE 1: engine ON ----
burn_time = fuel / mdot
for i in range(round(burn_time / dt)):
    T, P, rho = us_standard_atmosphere(h)
    mach = v / speed_of_sound(T)
    Cd = np.interp(mach, MACH_TABLE, CD_TABLE)    # NEW: look up Cd for this Mach (straight line between table points)
    q = 0.5 * rho * v**2
    drag = q * Cd * A
    ts.append(t)
    qs.append(q / 1000)
    machs.append(mach)
    cds.append(Cd)
    a = (thrust - m * g - drag) / m
    v = v + a * dt
    h = h + v * dt
    m = m - mdot * dt
    t = t + dt

# ---- PHASE 2: engine OFF ----
while v > 0:
    T, P, rho = us_standard_atmosphere(h)
    mach = v / speed_of_sound(T)
    Cd = np.interp(mach, MACH_TABLE, CD_TABLE)
    q = 0.5 * rho * v**2
    drag = q * Cd * A
    ts.append(t)
    qs.append(q / 1000)
    machs.append(mach)
    cds.append(Cd)
    a = (- m * g - drag) / m
    v = v + a * dt
    h = h + v * dt
    t = t + dt

k = qs.index(max(qs))
print("MAX Q =", round(qs[k], 1), "kPa at t =", round(ts[k]), "s,  Mach =", round(machs[k], 2), ", Cd =", round(cds[k], 2))
print("TOP OF FLIGHT at t =", round(t), "s:  height =", round(h / 1000, 1), "km")

# ---- PLOT: left = the drag curve (table), right = Cd during the flight ----
plt.subplot(1, 2, 1)
plt.plot(MACH_TABLE, CD_TABLE, "o-")       # dots = table points, lines = what np.interp uses in between
plt.xlabel("Mach number")
plt.ylabel("Cd")
plt.title("drag curve")
plt.grid()

plt.subplot(1, 2, 2)
plt.plot(ts, cds)
plt.axvline(burn_time, color="gray", linestyle="--")
plt.xlabel("time [s]")
plt.ylabel("Cd")
plt.title("Cd during the flight")
plt.grid()

plt.savefig("step3_5f_cd_mach.png")
plt.show()
