# Step 3.5b: The REAL atmosphere -- "US Standard Atmosphere 1976"
# The table engineers, aircraft and drone barometers use.  Compare it with our old one-line formula (Step 2.1).

import math

# ---- constants of the standard ----
G0 = 9.80665        # standard gravity [m/s^2]
M = 0.0289644       # mass of 1 mole of air [kg/mol]
R = 8.31446         # gas constant [J/(mol K)]
R0 = 6356766.0      # Earth radius used by the standard [m]

# ---- the layers of the air (from the official table) ----
# (bottom height [m], temperature at bottom [K], temperature change per metre [K/m], pressure at bottom [Pa])
LAYERS = [
    (0,     288.15,  -0.0065, 101325.0),   # troposphere: colder as you go up (weather, planes, drones)
    (11000, 216.65,   0.0,    22632.06),   # temperature stays the same
    (20000, 216.65,   0.001,  5474.889),   # stratosphere: WARMER as you go up (ozone absorbs sunlight)
    (32000, 228.65,   0.0028, 868.0187),
    (47000, 270.65,   0.0,    110.9063),   # temperature stays the same
    (51000, 270.65,  -0.0028, 66.93887),   # mesosphere: colder again
    (71000, 214.65,  -0.002,  3.956420),
    (84852, 186.946,  0.0,    0.3734),     # top of the standard (~86 km); above it we just keep T constant
]


def us_standard_atmosphere(h):
    """Temperature [K], pressure [Pa] and density [kg/m^3] at height h [m] above sea level."""
    hp = R0 * h / (R0 + h)          # small correction the standard uses ("geopotential height")

    # 1. find which layer we are in: the LAST layer whose bottom is below us
    for layer in LAYERS:
        if hp >= layer[0]:
            hb, Tb, L, Pb = layer

    # 2. temperature and pressure inside that layer
    dh = hp - hb                    # how far above the bottom of the layer
    if L == 0:
        T = Tb                                          # same temperature all through the layer
        P = Pb * math.exp(-G0 * M * dh / (R * Tb))      # = Step 2.1's e^(-h/H), with H = R*T/(M*g)
    else:
        T = Tb + L * dh                                 # temperature changes in a straight line
        P = Pb * (Tb / T) ** (G0 * M / (R * L))         # pressure formula when T changes (accept it for now)

    # 3. density from pressure and temperature (gas law, Step 2.1)
    rho = P * M / (R * T)
    return T, P, rho


# ---- compare with our old one-line air (Step 2.1) ----
print("height  |  temp    | REAL air   | our old air")
for km in [0, 10, 20, 30, 50, 80]:
    h = km * 1000.0
    T, P, rho = us_standard_atmosphere(h)
    old = 1.225 * math.exp(-h / 8500.0)
    print(f"{km:4} km | {T - 273.15:6.1f} C | {rho:<10.3g} | {old:.3g}")
