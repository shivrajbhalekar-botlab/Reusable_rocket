# Step 3.4: The rocket equation -- predict the final speed with ONE formula

import math

g = 0.0               # NO gravity for now: the rocket is floating in deep space
dt = 0.01             # time step [s]

# ---- the rocket (same as Step 3.3) ----
dry_mass = 200.0      # empty rocket [kg]
fuel = 800.0          # fuel [kg]
mdot = 10.0           # burn rate [kg/s]
ve = 1500.0           # exhaust speed [m/s]
thrust = mdot * ve

# ---- 1. The rocket equation ----
m0 = dry_mass + fuel                  # mass when FULL  [kg]
mf = dry_mass                         # mass when EMPTY [kg]
dv_formula = ve * math.log(m0 / mf)   # NEW: math.log is "ln", the natural logarithm

# ---- 2. The simulation (Step 3.3 loop) ----
v = 0.0
m = m0
burn_time = fuel / mdot
for i in range(round(burn_time / dt)):
    a = (thrust - m * g) / m
    v = v + a * dt
    m = m - mdot * dt

print("mass ratio m0/mf =", m0 / mf)
print("simulation:      speed gained =", round(v), "m/s")
print("rocket equation: speed gained =", round(dv_formula), "m/s")
