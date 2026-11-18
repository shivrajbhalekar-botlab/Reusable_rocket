# Step 2.1: How thick is the air at each height?

import math

RHO0 = 1.225      # air density at sea level [kg/m^3]
H = 8500.0        # "scale height": every 8.5 km up, air gets ~2.7x thinner [m]


def air_density(h):
    """Air density [kg/m^3] at height h [m] above the ground."""
    return RHO0 * math.exp(-h / H)


for h_km in [0, 10, 50, 100, 400]:
    rho = air_density(h_km * 1000)
    print(f"height = {h_km} km    air density = {rho:.3g} kg/m^3")
