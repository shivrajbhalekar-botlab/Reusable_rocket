# Step 1.7: Draw the orbit

import math
import matplotlib.pyplot as plt

MU = 3.986004418e14   # Earth's gravity strength [m^3/s^2]
RE = 6371e3           # Earth's radius [m]

dt = 0.1              # time step [s]
t_end = 100 * 60      # stop after 100 minutes [s]

x = 0.0               # start 400 km above the top of Earth
y = RE + 400e3
vx = math.sqrt(MU / y)   # orbit speed (about 7673 m/s)
# vx= 1000
vy = 0.0
t = 0.0

xs = [x / 1000]       # list of every x position so far [km]
ys = [y / 1000]       # list of every y position so far [km]

r = math.sqrt(x**2 + y**2)

while r > RE and t < t_end:
    g = MU / r**2
    ax = -g * x / r
    ay = -g * y / r
    vx = vx + ax * dt
    vy = vy + ay * dt
    x = x + vx * dt
    y = y + vy * dt
    t = t + dt
    r = math.sqrt(x**2 + y**2)
    xs.append(x / 1000)   # add the new position to the end of the list
    ys.append(y / 1000)

print("number of points saved =", len(xs))

# ---- drawing ----
plt.figure(figsize=(6, 6))                                          # a square window
plt.gca().add_patch(plt.Circle((0, 0), RE / 1000, color="lightblue"))  # Earth
plt.plot(xs, ys, color="red")                                       # the path
plt.plot(xs[0], ys[0], "ko")                                        # start point (black dot)
plt.axis("equal")                                                   # 1 km looks the same in x and y
plt.title("Ball in orbit, 400 km up")
plt.xlabel("x [km]")
plt.ylabel("y [km]")
plt.savefig("step1_7_orbit.png", dpi=120)                           # save a picture file
plt.show()                                                          # open a window
