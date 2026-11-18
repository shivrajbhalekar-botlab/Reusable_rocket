# Step 1.6: Throw the ball so fast it never lands (an orbit!)

import math

MU = 3.986004418e14   # Earth's gravity strength [m^3/s^2]
RE = 6371e3           # Earth's radius [m]

dt = 0.1              # time step [s]
t_end = 1000 * 60      # stop after 100 minutes [s]

x = 0.0               # start 400 km above the top of Earth
y = RE + 400e3
vx = math.sqrt(MU / y)   # sideways throw: the "orbit speed" (about 7673 m/s)
vy = 0.0
t = 0.0

print("throw speed =", round(vx), "m/s")

r = math.sqrt(x**2 + y**2)
lowest = r - RE                   # lowest altitude seen so far [m]

while r > RE and t < t_end:       # stop if it hits the ground OR time is up
    g = MU / r**2
    ax = -g * x / r
    ay = -g * y / r
    vx = vx + ax * dt
    vy = vy + ay * dt
    x = x + vx * dt
    y = y + vy * dt
    t = t + dt
    r = math.sqrt(x**2 + y**2)
    lowest = min(lowest, r - RE)  # remember the lowest point

if r <= RE:
    print("CRASHED after", round(t / 60, 1), "min")
else:
    print("still flying after", round(t / 60, 1), "min")
print("lowest altitude =", round(lowest / 1000), "km")
