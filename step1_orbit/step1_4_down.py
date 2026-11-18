# Step 1.4: On a round Earth, "down" means "toward the center"

import math

MU = 3.986004418e14   # Earth's gravity strength [m^3/s^2]
RE = 6371e3           # Earth's radius [m]

# Earth's center is at (0, 0). The ball's position is measured from there.
x = 0.0               # [m]
y = RE + 400e3        # [m]  straight above the center, 400 km up

r = math.sqrt(x**2 + y**2)   # distance from Earth's center (Pythagoras)
g = MU / r**2                # how strong the pull is (Step 1.1)

ax = -g * x / r       # the part of the pull in the x direction [m/s^2]
ay = -g * y / r       # the part of the pull in the y direction [m/s^2]

print("distance from center =", round(r / 1000), "km")
print("pull strength g =", round(g, 2), "m/s^2")
print("ax =", round(ax, 2), "   ay =", round(ay, 2))
