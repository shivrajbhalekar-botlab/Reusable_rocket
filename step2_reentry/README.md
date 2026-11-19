# Step 2 — Make it fall back and land (air drag + deorbit burn)

**Goal:** bring the ball home from a 400 km orbit to the ground.
Air is the brake, a small engine burn aims us at the air.
Built one idea per file, same as Step 1.

## How to run

```bash
conda activate rocket
cd /hdd/projects/Rocket/step2_reentry
python step2_1_air.py            # or any other file
```

---

## The files, in order

| File | New idea | What you see |
|---|---|---|
| `step2_1_air.py` | **Air density** falls with height: `ρ = 1.225·e^(−h/8500)` | 1.23 → 0.378 (10 km) → 9.5e-6 (100 km) kg/m³ |
| `step2_1b_air_slices.py` | Building that formula from 1 m slices ("lose 1/8500 per meter") | loop 0.3777 = formula 0.3777 |
| `step2_2_drag.py` | **Drag** `½·ρ·v²·Cd·A` on a falling ball, terminal speed | 1 kg ball from 1000 m: 32.7 s, lands at 33 m/s (no air: 14.3 s, 140 m/s) |
| `step2_2b_drag_table.py` | Drag at different speeds vs weight | drag = weight (9.82 N) at 33 m/s |
| `step2_2c_speed_plot.py` | Speed levels off at terminal speed | curve rises and flattens at 33 m/s; thrown at 60 → slows to 33 |
| `step2_3_throw_with_air.py` | **Drag in 2D**: points opposite to the velocity | sideways throw lands shorter; `Cd = 0` gives back Step 1.3 exactly |
| `step2_4_orbit_drag.py` | Drag in the orbit, density from current height | 180 km orbit decays and falls; 190 km lasts ~3× longer |
| `step2_5_deorbit_burn.py` | **Deorbit burn**: slow down 100 m/s at 400 km | no air: 400 ↔ 58 km forever; with air: caught at the bottom, lands |
| `step2_5b_down_and_sideways.py` | Split velocity into **down** and **sideways** | down speed peaks ~200 m/s; sideways 7573 → 7975 → 7573 |
| `step2_6_g_force.py` | **g-force** = how hard the air brakes | peak ≈ 7.5 g at ≈ 62 km; 1 g at the end |
| `step2_7_reentry_solve_ivp.py` | **`solve_ivp` + event** to stop at the ground | same reentry, more accurate |

---

## Key formulas

| What | Formula | Code |
|---|---|---|
| Air density | `ρ = ρ₀·e^(−h/H)`, ρ₀ = 1.225 kg/m³, H = 8500 m | `RHO0 * math.exp(-h / H)` |
| Scale height | `H = R·T/(M·g)` ≈ 8.4 km | |
| Drag force | `F = ½·ρ·v²·Cd·A` (newtons) | `0.5 * rho * speed**2 * Cd * A` |
| Drag acceleration (2D) | strength `F/m`, direction **opposite to velocity** | `-(drag/m) * vx / speed` |
| Total acceleration | gravity (to center) + drag (against motion) | `ax = -g*x/r - (drag/m)*vx/speed` |
| Terminal speed | `v_t = √(2·m·g / (ρ·Cd·A))` | |
| Deorbit burn | new speed = orbit speed − Δv | `vx = math.sqrt(MU / y) - dv` |
| g-force | `(drag/m) / 9.81` | `drag / m / G0` |
| Skater rule | sideways speed × distance from center = constant | |

---

## The ideas to remember

**1. Air thins exponentially.**
Air is squashed by the weight above it, so each meter up loses the same *fraction* (1/8500).
Every 8.5 km (the **scale height**) it's 2.7× thinner; every 5.9 km it halves. Above ~100 km almost nothing is left.

**2. Drag grows with speed squared.**
Moving through air you hit `ρ·A·v` kg of air per second and shove it at ~`v` → force ∝ `ρ·A·v²`.
`Cd` is the shape correction (sphere 0.47, flat plate 1.2, capsule ~1.3).
Twice the speed → 4× the drag.

**3. Terminal speed.**
Drag grows until it equals the weight → no net force → speed stops changing.
It depends on `m`, `Cd`, `A` and `ρ` (heavier → faster; bigger/blunter → slower; higher up → faster).
The *same* object lands at the *same* speed whether dropped from 1 km or from orbit.
At terminal speed the braking is always **1 g** (drag = weight), for any object.

**4. Drag is a vector, like gravity — just a different arrow.**
Gravity points opposite to the *position* (to the center): `x/r`.
Drag points opposite to the *velocity*: `vx/speed`.

**5. Orbits barely decay where there's no air.**
Our simple air has ~nothing at 400 km, so we used 180 km to see decay.
Lower orbit → thicker air → more drag → lower still: it speeds up and ends in a plunge.
10 km higher lasts ~3× longer (e^(10/8.5)).

**6. Braking in orbit lowers the *other* side.**
A 100 m/s burn at 400 km doesn't drop you straight down; it turns the circle into an oval with its
low point (58 km) half a lap away.
Without air it swings 400 → 58 → 400 forever, like a swing (falling speeds it up, so it overshoots and climbs back).
With air, the drag at the bottom takes its energy and it can't climb back → it lands.
The burn *aims* you at the air; the air does 98.7% of the braking for free.
- Too small a burn (20 m/s → low point 330 km): no air there, stays in orbit.
- Too big (300 m/s): low point underground → hits the ground even without air.

**7. "Down" and "sideways" rotate as you go around Earth.**
`vx`, `vy` are fixed screen directions, not "sideways/down" for the ball.
Gravity only ever adds *down* speed (it's always ⟂ to sideways), but a quarter-lap later that old
"down" direction has become "sideways" — that's how sideways speed grows while sinking.
Skater check: 7573 m/s × 6771 km = 7975 m/s × 6429 km.

**8. Circle vs oval vs crash.**
Circle: sideways speed = orbit speed **and** down speed = 0.
A little off: oval — still an orbit. Far off: crash (or escape).

**9. Reentry has three zones** (1 kg ball, 100 m/s burn):
1. 400 → ~110 km: coasting, speeding up slightly (the swing), 0 g.
2. ~110 → ~45 km: the big braking — thicker air vs dropping speed fight, peak ≈ 7.5 g at ≈ 62 km.
3. ~45 km → ground: terminal speed, 1 g.
The **peak g doesn't depend on mass** (4 kg: same 7.5 g, ~12 km lower) — it depends on the **entry angle**
(a bigger burn = steeper entry = more g).

**10. Euler wobble.**
Our own loop (update speed, then position) makes a circular orbit very slightly oval: ±0.4 km at dt = 0.1,
±0.04 km at dt = 0.01. It doesn't grow. `solve_ivp` (Step 2.7) doesn't have it.

---

## `solve_ivp` events (Step 2.7)

```python
def hit_ground(t, state):
    x, y, vx, vy = state
    return math.sqrt(x**2 + y**2) - RE   # altitude: > 0 in the air, 0 at the ground

hit_ground.terminal = True    # stop when it happens
hit_ground.direction = -1     # only when going DOWN through 0

sol = solve_ivp(dynamics, [0, t_end], state0, events=hit_ground, ...)
t_land = sol.t_events[0][0]          # when
state_land = sol.y_events[0][0]      # the exact state at that moment
```

---

## Honest limitations of this model

- **Air model** is good below ~80 km only. At 400 km the real air is ~a billion times denser than ours;
  at 100 km ours is too dense. Fine for reentry, wrong for slow orbit decay.
- **Instant burn** — a real deorbit burn takes minutes.
- **No heating** — a real 1 kg ball would burn up.
- **No lift** — real capsules tilt to get a little lift and reduce peak g to ~4 g.
- **2D, non-rotating Earth.**

---

## Python learned in Step 2

`math.exp`, `for ... in [list]`, `for i in range(n)`, f-strings (`{x:.3g}`, `{x:.4f}`), docstrings,
`abs()`, `max()`, `list.index()`, `list[-1]`, `plt.axhline`, `label=` + `plt.legend()`,
`plt.subplot(rows, cols, n)`, `np.arange`, `solve_ivp` events (`.terminal`, `.direction`, `sol.t_events`, `sol.y_events`).
