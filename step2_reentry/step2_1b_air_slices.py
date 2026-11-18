# Step 2.1b: Build the air-density formula ourselves, one slice at a time

import math

RHO0 = 1.225      # air density at sea level [kg/m^3]
H = 8500.0        # scale height [m]

dh = 1.0          # climb 1 meter per slice [m]
rho = RHO0        # start at sea level

for i in range(10000):           # 10,000 slices of 1 m = 10 km
    rho = rho - rho * dh / H     # each slice loses the fraction dh/H

print(f"climbing slice by slice: {rho:.4f} kg/m^3")
print(f"formula RHO0*exp(-h/H):  {RHO0 * math.exp(-10000 / H):.4f} kg/m^3")
