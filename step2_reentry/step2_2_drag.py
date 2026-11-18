# Step 2.2: Drop a ball WITH air (drag)

import math

g = 9.82                   # gravity [m/s^2]
dt = 0.01                  # time step [s]

# ---- the ball ----
m = 1.0                    # mass [kg]
radius = 0.1               # [m]
A = math.pi * radius**2    # front area that hits the air [m^2]
Cd = 0.47                  # drag coefficient: how "un-slippery" the shape is (sphere = 0.47)

rho = 1.225                # air density [kg/m^3]  (sea level; kept constant for now)

# ---- start ----
h = 1000.0                 # height [m]
v = 0.0 # speed [m/s]  (up is +, down is -)
v = -60
t = 0.0                    # clock [s]

while h > 0:
    drag = 0.5 * rho * v**2 * Cd * A    # 1. how hard the air pushes back [N]
    a = -g + drag / m                   # 2. gravity pulls DOWN, drag pushes UP
    v = v + a * dt                      # 3. same as Step 1.2
    h = h + v * dt
    t = t + dt

v_term = math.sqrt(2 * m * g / (rho * Cd * A))   # terminal speed (explained below)

print("landed after", round(t, 1), "s")
print("landing speed =", round(abs(v), 1), "m/s")
print("terminal speed formula =", round(v_term, 1), "m/s")
