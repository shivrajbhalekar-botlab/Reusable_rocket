# Step 3.5d: "Max Q" -- the moment the air squeezes the rocket the hardest
# Same flight as Step 3.5c (real air). NEW: dynamic pressure q = 1/2 * rho * v^2, and find its biggest value.

import math
import matplotlib.pyplot as plt
from atmosphere import us_standard_atmosphere

g = 9.82              # gravity [m/s^2]  (kept constant for now)
dt = 0.01             # time step [s]

# ---- the rocket (same as Step 3.5c) ----
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

ts, hs, vs, qs = [], [], [], []   # time, height [km], speed, q [kPa] for the WHOLE flight

# ---- PHASE 1: engine ON ----
burn_time = fuel / mdot
for i in range(round(burn_time / dt)):
    T, P, rho = us_standard_atmosphere(h)
    q = 0.5 * rho * v**2          # NEW: dynamic pressure [Pa] = how hard the air presses on the nose
    drag = q * Cd * A             # drag is just q x Cd x A  (same formula as before)
    ts.append(t)
    hs.append(h / 1000)
    vs.append(v)
    qs.append(q / 1000)           # store in kPa (1 kPa = 1000 Pa)
    a = (thrust - m * g - drag) / m
    v = v + a * dt
    h = h + v * dt
    m = m - mdot * dt
    t = t + dt

# ---- PHASE 2: engine OFF ----
while v > 0:
    T, P, rho = us_standard_atmosphere(h)
    q = 0.5 * rho * v**2
    drag = q * Cd * A
    ts.append(t)
    hs.append(h / 1000)
    vs.append(v)
    qs.append(q / 1000)
    a = (- m * g - drag) / m
    v = v + a * dt
    h = h + v * dt
    t = t + dt

# ---- find Max Q (like the peak g in Step 2.6) ----
q_max = max(qs)                   # the biggest q of the whole flight
k = qs.index(q_max)               # at which slice it happened
print("MAX Q =", round(q_max, 1), "kPa  at t =", round(ts[k]), "s,  height =",
      round(hs[k], 1), "km,  speed =", round(vs[k]), "m/s")
print("TOP OF FLIGHT =", round(h / 1000, 1), "km")

# ---- PLOT: height (left) and q (right) vs time ----
plt.subplot(1, 2, 1)
plt.plot(ts, hs)
plt.axvline(burn_time, color="gray", linestyle="--")   # dashed line = engine off
plt.xlabel("time [s]")
plt.ylabel("height [km]")
plt.grid()

plt.subplot(1, 2, 2)
plt.plot(ts, qs)
plt.plot(ts[k], q_max, "ro")                            # red dot = Max Q
plt.axvline(burn_time, color="gray", linestyle="--")
plt.xlabel("time [s]")
plt.ylabel("q [kPa]")
plt.title("Max Q")
plt.grid()

plt.savefig("step3_5d_max_q.png")
plt.show()
