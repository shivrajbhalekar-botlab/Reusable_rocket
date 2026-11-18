# Step 2.4: Put air drag into the orbit

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

# ---- start: circular orbit at 180 km (Step 1.6) ----
dt = 0.1                   # time step [s]
t_end = 10 * 3600          # give up after 10 hours [s]

x = 0.0
y = RE + 180e3
vx = math.sqrt(MU / y)     # orbit speed
vy = 0.0
t = 0.0

ts_hours = [0.0]                 # time, in hours, for the plot
alts_km = [(y - RE) / 1000]      # altitude, in km, for the plot

r = math.sqrt(x**2 + y**2)

while r > RE and t < t_end:
    # gravity: points to Earth's center                          (Step 1.5)
    g = MU / r**2

    # drag: points opposite to the motion                        (Step 2.3)
    # ...using the air density at the CURRENT height             (Step 2.1)
    rho = air_density(r - RE)
    speed = math.sqrt(vx**2 + vy**2)
    drag = 0.5 * rho * speed**2 * Cd * A

    # add both pulls together
    ax = -g * x / r - (drag / m) * vx / speed
    ay = -g * y / r - (drag / m) * vy / speed

    vx = vx + ax * dt
    vy = vy + ay * dt
    x = x + vx * dt
    y = y + vy * dt
    t = t + dt
    r = math.sqrt(x**2 + y**2)

    ts_hours.append(t / 3600)
    alts_km.append((r - RE) / 1000)

speed = math.sqrt(vx**2 + vy**2)
if r <= RE:
    print("landed after", round(t / 3600, 2), "hours")
    print("landing speed =", round(speed, 1), "m/s")
else:
    print("still flying after", round(t / 3600, 2), "hours, at", round((r - RE) / 1000), "km")

plt.plot(ts_hours, alts_km)
plt.title("Orbit slowly losing height to air drag")
plt.xlabel("time [hours]")
plt.ylabel("altitude [km]")
plt.savefig("step2_4_altitude.png", dpi=120)
plt.show()
