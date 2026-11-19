# Step 3.3: Where does thrust come from? Throwing exhaust out the back.

g = 9.82              # gravity [m/s^2]
dt = 0.01             # time step [s]

# ---- the rocket ----
dry_mass = 200.0      # the empty rocket [kg]
fuel = 800.0          # fuel at liftoff [kg]
mdot = 10.0           # fuel burned (and thrown out the back) every second [kg/s]
ve = 1500.0           # NEW: exhaust speed -- how fast the gas shoots out the nozzle [m/s]

thrust = mdot * ve    # NEW: thrust = (mass thrown per second) x (speed it's thrown at)

print("thrust =", round(thrust), "N")

# ---- the rest is exactly Step 3.2 ----
h = 0.0
v = 0.0
t = 0.0
m = dry_mass + fuel

burn_time = fuel / mdot
for i in range(round(burn_time / dt)):
    a = (thrust - m * g) / m
    v = v + a * dt
    h = h + v * dt
    m = m - mdot * dt
    t = t + dt

print("engine off after", round(t), "s")
print("speed =", round(v), "m/s")
print("height =", round(h / 1000, 1), "km")
