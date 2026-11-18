# Step 2.2c: Watch the speed level off at terminal speed

import math
import matplotlib.pyplot as plt

g = 9.82                   # gravity [m/s^2]
dt = 0.01                  # time step [s]

m = 1.0                    # mass [kg]
radius = 0.1               # [m]
A = math.pi * radius**2    # front area [m^2]
Cd = 0.47                  # sphere
rho = 1.225                # sea-level air [kg/m^3]

h = 1000.0                 # height [m]
v = 0.0                    # speed [m/s]  (up is +, down is -)
t = 0.0

ts = [t]                   # list of times
speeds = [abs(v)]          # list of speeds (size only, no sign)

while h > 0:
    drag = 0.5 * rho * v**2 * Cd * A
    a = -g + drag / m
    v = v + a * dt
    h = h + v * dt
    t = t + dt
    ts.append(t)
    speeds.append(abs(v))

v_term = math.sqrt(2 * m * g / (rho * Cd * A))

plt.plot(ts, speeds, label="ball's speed")
plt.axhline(v_term, color="red", linestyle="--", label="terminal speed")
plt.title("Falling through air: speed levels off")
plt.xlabel("time [s]")
plt.ylabel("speed [m/s]")
plt.legend()
plt.savefig("step2_2c_speed.png", dpi=120)
plt.show()
