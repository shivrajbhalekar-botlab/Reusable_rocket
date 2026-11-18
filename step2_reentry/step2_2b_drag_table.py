# Step 2.2b: How big is the drag force at different speeds?

import math

m = 1.0                    # mass [kg]
radius = 0.1               # [m]
A = math.pi * radius**2    # front area [m^2]
Cd = 0.47                  # sphere
rho = 1.225                # sea-level air [kg/m^3]
g = 9.82

weight = m * g
print(f"weight = {weight:.2f} N")

for v in [0, 10, 20, 30, 33, 40]:
    drag = 0.5 * rho * v**2 * Cd * A
    print(f"speed = {v} m/s    drag = {drag:.2f} N")
