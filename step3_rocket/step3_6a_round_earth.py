# Step 3.6a: Put the real rocket on the ROUND Earth (2D, like Step 1.4) -- still flying straight up
# Same rocket as Step 3.5h. NEW: position (x, y) around Earth's centre, and real gravity g = MU / r^2.

import math
import numpy as np
import matplotlib.pyplot as plt
from atmosphere import us_standard_atmosphere, speed_of_sound

MU = 3.986004418e14   # Earth's gravity constant [m^3/s^2]  (Step 1.1)
RE = 6371e3           # Earth's radius [m]
dt = 0.01             # time step [s]

# ---- the rocket: Falcon 9-like (same as Step 3.5h) ----
m0 = 549000.0
fuel = 395700.0
n_engines = 9
thrust_vac = n_engines * 914000.0         # [N]
ve_vac = 311.0 * 9.80665                  # Isp 311 s -> ~3050 m/s
mdot = thrust_vac / ve_vac                # ~2697 kg/s
Ae = n_engines * 0.681                    # all nozzle openings [m^2]
A = math.pi * 1.85**2                     # front area [m^2]

MACH_TABLE = [0.0,  0.6,  0.8,  0.9,  1.0,  1.1,  1.2,  1.5,  2.0,  3.0,  5.0]
CD_TABLE   = [0.30, 0.30, 0.32, 0.38, 0.50, 0.55, 0.54, 0.48, 0.40, 0.32, 0.25]

# ---- start on the pad: at the TOP of the Earth (like Step 1.5) ----
x = 0.0
y = RE
vx = 0.0
vy = 0.0
t = 0.0
m = m0

ts, hs = [], []

# ---- PHASE 1: engine ON ----
burn_time = fuel / mdot
for i in range(round(burn_time / dt)):
    r = math.sqrt(x**2 + y**2)                # distance from Earth's centre
    h = r - RE                                # height above the ground
    speed = math.sqrt(vx**2 + vy**2)
    T, P, rho = us_standard_atmosphere(h)
    thrust = thrust_vac - P * Ae
    Cd = np.interp(speed / speed_of_sound(T), MACH_TABLE, CD_TABLE)
    drag = 0.5 * rho * speed**2 * Cd * A
    g = MU / r**2                             # NEW: real gravity, gets weaker as we go up

    # thrust points straight UP = away from Earth's centre = direction (x/r, y/r)
    # gravity points DOWN = towards Earth's centre = direction (-x/r, -y/r)      (Step 1.4)
    ax = (thrust / m) * x / r - g * x / r
    ay = (thrust / m) * y / r - g * y / r

    # drag points opposite to the velocity (Step 2.3) -- only once we are moving (no dividing by 0)
    if speed > 0:
        ax = ax - (drag / m) * vx / speed
        ay = ay - (drag / m) * vy / speed

    ts.append(t)
    hs.append(h / 1000)
    vx = vx + ax * dt
    vy = vy + ay * dt
    x = x + vx * dt
    y = y + vy * dt
    m = m - mdot * dt
    t = t + dt

r = math.sqrt(x**2 + y**2)
print("ENGINE OFF at t =", round(t), "s:  height =", round((r - RE) / 1000, 1), "km,  speed =",
      round(math.sqrt(vx**2 + vy**2)), "m/s")

# ---- PHASE 2: engine OFF -- coast while we are still moving AWAY from Earth ----
v_up = (vx * x + vy * y) / r                  # speed straight up (the "away" speed from Step 2.5b)
while v_up > 0:
    r = math.sqrt(x**2 + y**2)
    h = r - RE
    speed = math.sqrt(vx**2 + vy**2)
    T, P, rho = us_standard_atmosphere(h)
    Cd = np.interp(speed / speed_of_sound(T), MACH_TABLE, CD_TABLE)
    drag = 0.5 * rho * speed**2 * Cd * A
    g = MU / r**2

    ax = - g * x / r
    ay = - g * y / r
    if speed > 0:
        ax = ax - (drag / m) * vx / speed
        ay = ay - (drag / m) * vy / speed

    ts.append(t)
    hs.append(h / 1000)
    vx = vx + ax * dt
    vy = vy + ay * dt
    x = x + vx * dt
    y = y + vy * dt
    t = t + dt
    v_up = (vx * x + vy * y) / r

r = math.sqrt(x**2 + y**2)
print("TOP OF FLIGHT at t =", round(t), "s:  height =", round((r - RE) / 1000), "km")
print("gravity at the top =", round(MU / r**2, 2), "m/s^2   (9.82 on the ground)")

# ---- PLOT: height vs time ----
plt.plot(ts, hs)
plt.axvline(burn_time, color="gray", linestyle="--")
plt.xlabel("time [s]")
plt.ylabel("height [km]")
plt.title("Step 3.6a: straight up on the round Earth")
plt.grid()
plt.savefig("step3_6a_round_earth.png")
plt.show()
