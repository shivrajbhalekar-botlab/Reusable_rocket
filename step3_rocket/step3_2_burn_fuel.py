# Step 3.2: Burning fuel -- the rocket gets LIGHTER as it flies

g = 9.82              # gravity [m/s^2]
dt = 0.01             # time step [s]

# ---- the rocket ----
dry_mass = 200.0      # the empty rocket: engine, tank, structure [kg]
fuel = 800.0          # fuel in the tank at liftoff [kg]
mdot = 10.0           # fuel burned every second [kg/s]   (say "m-dot")
thrust = 15000.0      # engine push, pointing UP [N]  (same as Step 3.1)

# ---- start on the launch pad ----
h = 0.0
v = 0.0
t = 0.0
m = dry_mass + fuel   # total mass at liftoff: 1000 kg (same as Step 3.1)

print("liftoff mass =", round(m), "kg,  acceleration =", round((thrust - m * g) / m, 2), "m/s^2")

burn_time = fuel / mdot                  # 800 kg / 10 kg/s = 80 s until the tank is empty
for i in range(round(burn_time / dt)):
    a = (thrust - m * g) / m             # same as Step 3.1, but m changes every slice
    v = v + a * dt
    h = h + v * dt
    m = m - mdot * dt                    # NEW: burn a little fuel -> lighter
    t = t + dt

print("engine off after", round(t), "s  (tank empty)")
print("mass left =", round(m), "kg,  acceleration just before cutoff =", round(a, 1), "m/s^2")
print("speed =", round(v), "m/s")
print("height =", round(h / 1000, 1), "km")
