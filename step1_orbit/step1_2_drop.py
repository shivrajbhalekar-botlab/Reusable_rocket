# Step 1.2: Drop a ball and watch it fall

g = 9.82      # gravity at the ground [m/s^2]  (from Step 1.1)
dt = 0.01     # time step: how much time passes in each loop [s]

h = 100.0     # height above the ground [m]
v = 0.0       # speed [m/s]  (up is +, down is -)
t = 0.0       # clock [s]

while h > 0:
    v = v - g * dt    # 1. gravity changes the speed
    h = h + v * dt    # 2. the speed changes the height
    t = t + dt        # 3. the clock moves forward
    print("t =", round(t, 2), "s   height =", round(h, 1), "m   speed =", round(v, 1), "m/s")
