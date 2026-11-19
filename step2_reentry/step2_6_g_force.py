# Step 2.6: How hard does the air brake? (g-force during reentry)

import math
import matplotlib.pyplot as plt

MU = 3.986004418e14   # Earth's gravity strength [m^3/s^2]
RE = 6371e3           # Earth's radius [m]
G0 = 9.81             # "1 g" -- the pull you feel standing on Earth [m/s^2]

RHO0 = 1.225          # air density at sea level [kg/m^3]
H = 8500.0            # scale height [m]


def air_density(h):
    """Air density [kg/m^3] at height h [m] above the ground.  (Step 2.1)"""
    return RHO0 * math.exp(-h / H)


# ---- the ball (same as Step 2.2) ----
m = 4.0                    # mass [kg]
radius = 0.1               # [m]
A = math.pi * radius**2    # front area [m^2]
Cd = 0.47                  # sphere

# ---- start: 400 km orbit + 100 m/s deorbit burn (Step 2.5, Run B) ----
dt = 0.1
t_end = 3 * 3600

x = 0.0
y = RE + 400e3
vx = math.sqrt(MU / y) - 100.0
vy = 0.0
t = 0.0

alts_km = []          # altitude [km]
speeds = []           # speed [m/s]
g_forces = []         # how hard the air brakes, in g's

r = math.sqrt(x**2 + y**2)

while r > RE and t < t_end:
    g = MU / r**2
    rho = air_density(r - RE)
    speed = math.sqrt(vx**2 + vy**2)
    drag = 0.5 * rho * speed**2 * Cd * A

    # NEW: the braking, measured in g's
    braking = drag / m                 # deceleration from the air [m/s^2]
    alts_km.append((r - RE) / 1000)
    speeds.append(speed)
    g_forces.append(braking / G0)      # e.g. 19.6 m/s^2 -> 2 g

    ax = -g * x / r - (drag / m) * vx / speed
    ay = -g * y / r - (drag / m) * vy / speed
    vx = vx + ax * dt
    vy = vy + ay * dt
    x = x + vx * dt
    y = y + vy * dt
    t = t + dt
    r = math.sqrt(x**2 + y**2)

peak = max(g_forces)                   # the biggest g-force of the whole flight
i = g_forces.index(peak)               # WHERE in the list it happened
print("peak g-force =", round(peak, 1), "g")
print("it happened at", round(alts_km[i]), "km, moving at", round(speeds[i]), "m/s")
print("landed after", round(t / 60, 1), "minutes")

plt.subplot(1, 2, 1)                   # left picture
plt.plot(speeds, alts_km)
plt.xlabel("speed [m/s]")
plt.ylabel("altitude [km]")
plt.title("Speed")

plt.subplot(1, 2, 2)                   # right picture
plt.plot(g_forces, alts_km)
plt.xlabel("g-force [g]")
plt.title("Braking")

plt.savefig("step2_6_g_force.png", dpi=120)
plt.show()
