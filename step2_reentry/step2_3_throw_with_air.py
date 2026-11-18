# Step 2.3: Throw the ball sideways WITH air (drag in 2D)

import math

g = 9.82                   # gravity [m/s^2]
dt = 0.01                  # time step [s]

# ---- the ball (same as Step 2.2) ----
m = 1.0                    # mass [kg]
radius = 0.1               # [m]
A = math.pi * radius**2    # front area [m^2]
Cd = 0.47                  # sphere
rho = 1.225                # sea-level air [kg/m^3]
# rho = 0

# ---- start (same as Step 1.3) ----
x = 0.0                    # sideways position [m]
y = 100.0                  # height [m]
vx = 20.0                  # sideways speed [m/s]
vy = 0.0                   # up/down speed [m/s]
t = 0.0

while y > 0:
    speed = math.sqrt(vx**2 + vy**2)          # 1. total speed (Pythagoras)
    drag = 0.5 * rho * speed**2 * Cd * A      # 2. drag strength [N]   (Step 2.2)
    ax = -(drag / m) * vx / speed             # 3. drag points OPPOSITE to the motion
    ay = -g - (drag / m) * vy / speed         #    ...plus gravity pulling down
    vx = vx + ax * dt                         # 4. same loop as Step 1.3
    vy = vy + ay * dt
    x = x + vx * dt
    y = y + vy * dt
    t = t + dt

print("landed after", round(t, 2), "s")
print("landed", round(x, 1), "m away")
