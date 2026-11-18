# Step 1.5: Drop a ball from space (400 km up)

import math

MU = 3.986004418e14   # Earth's gravity strength [m^3/s^2]
RE = 6371e3           # Earth's radius [m]

dt = 0.001             # time step [s]

x = 0.0               # position, measured from Earth's center [m]
y = RE + 400e3
vx = 0.0              # speed [m/s]  (just let go, no throw)
vy = 0.0
t = 0.0               # clock [s]

r = math.sqrt(x**2 + y**2)        # distance from Earth's center

while r > RE:                     # keep going while above the ground
    g = MU / r**2                 # 1. how strong is the pull here?   (Step 1.1)
    ax = -g * x / r               # 2. which way does it point?        (Step 1.4)
    ay = -g * y / r
    vx = vx + ax * dt             # 3. the pull changes the speed      (Step 1.2)
    vy = vy + ay * dt
    x = x + vx * dt               # 4. the speed changes the position  (Step 1.2)
    y = y + vy * dt
    t = t + dt                    # 5. the clock moves forward
    r = math.sqrt(x**2 + y**2)    # 6. new distance, for the next check

speed = math.sqrt(vx**2 + vy**2)
print("hit the ground after", round(t, 1), "s  =", round(t / 60, 1), "min")
print("impact speed =", round(speed), "m/s")
print("landed at x =", round(x / 1000), "km")
