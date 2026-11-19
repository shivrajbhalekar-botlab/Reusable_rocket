# Step 3.5c: Fly straight up again (Step 3.5) -- but through the REAL air (Step 3.5b)

import math
import matplotlib.pyplot as plt
from atmosphere import us_standard_atmosphere     # NEW: use the function from our own file atmosphere.py

g = 9.82              # gravity [m/s^2]  (kept constant for now)
dt = 0.01             # time step [s]

# ---- the rocket (same as Step 3.5) ----
dry_mass = 200.0      # empty rocket [kg]
fuel = 800.0          # fuel [kg]
mdot = 10.0           # burn rate [kg/s]
ve = 1500.0           # exhaust speed [m/s]
thrust = mdot * ve    # 15000 N

radius = 0.25                 # [m]  (50 cm wide)
A = math.pi * radius**2       # front area [m^2]
Cd = 0.5                      # pointy-nosed rocket

# ---- start on the pad ----
h = 0.0
v = 0.0               # up is +
t = 0.0
m = dry_mass + fuel

on_t, on_h = [], []       # engine ON  (for the plot)
off_t, off_h = [], []     # engine OFF

# ---- PHASE 1: engine ON ----
burn_time = fuel / mdot
for i in range(round(burn_time / dt)):
    T, P, rho = us_standard_atmosphere(h)          # NEW: real air (we only need rho for now)
    drag = 0.5 * rho * v**2 * Cd * A
    a = (thrust - m * g - drag) / m
    v = v + a * dt
    h = h + v * dt
    m = m - mdot * dt
    t = t + dt
    on_t.append(t)
    on_h.append(h / 1000)

print("ENGINE OFF at t =", round(t), "s:  height =", round(h / 1000, 1), "km,  speed =", round(v), "m/s")

# ---- PHASE 2: engine OFF -- coast upward until it stops rising ----
while v > 0:
    T, P, rho = us_standard_atmosphere(h)          # NEW: real air
    drag = 0.5 * rho * v**2 * Cd * A
    a = (- m * g - drag) / m
    v = v + a * dt
    h = h + v * dt
    t = t + dt
    off_t.append(t)
    off_h.append(h / 1000)

print("TOP OF FLIGHT at t =", round(t), "s:  height =", round(h / 1000, 1), "km")

# ---- PLOT ----
plt.plot(on_t, on_h, "r", label="engine ON")
plt.plot(off_t, off_h, "b", label="engine OFF (coasting)")
plt.xlabel("time [s]")
plt.ylabel("height [km]")
plt.title("Step 3.5c: fly up through the REAL air")
plt.legend()
plt.grid()
plt.savefig("step3_5c_fly_real_air.png")
plt.show()
