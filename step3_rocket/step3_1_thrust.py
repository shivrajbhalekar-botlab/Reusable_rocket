# Step 3.1: Thrust -- an engine pushes the rocket UP

g = 9.82              # gravity [m/s^2]
dt = 0.01             # time step [s]

# ---- the rocket ----
m = 1000.0            # mass [kg]  (stays the same for now)
thrust = 15000.0      # engine push, pointing UP [N]

# ---- start on the launch pad ----
h = 0.0               # height [m]
v = 0.0               # speed [m/s]  (up is +)
t = 0.0

weight = m * g
print("weight =", round(weight), "N,   thrust =", round(thrust), "N")

burn_time = 10.0                       # run the engine for 10 seconds
for i in range(round(burn_time / dt)): # 10 s / 0.01 s = 1000 slices
    a = (thrust - weight) / m          # NEW: engine up, gravity down
    v = v + a * dt                     # same loop as Step 1.2
    h = h + v * dt
    t = t + dt

print("acceleration =", round(a, 2), "m/s^2")
print("after", round(t), "s:  height =", round(h, 1), "m,  speed =", round(v, 1), "m/s")
