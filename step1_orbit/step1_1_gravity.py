# Step 1.1: How strong is Earth's gravity?

MU = 3.986004418e14   # Earth's gravity strength [m^3/s^2]
RE = 6371e3           # Earth's radius [m]

r = RE                # distance from Earth's center: standing on the ground
g = MU / r**2         # how hard gravity pulls at that distance [m/s^2]

print("gravity =", round(g, 2), "m/s^2")
