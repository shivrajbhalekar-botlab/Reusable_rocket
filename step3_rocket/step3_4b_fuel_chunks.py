# Step 3.4b: WHERE does the rocket equation come from?
# Burn the fuel in small chunks. Each chunk thrown backward gives the rocket a small kick forward.
# Add up all the kicks -> you get the rocket equation.

import math

dry_mass = 200.0      # empty rocket [kg]
fuel = 800.0          # fuel [kg]
ve = 1500.0           # exhaust speed [m/s]
chunk = 1.0           # burn the fuel 1 kg at a time [kg]

m = dry_mass + fuel   # full rocket: 1000 kg
v = 0.0               # rocket speed [m/s]

print("first kick:", round(ve * chunk / m, 2), "m/s   (rocket weighs", m, "kg)")

for i in range(round(fuel / chunk)):
    kick = ve * chunk / m     # throw 'chunk' kg backward at ve  ->  rocket (m kg) gains ve * chunk / m
    v = v + kick              # add this kick to the speed
    m = m - chunk             # that chunk of fuel is gone

print("last kick: ", round(kick, 2), "m/s   (rocket weighed", round(m + chunk, 2), "kg)")
print("adding all the kicks:", round(v, 1), "m/s")
print("rocket equation:     ", round(ve * math.log((dry_mass + fuel) / dry_mass), 1), "m/s")
