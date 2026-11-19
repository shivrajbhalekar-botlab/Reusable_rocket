# atmosphere.py -- the REAL air: US Standard Atmosphere 1976 (built in Step 3.5b)
# This file has NO prints. It only holds the function, so other steps can use it with:
#     from atmosphere import us_standard_atmosphere

import math

# ---- constants of the standard ----
G0 = 9.80665        # standard gravity [m/s^2]
M = 0.0289644       # mass of 1 mole of air [kg/mol]
R = 8.31446         # gas constant [J/(mol K)]
R0 = 6356766.0      # Earth radius used by the standard [m]

# ---- the layers of the air (from the official table) ----
# (bottom height [m], temperature at bottom [K], temperature change per metre [K/m], pressure at bottom [Pa])
LAYERS = [
    (0,     288.15,  -0.0065, 101325.0),   # troposphere: colder as you go up
    (11000, 216.65,   0.0,    22632.06),   # temperature stays the same
    (20000, 216.65,   0.001,  5474.889),   # stratosphere: WARMER as you go up (ozone)
    (32000, 228.65,   0.0028, 868.0187),
    (47000, 270.65,   0.0,    110.9063),   # temperature stays the same
    (51000, 270.65,  -0.0028, 66.93887),   # mesosphere: colder again
    (71000, 214.65,  -0.002,  3.956420),
    (84852, 186.946,  0.0,    0.3734),     # top of the standard (~86 km); above it we just keep T constant
]


def us_standard_atmosphere(h):
    """Temperature [K], pressure [Pa] and density [kg/m^3] at height h [m] above sea level."""
    hp = R0 * h / (R0 + h)          # "geopotential height" correction

    for layer in LAYERS:            # find our layer: the LAST one whose bottom is below us
        if hp >= layer[0]:
            hb, Tb, L, Pb = layer

    dh = hp - hb
    if L == 0:
        T = Tb
        P = Pb * math.exp(-G0 * M * dh / (R * Tb))
    else:
        T = Tb + L * dh
        P = Pb * (Tb / T) ** (G0 * M / (R * L))

    rho = P * M / (R * T)
    return T, P, rho


GAMMA = 1.4         # "ratio of specific heats" of air (how springy air is when squeezed)


def speed_of_sound(T):
    """Speed of sound [m/s] in air at temperature T [K].  (Step 3.5e)"""
    return math.sqrt(GAMMA * R * T / M)
