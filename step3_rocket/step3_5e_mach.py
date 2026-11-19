# Step 3.5e: Mach number -- how fast are we compared to the speed of sound?
# Same flight as Step 3.5d. NEW: speed of sound (depends on temperature) and Mach = v / a.

import math
import matplotlib.pyplot as plt
from atmosphere import us_standard_atmosphere, speed_of_sound    # NEW: also take speed_of_sound

g = 9.82              # gravity [m/s^2]  (kept constant for now)
dt = 0.01             # time step [s]

# ---- the rocket (same as Step 3.5d) ----
dry_mass = 200.0      # empty rocket [kg]
fuel = 800.0          # fuel [kg]
mdot = 10.0           # burn rate [kg/s]
ve = 1500.0           # exhaust speed [m/s]
thrust = mdot * ve    # 15000 N

radius = 0.25                 # [m]
A = math.pi * radius**2       # front area [m^2]
Cd = 0.5

# ---- start on the pad ----
h = 0.0
v = 0.0
t = 0.0
m = dry_mass + fuel

ts, hs, vs, qs, machs = [], [], [], [], []

# ---- PHASE 1: engine ON ----
burn_time = fuel / mdot
for i in range(round(burn_time / dt)):
    T, P, rho = us_standard_atmosphere(h)
    a_sound = speed_of_sound(T)   # NEW: speed of sound here [m/s]
    mach = v / a_sound            # NEW: Mach number (1 = speed of sound)
    q = 0.5 * rho * v**2
    drag = q * Cd * A
    ts.append(t)
    hs.append(h / 1000)
    vs.append(v)
    qs.append(q / 1000)
    machs.append(mach)
    a = (thrust - m * g - drag) / m
    v = v + a * dt
    h = h + v * dt
    m = m - mdot * dt
    t = t + dt

# ---- PHASE 2: engine OFF ----
while v > 0:
    T, P, rho = us_standard_atmosphere(h)
    a_sound = speed_of_sound(T)
    mach = v / a_sound
    q = 0.5 * rho * v**2
    drag = q * Cd * A
    ts.append(t)
    hs.append(h / 1000)
    vs.append(v)
    qs.append(q / 1000)
    machs.append(mach)
    a = (- m * g - drag) / m
    v = v + a * dt
    h = h + v * dt
    t = t + dt

# ---- 1. when do we go supersonic (pass Mach 1)? ----
for j in range(len(machs)):
    if machs[j] >= 1.0:
        break                     # NEW: 'break' = stop the loop right now; j stays at this slice
print("MACH 1 (supersonic) at t =", round(ts[j]), "s,  height =", round(hs[j], 1), "km,  speed =", round(vs[j]), "m/s")

# ---- 2. Mach number at Max Q ----
k = qs.index(max(qs))
print("MAX Q at t =", round(ts[k]), "s,  Mach =", round(machs[k], 2))

# ---- 3. fastest Mach of the flight ----
print("TOP MACH =", round(max(machs), 1))

# ---- PLOT: Mach vs time ----
plt.plot(ts, machs)
plt.axhline(1.0, color="red", linestyle=":")                 # dotted red line = speed of sound
plt.axvline(burn_time, color="gray", linestyle="--")         # dashed line = engine off
plt.xlabel("time [s]")
plt.ylabel("Mach number")
plt.title("Step 3.5e: Mach number")
plt.grid()
plt.savefig("step3_5e_mach.png")
plt.show()
