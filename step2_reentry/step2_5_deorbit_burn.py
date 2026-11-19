# Step 2.5: The deorbit burn -- slow down a little, and the air does the rest

import math
import matplotlib.pyplot as plt

MU = 3.986004418e14   # Earth's gravity strength [m^3/s^2]
RE = 6371e3           # Earth's radius [m]

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

# ---- start: circular orbit at 400 km, then the burn ----
dt = 0.1                   # time step [s]
t_end = 3 * 3600           # give up after 3 hours [s]

x = 0.0
y = RE + 400e3
v_orbit = math.sqrt(MU / y)    # orbit speed at 400 km (Step 1.6)
dv = 100.0                     # DEORBIT BURN: how much we slow down [m/s]
vx = v_orbit - dv              # speed right after the burn
vy = 0.0
t = 0.0

print("orbit speed =", round(v_orbit, 1), "m/s,  after burn =", round(vx, 1), "m/s")

ts_min = [0.0]                   # time, in minutes, for the plot
alts_km = [(y - RE) / 1000]      # altitude, in km, for the plot

r = math.sqrt(x**2 + y**2)

while r > RE and t < t_end:      # the same loop as Step 2.4
    g = MU / r**2
    rho = air_density(r - RE)
    speed = math.sqrt(vx**2 + vy**2)
    drag = 0.5 * rho * speed**2 * Cd * A

    ax = -g * x / r - (drag / m) * vx / speed
    ay = -g * y / r - (drag / m) * vy / speed

    vx = vx + ax * dt
    vy = vy + ay * dt
    x = x + vx * dt
    y = y + vy * dt
    t = t + dt
    r = math.sqrt(x**2 + y**2)

    ts_min.append(t / 60)
    alts_km.append((r - RE) / 1000)

speed = math.sqrt(vx**2 + vy**2)
if r <= RE:
    print("landed after", round(t / 60, 1), "minutes")
    print("landing speed =", round(speed, 1), "m/s")
else:
    print("still flying after", round(t / 60, 1), "minutes, at", round((r - RE) / 1000), "km")
print("lowest altitude reached =", round(min(alts_km)), "km")

plt.plot(ts_min, alts_km)
plt.title(f"Deorbit burn of {dv} m/s")
plt.xlabel("time after burn [minutes]")
plt.ylabel("altitude [km]")
plt.savefig("step2_5_deorbit.png", dpi=120)
plt.show()
