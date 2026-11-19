# Step 3.5: Fly straight up through the air -- engine ON, then engine OFF and coast to the top

import math
import matplotlib.pyplot as plt

g = 9.82              # gravity [m/s^2]  (kept constant for now)
dt = 0.01             # time step [s]

RHO0 = 1.225          # air density at sea level [kg/m^3]
H = 8500.0            # scale height [m]


def air_density(h):
    """Air density [kg/m^3] at height h [m] above the ground.  (Step 2.1)"""
    return RHO0 * math.exp(-h / H)


# ---- the rocket (same engine and tank as Step 3.3) ----
dry_mass = 200.0      # empty rocket [kg]
fuel = 800.0          # fuel [kg]
mdot = 10.0           # burn rate [kg/s]
ve = 1500.0           # exhaust speed [m/s]
thrust = mdot * ve    # 15000 N

# NEW for the rocket: its size and shape, for drag (Step 2.2)
radius = 0.25                 # [m]  (50 cm wide)
A = math.pi * radius**2       # front area [m^2]
Cd = 0.5                      # pointy-nosed rocket

# ---- start on the pad ----
h = 0.0
v = 0.0               # up is +
t = 0.0
m = dry_mass + fuel

# NEW (for the plot): empty lists to remember time and height in each phase
on_t, on_h = [], []       # engine ON
off_t, off_h = [], []     # engine OFF

# ---- PHASE 1: engine ON ----
burn_time = fuel / mdot
for i in range(round(burn_time / dt)):
    drag = 0.5 * air_density(h) * v**2 * Cd * A
    a = (thrust - m * g - drag) / m       # engine up, gravity down, drag DOWN (we're going up)
    v = v + a * dt
    h = h + v * dt
    m = m - mdot * dt
    t = t + dt
    on_t.append(t)            # remember this moment (for the plot)
    on_h.append(h / 1000)     # height in km

print("ENGINE OFF at t =", round(t), "s:  height =", round(h / 1000, 1), "km,  speed =", round(v), "m/s")

# ---- PHASE 2: engine OFF -- coast upward until it stops rising ----
while v > 0:
    drag = 0.5 * air_density(h) * v**2 * Cd * A
    a = (- m * g - drag) / m              # no thrust any more: only gravity and drag, both DOWN
    v = v + a * dt
    h = h + v * dt
    t = t + dt
    off_t.append(t)
    off_h.append(h / 1000)

print("TOP OF FLIGHT at t =", round(t), "s:  height =", round(h / 1000, 1), "km")

# ---- PLOT: height vs time, red = engine ON, blue = coasting ----
plt.plot(on_t, on_h, "r", label="engine ON")
plt.plot(off_t, off_h, "b", label="engine OFF (coasting)")
plt.xlabel("time [s]")
plt.ylabel("height [km]")
plt.title("Step 3.5: fly up, then coast to the top")
plt.legend()
plt.grid()
plt.savefig("step3_5_fly_up.png")
plt.show()
