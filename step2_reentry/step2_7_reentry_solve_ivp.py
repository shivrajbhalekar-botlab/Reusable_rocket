# Step 2.7: The same reentry, with solve_ivp -- and an "event" to stop at the ground

import math
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

MU = 3.986004418e14   # Earth's gravity strength [m^3/s^2]
RE = 6371e3           # Earth's radius [m]
G0 = 9.81             # 1 g [m/s^2]

RHO0 = 1.225          # air density at sea level [kg/m^3]
H = 8500.0            # scale height [m]


def air_density(h):
    """Air density [kg/m^3] at height h [m] above the ground.  (Step 2.1)"""
    return RHO0 * math.exp(-h / H)


# ---- the ball (same as Step 2.2) ----
m = 1.0                    # mass [kg]
radius = 0.1               # [m]
A = math.pi * radius**2    # front area [m^2]
Cd = 0.47                  # sphere


# ---- 1. The physics: gravity + drag (Step 1.8 + Step 2.4) ----
def dynamics(t, state):
    x, y, vx, vy = state
    r = math.sqrt(x**2 + y**2)
    g = MU / r**2
    rho = air_density(r - RE)
    speed = math.sqrt(vx**2 + vy**2)
    drag = 0.5 * rho * speed**2 * Cd * A
    ax = -g * x / r - (drag / m) * vx / speed
    ay = -g * y / r - (drag / m) * vy / speed
    return [vx, vy, ax, ay]


# ---- 2. NEW: the "event" -- tell solve_ivp when to stop ----
def hit_ground(t, state):
    x, y, vx, vy = state
    return math.sqrt(x**2 + y**2) - RE      # the altitude: above 0 in the air, 0 at the ground

hit_ground.terminal = True     # STOP the simulation when this happens
hit_ground.direction = -1      # only count it when the altitude is going DOWN through 0


# ---- 3. Start: 400 km orbit + 100 m/s deorbit burn (Step 2.5) ----
y0 = RE + 400e3
state0 = [0.0, y0, math.sqrt(MU / y0) - 100.0, 0.0]

t_end = 3 * 3600                         # give up after 3 hours [s]
times = np.arange(0, t_end, 1.0)         # report the state every 1 second

sol = solve_ivp(dynamics, [0, t_end], state0, method="DOP853",
                rtol=1e-10, atol=1e-6, t_eval=times, events=hit_ground)


# ---- 4. Results ----
t_land = sol.t_events[0][0]              # the moment the event happened [s]
x_l, y_l, vx_l, vy_l = sol.y_events[0][0]  # the state at that moment
v_land = math.sqrt(vx_l**2 + vy_l**2)

print("landed after", round(t_land / 60, 1), "minutes")
print("landing speed =", round(v_land, 1), "m/s")

# measure speed and g-force at every reported second (same formulas as dynamics)
alts_km = []
speeds = []
g_forces = []
for k in range(len(sol.t)):
    x, y, vx, vy = sol.y[:, k]           # every row, column k = the state at second k
    r = math.sqrt(x**2 + y**2)
    speed = math.sqrt(vx**2 + vy**2)
    drag = 0.5 * air_density(r - RE) * speed**2 * Cd * A
    alts_km.append((r - RE) / 1000)
    speeds.append(speed)
    g_forces.append(drag / m / G0)

peak = max(g_forces)
i = g_forces.index(peak)
print("peak g-force =", round(peak, 1), "g, at", round(alts_km[i]), "km")
print("dynamics() was called", sol.nfev, "times")


# ---- 5. Plot (same as Step 2.6) ----
plt.subplot(1, 2, 1)
plt.plot(speeds, alts_km)
plt.xlabel("speed [m/s]")
plt.ylabel("altitude [km]")
plt.title("Speed")

plt.subplot(1, 2, 2)
plt.plot(g_forces, alts_km)
plt.xlabel("g-force [g]")
plt.title("Braking")

plt.savefig("step2_7_reentry.png", dpi=120)
plt.show()
