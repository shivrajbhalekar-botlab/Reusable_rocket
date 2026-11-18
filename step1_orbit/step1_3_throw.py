# Step 1.3: Throw the ball sideways

g = 9.82      # gravity [m/s^2]
dt = 0.01     # time step [s]

x = 0.0       # sideways position [m]
y = 100.0     # height above the ground [m]
vx = 20.0     # sideways speed [m/s]   (the throw)
vy = 0.0      # up/down speed [m/s]    (up is +, down is -)
t = 0.0       # clock [s]

while y > 0:
    vy = vy - g * dt   # gravity pulls DOWN only, so only vy changes
    x = x + vx * dt    # sideways speed moves the ball sideways
    y = y + vy * dt    # up/down speed moves the ball up/down
    t = t + dt

print("landed after", round(t, 2), "s")
print("landed", round(x, 1), "m away")
