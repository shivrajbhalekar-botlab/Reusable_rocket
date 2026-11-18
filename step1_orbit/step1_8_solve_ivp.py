# Step 1.8: Let scipy run the loop for us (solve_ivp)

import math
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

MU = 3.986004418e14   # Earth's gravity strength [m^3/s^2]
RE = 6371e3           # Earth's radius [m]


# ---- 1. The physics: how fast is each number changing RIGHT NOW? ----
def dynamics(t, state):
    x, y, vx, vy = state            # unpack the 4 numbers
    r = math.sqrt(x**2 + y**2)
    g = MU / r**2
    ax = -g * x / r
    ay = -g * y / r
    return [vx, vy, ax, ay]         # x changes at rate vx, y at vy, vx at ax, vy at ay


# ---- 2. The starting state ----
x0 = 0.0
y0 = RE + 400e3
vx0 = math.sqrt(MU / y0)            # orbit speed
vy0 = 0.0
state0 = [x0, y0, vx0, vy0]

period = 2 * math.pi * y0 / vx0     # one lap = length of the circle / speed
print("period =", round(period / 60, 2), "min")


# ---- 3. Let solve_ivp do the loop ----
times = np.linspace(0, period, 1000)    # 1000 evenly spaced moments we want reported
sol = solve_ivp(dynamics, [0, period], state0,
                method="DOP853", rtol=1e-10, atol=1e-6, t_eval=times)

print("dynamics() was called", sol.nfev, "times   (our own loop: about 55,000)")


# ---- 4. Check the answer ----
def energy(state):
    x, y, vx, vy = state
    return 0.5 * (vx**2 + vy**2) - MU / math.sqrt(x**2 + y**2)

state_end = sol.y[:, -1]            # every row, last column = the final state
x_end, y_end, vx_end, vy_end = state_end

gap = math.sqrt((x_end - x0)**2 + (y_end - y0)**2)
print("distance from start after one lap =", round(gap, 3), "m")

E0 = energy(state0)
E1 = energy(state_end)
print("energy change =", abs(E1 - E0) / abs(E0), "(relative)")


# ---- 5. Draw it (same as Step 1.7) ----
plt.figure(figsize=(6, 6))
plt.gca().add_patch(plt.Circle((0, 0), RE / 1000, color="lightblue"))
plt.plot(sol.y[0] / 1000, sol.y[1] / 1000, color="red")    # row 0 = all x, row 1 = all y
plt.plot(x0 / 1000, y0 / 1000, "ko")
plt.axis("equal")
plt.title("Orbit with solve_ivp")
plt.xlabel("x [km]")
plt.ylabel("y [km]")
plt.savefig("step1_8_orbit.png", dpi=120)
plt.show()
