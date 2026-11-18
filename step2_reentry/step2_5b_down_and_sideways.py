# Step 2.5b: After the burn (no air), split the speed into DOWN and SIDEWAYS

import math
import matplotlib.pyplot as plt

MU = 3.986004418e14   # Earth's gravity strength [m^3/s^2]
RE = 6371e3           # Earth's radius [m]

dt = 0.1              # time step [s]
t_end = 100 * 60      # a bit more than one lap [s]

x = 0.0
y = RE + 400e3
vx = math.sqrt(MU / y) - 100.0    # orbit speed minus a 100 m/s burn
vy = 0.0
t = 0.0

ts_min = []
down_speeds = []        # speed toward Earth's center [m/s]
side_speeds = []        # speed along the ground [m/s]
orbit_speeds = []       # orbit speed needed at the current height [m/s]

r = math.sqrt(x**2 + y**2)

while t < t_end:
    # ---- split the velocity into down + sideways ----
    speed = math.sqrt(vx**2 + vy**2)
    away = vx * (x / r) + vy * (y / r)          # part of the velocity pointing AWAY from the center
    down = -away                                # so "down" is the opposite
    side = math.sqrt(speed**2 - away**2)        # the rest is sideways (Pythagoras)

    ts_min.append(t / 60)
    down_speeds.append(down)
    side_speeds.append(side)
    orbit_speeds.append(math.sqrt(MU / r))

    # ---- the usual orbit loop (no air) ----
    g = MU / r**2
    ax = -g * x / r
    ay = -g * y / r
    vx = vx + ax * dt
    vy = vy + ay * dt
    x = x + vx * dt
    y = y + vy * dt
    t = t + dt
    r = math.sqrt(x**2 + y**2)

plt.subplot(2, 1, 1)                              # top picture
plt.plot(ts_min, down_speeds)
plt.axhline(0, color="gray")
plt.ylabel("down speed [m/s]")
plt.title("After a 100 m/s burn (no air)")

plt.subplot(2, 1, 2)                              # bottom picture
plt.plot(ts_min, side_speeds, label="sideways speed")
plt.plot(ts_min, orbit_speeds, "--", label="orbit speed needed here")
plt.ylabel("speed [m/s]")
plt.xlabel("time after burn [minutes]")
plt.legend()

plt.savefig("step2_5b_speeds.png", dpi=120)
plt.show()
