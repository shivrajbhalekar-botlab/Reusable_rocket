import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

MU = 3.986004418e14          # Earth gravity [m^3/s^2]
RE = 6371e3                  # Earth radius [m]

def dynamics(t, s):
    r, v = s[:3], s[3:]
    a = -MU * r / np.linalg.norm(r)**3
    return np.hstack([v, a])

# sample object: circular orbit at 400 km altitude
r0 = RE + 400e3
v0 = np.sqrt(MU / r0)
s0 = [r0, 0, 0, 0, v0, 0]
period = 2*np.pi*np.sqrt(r0**3 / MU)

sol = solve_ivp(dynamics, [0, period], s0, method="DOP853",
                rtol=1e-10, atol=1e-6, dense_output=True)
r, v = sol.y[:3], sol.y[3:]
energy = 0.5*np.sum(v**2, axis=0) - MU/np.linalg.norm(r, axis=0)

print(f"period = {period/60:.2f} min")
print(f"end position error = {np.linalg.norm(r[:, -1]-r[:, 0]):.3f} m")
print(f"energy drift = {abs(energy[-1]-energy[0])/abs(energy[0]):.2e} (relative)")

fig = plt.figure(); ax = fig.add_subplot(projection="3d")
ax.plot(*r/1e3); ax.set_title("Sample object, 400 km circular orbit [km]")
plt.savefig("orbit.png", dpi=120)