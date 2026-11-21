# Step 3.6b: TILT the rocket -- point the thrust a few degrees away from straight up
# Same as Step 3.6a. NEW: after 10 s the thrust leans 5 degrees toward the east, so part of it pushes SIDEWAYS.

import math
import numpy as np
import matplotlib.pyplot as plt
from atmosphere import us_standard_atmosphere, speed_of_sound

MU = 3.986004418e14   # [m^3/s^2]
RE = 6371e3           # [m]
dt = 0.01             # [s]

# ---- the rocket: Falcon 9-like (same as Step 3.6a) ----
m0 = 549000.0
fuel = 395700.0
n_engines = 9
thrust_vac = n_engines * 914000.0
ve_vac = 311.0 * 9.80665
mdot = thrust_vac / ve_vac
Ae = n_engines * 0.681
A = math.pi * 1.85**2

MACH_TABLE = [0.0,  0.6,  0.8,  0.9,  1.0,  1.1,  1.2,  1.5,  2.0,  3.0,  5.0]
CD_TABLE   = [0.30, 0.30, 0.32, 0.38, 0.50, 0.55, 0.54, 0.48, 0.40, 0.32, 0.25]

# NEW: the tilt plan
tilt_start = 10.0     # go straight up for the first 10 s (clear the launch tower)
tilt_deg = 5.0        # then lean 5 degrees toward the east (+x)

# ---- start on the pad ----
x = 0.0
y = RE
vx = 0.0
vy = 0.0
t = 0.0
m = m0

xs, hs = [], []

# ---- PHASE 1: engine ON ----
burn_time = fuel / mdot
for i in range(round(burn_time / dt)):
    r = math.sqrt(x**2 + y**2)
    h = r - RE
    speed = math.sqrt(vx**2 + vy**2)
    T, P, rho = us_standard_atmosphere(h)
    thrust = thrust_vac - P * Ae
    Cd = np.interp(speed / speed_of_sound(T), MACH_TABLE, CD_TABLE)
    drag = 0.5 * rho * speed**2 * Cd * A
    g = MU / r**2

    # NEW: which way does the thrust point?
    if t < tilt_start:
        tilt = 0.0                            # straight up
    else:
        tilt = math.radians(tilt_deg)         # degrees -> radians (math.cos/sin need radians)
    up_x, up_y = x / r, y / r                 # "up"       = away from Earth's centre
    side_x, side_y = y / r, -x / r            # "sideways" = 90 degrees from up, along the ground (east)
    dir_x = math.cos(tilt) * up_x + math.sin(tilt) * side_x     # mostly up ...
    dir_y = math.cos(tilt) * up_y + math.sin(tilt) * side_y     # ... plus a little sideways

    ax = (thrust / m) * dir_x - g * x / r     # thrust along the tilted direction, gravity down
    ay = (thrust / m) * dir_y - g * y / r
    if speed > 0:
        ax = ax - (drag / m) * vx / speed
        ay = ay - (drag / m) * vy / speed

    xs.append(x / 1000)
    hs.append(h / 1000)
    vx = vx + ax * dt
    vy = vy + ay * dt
    x = x + vx * dt
    y = y + vy * dt
    m = m - mdot * dt
    t = t + dt

r = math.sqrt(x**2 + y**2)
v_up = (vx * x + vy * y) / r                  # speed AWAY from Earth   (Step 2.5b)
v_side = (vx * y - vy * x) / r                # speed ALONG the ground  (Step 2.5b) -- this is what orbit needs
print("ENGINE OFF at t =", round(t), "s:  height =", round((r - RE) / 1000, 1), "km")
print("   up speed =", round(v_up), "m/s,   sideways speed =", round(v_side), "m/s,   orbit needs", round(math.sqrt(MU / r)), "m/s sideways")

# ---- PHASE 2: engine OFF -- coast while still moving away from Earth ----
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

    xs.append(x / 1000)
    hs.append(h / 1000)
    vx = vx + ax * dt
    vy = vy + ay * dt
    x = x + vx * dt
    y = y + vy * dt
    t = t + dt
    v_up = (vx * x + vy * y) / r

r = math.sqrt(x**2 + y**2)
print("TOP OF FLIGHT at t =", round(t), "s:  height =", round((r - RE) / 1000), "km,  downrange =", round(x / 1000), "km")

# ---- PLOT: the PATH -- height vs how far east we went ----
plt.plot(xs, hs)
plt.xlabel("east (downrange) [km]")
plt.ylabel("height [km]")
plt.title("Step 3.6b: tilted " + str(tilt_deg) + " degrees")
plt.grid()
plt.savefig("step3_6b_tilt.png")
plt.show()
