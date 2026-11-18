# Step 1 — Make an object orbit Earth

**Goal:** put a ball 400 km above Earth, throw it sideways fast enough, and watch it go around forever.
We built it from nothing, one idea per file.

## How to run

```bash
conda activate rocket
cd /hdd/projects/Rocket/step1_orbit
python step1_1_gravity.py        # or any other file
```

Run from inside this folder so the saved pictures (`.png`) land here.

---

## The files, in order

| File | New idea | What you see |
|---|---|---|
| `step1_1_gravity.py` | Gravity strength: `g = MU / r²` | `gravity = 9.82 m/s^2` (8.69 at 400 km) |
| `step1_2_drop.py` | **The time loop**: chop time into slices `dt` | Ball falls 100 m in ~4.51 s |
| `step1_3_throw.py` | **Two directions**: `x, y, vx, vy` | Sideways throw lands at the *same time* on flat ground |
| `step1_4_down.py` | **Round Earth**: "down" = toward the center | Pull splits into `ax`, `ay` |
| `step1_5_fall_from_space.py` | Round-Earth gravity **inside** the loop | Dropped from 400 km: hits ground after ~5 min at ~2719 m/s |
| `step1_6_orbit.py` | **Orbit speed** `√(MU/r)` ≈ 7673 m/s | Never lands. 7000 m/s → crashes |
| `step1_7_draw.py` | **Lists + plotting** (matplotlib) | Picture of the orbit (circle). 8000 m/s → ellipse |
| `step1_8_solve_ivp.py` | **`solve_ivp`** does the loop for us | 1 lap = 92.41 min, back to start within ~1 mm |
| `step1_orbit.py` | The original compact version (3D, numpy) | Same physics as 1.8 |

---

## Key formulas

| What | Formula | Code |
|---|---|---|
| Earth constants | `MU = 3.986e14 m³/s²`, `RE = 6371 km` | `MU`, `RE` |
| Distance from center | `r = √(x² + y²)` | `math.sqrt(x**2 + y**2)` |
| Gravity strength | `g = MU / r²` | `MU / r**2` |
| Gravity components (point to center) | `ax = -g·x/r`, `ay = -g·y/r` | `-g * x / r` |
| One time slice | speed += accel·dt, then position += speed·dt | `vx = vx + ax*dt`, `x = x + vx*dt` |
| Circular orbit speed | `v = √(MU / r)` | `math.sqrt(MU / r)` |
| Escape speed | `v = √(2·MU / r)` = 1.414 × orbit speed | |
| Time for one lap | `T = 2πr / v` | `2 * math.pi * r / v` |
| Energy (per kg) | `E = ½v² − MU/r` | must stay constant with no air/engine |

---

## The ideas to remember

**1. Simulation = slices of time.**
Each slice does two things: the force changes the *speed*, the speed changes the *position*.
Smaller `dt` → more accurate, but more work. (1.2: `dt=1` put the ball 47 m underground; `dt=0.1` fixed it.)

**2. Components.**
A force or velocity is one arrow. We store it as its x-part and y-part.
`x/r` and `y/r` give the direction; multiply by `g` for size; the minus sign flips it toward the center.
Example: ball at (3, 4), r = 5, g = 10 → `ax = -6`, `ay = -8`, and √(6² + 8²) = 10.

**3. Why an orbit works — fall = drop.**
In time `t` the ball **falls** `½·g·t²`.
Moving sideways `v·t`, the round Earth **curves away** by `(v·t)² / (2r)` (Pythagoras).
Set them equal → `g = v²/r` → `v = √(MU/r)`.
Check at 400 km, 1 second: falls 4.35 m, ground curves away 4.35 m. Height never changes.
Flat ground never curves away — that's why no throw orbits in 1.3.

**4. Circle, ellipse, crash, escape.**

| Throw speed at 400 km | Result |
|---|---|
| < ~7600 m/s | crashes on the far side |
| 7673 m/s | circle |
| between 7673 and 10851 m/s | ellipse (8000 m/s reaches ~1700 km) |
| ≥ 10851 m/s | escapes forever (energy `E` ≥ 0) |

**5. `solve_ivp` = same physics, smarter loop.**
You write only `dynamics(t, state)` — *how fast each number is changing right now*:
`[x, y, vx, vy]` changes at `[vx, vy, ax, ay]`.
`solve_ivp` chooses `dt` itself and checks its own error.
`sol.y` is a table: 4 rows (x, y, vx, vy) × one column per reported time. `sol.y[:, -1]` = final state.

**6. How to know a simulation is right.**
- After one lap the ball should be back where it started (gap ≈ 0.001 m).
- Energy `E` should not change (relative change ≈ 1e-12).

---

## How 1.8 maps to the original `step1_orbit.py`

| Original | Meaning |
|---|---|
| `s0 = [r0, 0, 0, 0, v0, 0]` | Same state in 3D: `[x, y, z, vx, vy, vz]` |
| `r, v = s[:3], s[3:]` | First 3 = position, last 3 = velocity |
| `a = -MU * r / norm(r)**3` | Same as `-g * x / r` for all 3 parts at once (`MU/r³·x = (MU/r²)·(x/r)`) |
| `np.hstack([v, a])` | The rates: `[vx, vy, vz, ax, ay, az]` |
| `energy drift`, `end position error` | The same two checks as ours |

---

## Python learned along the way

`import`, variables, `e14` / `e3` notation, `**` (power), `round()`, `print()`,
`while` loop, `and`, `if / else`, `min()`, `math.sqrt`, lists `[ ]` + `.append()` + `len()` + `xs[0]` / `[-1]`,
`def` functions + `return`, unpacking `x, y, vx, vy = state`, `matplotlib` plotting, `numpy.linspace`, `scipy.integrate.solve_ivp`.
