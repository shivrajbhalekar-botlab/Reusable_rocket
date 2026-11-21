# Rocket Simulation — Project Context & Handoff

> **Read this whole file before doing anything in a new session.**
> It records what we built, how the user wants to be taught, the decisions made,
> open issues, and exactly where to resume.
> Last updated: 2026-11-18 (end of session 1).

---

## 1. What this project is

The user is **learning** by building a **reusable-rocket simulation** in Python, from zero.
The goal is understanding, not just working code. The user wants to be taught
**step by step, in very, very small steps**, so they understand every line and every bit of physics.

### The big roadmap (6 big steps)

| # | Big step | Status |
|---|---|---|
| 1 | Make an object orbit Earth (simulation setup) | ✅ **Done** |
| 2 | Make it fall back and land: air drag + deorbit burn → reentry | ✅ **Done** (2.1–2.7, README written) |
| 3 | Replace the object with a rocket: mass, engine, thrust, fly up | 🔄 **In progress** (at 3.5; re-explaining 3.4) |
| 4 | Countdown (timer + checks) and stage separation (split into two objects) | ⏳ |
| 5 | Bring the booster back: boostback, descent, G-FOLD landing burn | ⏳ |
| 6 | Make it look good: 3D viewer, plots, Monte Carlo runs | ⏳ |

### The user's FINAL VISION (stated 2026-11-19)

> "Show a site on the Earth, set the time of launch, launch the rocket, it goes up, places a payload in orbit,
> and some (the booster) comes back down."

Agreed design: **two parts, like a drone flight log replay** —
(1) our Python physics sim writes, for every second, time + position of rocket / booster / payload to a file;
(2) **CesiumJS** (free, open-source browser 3D globe with built-in clock/timeline/play button) plays it back:
launch-site marker (example used: Sriharikota 13.7°N, 80.2°E), yellow ascent, blue payload orbit, red booster return,
launch time = the clock start. (Cesium can run without an ion token using its bundled NaturalEarthII imagery.)

New physics this requires (added to the roadmap): **3D**, **launch site lat/long → position**, **rotating Earth**
(site moves ~450 m/s at 13.7°N; launch time sets the site's orientation in space), **staging**, **booster return**.

Updated roadmap detail:
- Step 3: 3.5 vertical flight through air → 3.6 tilt over (gravity turn) → 3.7 reach orbit (all 2D)
- Step 4: 4.1 move to 3D → 4.2 launch site (lat/long) → 4.3 rotating Earth + launch time → 4.4 countdown →
  4.5 stage separation (booster + upper stage = two objects) → 4.6 payload into orbit
- Step 5: booster return (boostback → reentry → landing burn / G-FOLD)
- Step 6: export trajectory → CesiumJS globe with timeline (optionally cross-check with RocketPy; Isaac/Gazebo/KSP+kRPC alternatives)

Rule: **don't start the next step until the current one runs and is understood.**
Each big step is broken into mini-steps (1.1, 1.2, ...), each adding **one** new idea.

---

## 2. HOW TO TEACH THIS USER (most important section)

A new session must behave exactly like this.

### 2.1 Hard rules

1. **Never run shell commands for the user.** Do not use Bash to install, create envs, run scripts,
   move files, or even to check things. Give the exact command in a code block, explain each part
   briefly, say what output to expect, and wait for the user to report back.
   (The user explicitly said: *"tell me the command, never run the command."*)
   Creating/editing files with the file-writing tools is fine and expected.
2. **One new idea per mini-step.** If something needs several new ideas, split it.
   It's fine — preferred — to re-plan and split further when a step looks big
   (we did this: Step 1 grew from 5 to 8 mini-steps).
3. **Wait for "next".** Never jump ahead or bundle the next mini-step in.
4. **Since we don't run code, compute expected outputs by hand, carefully.**
   If not 100% certain of the last digit, say "roughly" / "the last digit may differ".
   Never claim something was run/verified when it wasn't.
5. The user writes casually with typos and sometimes Hindi words ("accha" = "okay/I see").
   Never comment on typos. Respond in English.
6. **Teach only what is used in real life** (user's request, 2026-11-19). Every mini-step gets a short
   **"Used in real life"** section (who uses it, a real example, the real standard/tool). Simplifications are allowed only
   as stepping stones, clearly labelled "real engineers do X instead", with a planned mini-step that upgrades to the real
   method (see the "Real-life upgrades" list in §6b).

### 2.2 Format of every mini-step reply

1. One line: what the **one new idea** is.
2. Create the file `stepN_reentry/stepN_M_name.py` (small, heavily commented, plain Python).
3. **Run command** in a code block (`python stepN_M_name.py`, run from inside the step folder).
4. **Expected output** in a code block.
5. **"The big idea"** — plain-language explanation, often with an ASCII diagram.
6. **"What's new, line by line"** — explain only the lines that are new (bullets or a table).
   Explain Python syntax too (e.g. `e14`, `**`, `for`, f-strings, `range`) the first time it appears.
7. **"Your one experiment"** — change ONE number, ask the user to **guess before running**,
   then give the expected result and the lesson it teaches.
8. End with: **"Type next when this makes sense"** (and invite questions on any unclear line).

### 2.3 When the user asks "explain X" / "I didn't understand X"

- Slow down. Derive from scratch with **tiny easy numbers** (e.g. 3-4-5 triangle, g = 10).
- Use **ASCII diagrams** and **tables**, and finish with a **numeric check** that ties the
  explanation to numbers they've already seen in their own output.
- Link back to earlier mini-steps ("same as Step 1.2's dt lesson").
- Physics at intuition level; avoid calculus. If something truly needs calculus, say
  "accept this for now" and give the intuition.
- Often add a tiny verification script or experiment (e.g. `step2_1b_air_slices.py`).
- End by asking which part is still unclear, or "type next".

### 2.4 Code style (keep consistent)

- Plain Python + `math` first. `numpy` only when needed (introduced in 1.8 for `linspace`).
- Variable names: `x, y, vx, vy, ax, ay, r, g, t, dt`, constants `MU, RE, RHO0, H` in CAPS.
- Hand-written loops use **semi-implicit Euler**: update velocity first, then position
  (`vx = vx + ax*dt` then `x = x + vx*dt`). Don't mention the name unless asked.
- 2D for now (x, y), Earth's center at (0, 0), ball starts at `(0, RE + 400e3)`.
- Units: SI (m, s, kg) inside code; convert to km only for printing/plotting.
- Each step folder gets a `README.md` summarizing the step (user asked for this for Step 1).
- Be honest about model limitations (e.g. the simple atmosphere is wrong above ~80 km).

---

## 3. Environment

- OS: Linux. Conda at `~/miniconda3`.
- Project env: **conda env `rocket`**, Python 3.12, from conda-forge:
  ```bash
  conda create -n rocket -c conda-forge --override-channels python=3.12 numpy scipy matplotlib
  conda activate rocket
  ```
- User confirmed the env works (`step1_1_gravity.py` printed `gravity = 9.82 m/s^2`).
- VS Code interpreter should be set to **rocket (conda)**.
- The project is now a **git repository** (the user ran `git init` themselves on 2026-11-19).
- Earlier a `.venv/` and `requirements.txt` were created in the root by mistake (user preferred conda).
  The user was told to delete them with `rm -rf .venv requirements.txt` — **not confirmed** whether they did.

---

## 4. Project layout (current)

```
/hdd/projects/Rocket/
├── context.md                       ← this file
├── step1_orbit/                     ← Big Step 1 (DONE)
│   ├── README.md                    ← full Step 1 notes: files, formulas, ideas, mapping to original
│   ├── step1_orbit.py               ← the ORIGINAL compact 3D script (numpy, solve_ivp, DOP853)
│   ├── step1_1_gravity.py
│   ├── step1_2_drop.py
│   ├── step1_3_throw.py
│   ├── step1_4_down.py
│   ├── step1_5_fall_from_space.py
│   ├── step1_6_orbit.py
│   ├── step1_7_draw.py
│   ├── step1_8_solve_ivp.py
│   └── *.png                        ← saved plots (orbit.png, step1_7_orbit.png, step1_8_orbit.png)
└── step2_reentry/                   ← Big Step 2 (IN PROGRESS)
    ├── step2_1_air.py
    └── step2_1b_air_slices.py
```

The user moved Step 1 files into `step1_orbit/` and Step 2 files into `step2_reentry/` themselves
(they said "done"). Scripts save PNGs with relative paths, so **run each script from inside its folder**.

---

## 5. What we built — Step 1 (orbit), mini-step by mini-step

Full notes are in `step1_orbit/README.md`. Summary:

| Mini-step | File | New idea | Expected output |
|---|---|---|---|
| 1.1 | `step1_1_gravity.py` | `g = MU / r²`; `e14`, `**` | `gravity = 9.82 m/s^2`; experiment `r = RE + 400e3` → 8.69 |
| 1.2 | `step1_2_drop.py` | **Time loop** (`while`, `dt`), state `h, v, t`, up = + | dt=1: ends at t=5, h=-47.3 (overshoot!); dt=0.1: t=4.5, h=-1.6, v=-44.2. True: 4.51 s, 44.3 m/s |
| 1.3 | `step1_3_throw.py` | **2D**: `x, y, vx, vy`; flat ground | `landed after 4.51 s`, `90.2 m away`; vx=200 → same 4.51 s, 902.0 m |
| 1.4 | `step1_4_down.py` | **Round Earth**: origin at Earth's center, `r = sqrt(x²+y²)`, `ax = -g*x/r` | at (0, 6771 km): `ax=-0.0, ay=-8.69`; at (6771 km, 0): `ax=-8.69` |
| 1.5 | `step1_5_fall_from_space.py` | Round-Earth gravity **inside** the loop | dropped from 400 km: ~300.3 s (5.0 min), ~2719 m/s, x=0 |
| 1.6 | `step1_6_orbit.py` | **Orbit speed** `vx = sqrt(MU/y)` ≈ 7673 m/s; `and`, `if/else`, `min()` | `still flying after 100.0 min`, `lowest altitude = 400 km`; vx=7000 → CRASHED |
| 1.7 | `step1_7_draw.py` | **Lists + matplotlib** (`append`, `len`, `xs[0]`, `plt.Circle`, `axis("equal")`) | red circle around blue Earth; vx=8000 → ellipse reaching ~1700 km |
| 1.8 | `step1_8_solve_ivp.py` | **`solve_ivp`**: `def dynamics(t, state)` returns rates `[vx, vy, ax, ay]`; DOP853, rtol 1e-10, atol 1e-6, `t_eval=np.linspace`; `sol.y` table, `sol.y[:, -1]` | period 92.41 min; gap ≈ 0.001 m; energy change ≈ 1e-12; `sol.nfev` far below our 55,000 |

### Concepts explained in depth during Step 1 (user understood all of these)

- **Components** of a vector: `ax = -g*x/r` = direction (`x/r`), flipped toward center (`-`), scaled by `g`.
  Taught with ball at (3,4), r=5, g=10 → ax=-6, ay=-8, √(36+64)=10. User summarized it as "taking the components" — confirmed.
- **Orbit speed derivation ("fall = drop")**: fall in time t = ½gt²; ground curves away by (vt)²/(2r)
  (Pythagoras, drop² neglected); equal → g = v²/r → v = √(MU/r). Check at 400 km for 1 s: both 4.35 m.
  Mentioned centripetal acceleration v²/r.
- **Escape speed** (user discovered it by increasing vx): energy budget ½v² vs MU/r → v_esc = √(2MU/r)
  = √2 × v_orbit = 10,851 m/s at 400 km (11,186 m/s from surface). Energy `E = ½v² − MU/r`:
  negative = trapped, ≥ 0 = escapes. Suggested adding an energy print to `step1_7_draw.py`
  (vx=7673 → E ≈ -29.4 million J/kg; 10800 → slightly negative; 11000 → positive).
- **Accuracy vs work trade-off** (dt in 1.2; rtol in 1.8).
- **How to verify a sim**: returns to start after one period; energy conserved.
- **Mapping to original `step1_orbit.py`**: `a = -MU*r/norm(r)**3` ≡ `(MU/r²)(x/r)` for all 3 axes; `np.hstack([v, a])` = rates.

### Python learned so far

`import`, variables, `e` notation, `**`, `round()`, `print()`, `while`, `and`, `if/else`, `min()`,
`math.sqrt`, `math.exp`, lists (`[]`, `.append`, `len`, indexing `[0]`, `[-1]`), `def`/`return`,
docstrings, tuple unpacking, `for ... in [list]`, `for i in range(n)`, f-strings with `:.3g` / `:.4f`,
matplotlib basics, `np.linspace`, `scipy.integrate.solve_ivp`, numpy row/column indexing `sol.y[:, -1]`.

---

## 6. Step 2 (reentry) — where we are

### Plan for Step 2

| Mini-step | Idea | Status |
|---|---|---|
| **2.1** | How thick is the air at each height? Exponential atmosphere | ✅ done, understood (incl. scale height) |
| 2.2 | Air drag on a falling ball (1D, like Step 1.2 + drag) → terminal speed | ✅ done (+ 2.2b drag table, 2.2c speed plot) |
| 2.3 | Throw sideways WITH air: drag as a 2D vector opposite to velocity (flat ground, constant rho) | ✅ done |
| 2.4 | Add drag to the orbit (own Euler loop, `air_density(r - RE)`, start 180 km) | ✅ done (user tested RHO0 = 0 → saw ±0.4 km Euler wobble, explained) |
| 2.5 | Deorbit burn: instant retrograde dv = 100 m/s at 400 km → perigee ~58 km → captured by air | 🔄 **file given, waiting for user** |
| 2.6 | G-force during reentry (`step2_6_g_force.py`: braking = drag/m / G0; speed & g vs altitude) | ✅ done (m=1: 7.5 g @ 62 km; m=4: 7.5 g @ 50 km) |
| 2.7 | Switch reentry to `solve_ivp` + `events` (stop at ground, no Euler wobble); then write `step2_reentry/README.md` | 🔄 **file given, waiting for user** |

(Step 2 was re-split on 2026-11-18: old 2.3/2.4/2.5 became 2.4/2.5/2.6.)

### 2.1 files

- `step2_1_air.py`: `RHO0 = 1.225`, `H = 8500.0`, `def air_density(h): return RHO0 * math.exp(-h / H)`,
  `for` loop over `[0, 10, 50, 100, 400]` km, f-string `:.3g`.
  Expected: 1.23, 0.378, 0.00342, 9.52e-06, 4.47e-21 kg/m³.
  Experiment: add 8.5 km → 0.451 (37%). Also suggested `RHO0 * 0.889 ** (h/1000)` gives ~same numbers.
  Experiment with `H = 4250` → ~0.116 at 10 km.
- `step2_1b_air_slices.py`: builds the formula with a loop of 10,000 × 1 m slices,
  `rho = rho - rho*dh/H`; prints loop `0.3777` vs formula `0.3777`.
  Experiment: `dh = 1000`, `range(10)` → loop 0.3504 vs 0.3777 (big slices ≈ 7% wrong).

### 2.1 concepts explained (in this order)

1. Density = kg of air per m³; `RHO0` = 1.225 at sea level.
2. Why air thins: "stack of pillows" — bottom air carries the weight of all air above.
3. Same **fraction** lost per km (~11%, keep 0.889) → exponential decay.
4. Full derivation: pressure = weight of air above (column ≈ 10,300 kg on 1 m², 101,325 Pa);
   thin slice: ΔP = ρgΔh; gas law P = ρ·RT/M (RT/M ≈ 82,600; check 1.225×82,600 ≈ 101,200 Pa);
   fraction lost = Δh·gM/(RT) = Δh/H; H = RT/(Mg) ≈ 8,400 m (we use 8,500); repeating tiny slices → e^(−h/H).
5. **Scale height H** (last thing explained): the climb for air to get 2.7× thinner (37% left);
   "half height" = 5.9 km (density halves every 5.9 km); H = height of the atmosphere if squashed to
   uniform sea-level density (1.225 × 8500 ≈ 10,400 kg/m², matches the column); hotter → bigger H,
   heavier gas or stronger gravity → smaller H; Mars H ≈ 11 km.

### ▶ RESUME HERE

Step 2.2 done and understood. The user was new to the drag formula; it was derived from scratch
(air hit per second ρAv × speed given v → ρAv², then ½·Cd shape correction; Cd table; dynamic pressure;
drag-vs-weight table → terminal speed 33 m/s; self-correcting; approaches gradually, 90% at 5 s).
Extra files: `step2_2b_drag_table.py` (user ran it, output matched), `step2_2c_speed_plot.py`
(speed vs time with `plt.axhline` + `legend`; experiment v = -60 → slows down to 33).
The user's `step2_2_drag.py` now has an extra line `v = -60` (their experiment).

**Step 2.3 file `step2_reentry/step2_3_throw_with_air.py` has been given** (Step 1.3 + drag:
`speed = sqrt(vx²+vy²)`, `ax = -(drag/m)*vx/speed`, `ay = -g - (drag/m)*vy/speed`, constant rho, flat ground).
Expected (rough hand estimate, NOT exact): lands after ~5.0 s, ~60 m away (no air: 4.51 s, 90.2 m).
Experiment: `Cd = 0` → exactly 4.51 s and 90.2 m (Step 1.3 numbers). Avoid any experiment
with zero starting speed (division by zero in `vx / speed`).
User did 2.3 (didn't report numbers; they also tried `rho = 0`, left as a comment on line 14).

**Step 2.4 file `step2_reentry/step2_4_orbit_drag.py` has been given.** Decision taken: used our own
semi-implicit Euler loop (dt = 0.1, t_end = 10 h), NOT solve_ivp, so no `events` are needed yet to stop at
the ground; gravity + drag added in `ax`, `ay`; `air_density(r - RE)`; 1 kg ball; **start at 180 km** (not 400)
because the simple atmosphere has ~no air at 400 km (told the user honestly). Plots altitude vs time (hours).
Expected (orbit-averaged hand estimate, rough): decays over ~2.7 orbits (period ~88 min) → lands after
roughly 4 hours, landing speed ≈ 33 m/s (sea-level terminal speed, same as 2.2). Real ball would burn up.
Experiment: start at 190 km + set `t_end = 24 * 3600` → lasts ~3.2× longer (e^(10/8.5)) → roughly 13 hours.
User finished 2.4 (no numbers reported).

**Step 2.5 file `step2_reentry/step2_5_deorbit_burn.py` has been given.** Same Euler loop as 2.4 (dt 0.1,
t_end 3 h), start 400 km circular, `vx = v_orbit - dv` with dv = 100 (instant burn — simplification).
Hand calc (vis-viva): perigee ≈ 58 km (rp = ra / (2MU/(ra·v²) − 1)); half-period of that ellipse ≈ 44.5 min.
Expected (rough): `orbit speed = 7672.6, after burn = 7572.6`; lands after roughly 45–60 min, ~33 m/s,
on the far side of Earth. Plot: altitude vs time (minutes); prints lowest altitude.
Experiments: dv = 20 → perigee ≈ 330 km → no air → "still flying after 180 min", lowest ≈ 330 km.
Bonus: RHO0 = 0 with dv = 100 → never lands, lowest ≈ 58 km (the burn alone doesn't land you; the air does).
**2.5 needed a lot of re-explaining (the user found it hard). What finally worked, in order:**
- Plain goal first: "bring the ball home; no air at 400 km; air only low down; how do we get it into the air cheaply?"
- Run A (`RHO0 = 0`, dv = 100): user saw the 400 ↔ 58 km wave themselves (lowest = 58 km matched hand calc).
- "Why does it climb back up?": falling speeds it up → overshoot like a **swing** / a braking car
  (fall > drop 400→~225 km builds down speed; fall < drop 225→58 km brakes it; at 58 km down speed = 0, then climbs).
- `step2_5b_down_and_sideways.py`: splits velocity into down (radial, `away = vx*x/r + vy*y/r`) and sideways
  (`sqrt(speed² − away²)`), plots both + orbit speed needed (`plt.subplot`). Down speed peaks ~200 m/s;
  sideways 7573 → 7975 → 7573 (skater rule: sideways speed × r = const = 51.27 million).
- Important correction: in code, `vx`/`vy` are fixed screen axes, NOT sideways/down (those rotate around Earth).
- "Must sideways = orbit speed to stay in orbit?" → equal + zero down speed = circle; a little off = oval (still orbit);
  far off = crash/escape. The 3-case version (Step 1.6 circle / 2.5 plot oval / 7000 crash) landed best.
- **What finally answered "what increases sideways speed if gravity is ⟂ to sideways?":** the user was right that gravity is
  always ⟂ to sideways. Gravity only creates DOWN speed; as the ball moves around Earth, "down" rotates, so the old
  down-velocity arrow becomes sideways a quarter-turn later (diagram: ↓ at the top = sideways on the right side).
  The "bicycle downhill / gravity partly along the motion" explanation CONFUSED them — avoid it.
- User said "ohk then what next" → they still need to do **Run B** (`RHO0 = 1.225`, dv = 100) to see the air catch the ball.
User then asked "terminal speed differs per shape?" → yes; v_t = √(2mg/(ρCdA)); examples: ball 33, m=4 → 66,
flat plate 21, 2× radius 16.5, ball at 10 km ≈ 59 m/s; raindrop ~9, skydiver ~55, parachute ~5.
User said "next" WITHOUT reporting Run B numbers.

**Step 2.6 file `step2_reentry/step2_6_g_force.py` given** (same loop as 2.5 Run B; `G0 = 9.81`; records altitude,
speed, braking g = drag/m/G0; `max()`, `list.index()`; `plt.subplot(1, 2, n)`; altitude on the vertical axis).
Expected — NOT computable exactly by hand, told the user so: peak roughly ~8 g (shallow ballistic entry, like
Soyuz/Vostok ballistic mode), at roughly 60–70 km; speed plot shows speed rising 7573 → ~7900 while sinking
(the "swing"), then a sharp drop. Experiment: m = 4 → peak g about the SAME, but ~12 km lower (H·ln4)
— Allen–Eggers: peak g doesn't depend on mass/shape, only where it happens does.
**User ran 2.6 (plots shared):** m = 1 → peak ≈ 7.5 g at ≈ 62 km; m = 4 → peak ≈ 7.5 g at ≈ 50 km (12 km lower) — both
predictions confirmed. Explained the 3 zones (coast/swing 0 g → braking spike, ρ-vs-v² tug-of-war → terminal speed).
CORRECTION made to the user: near the ground the braking is **1 g, not 0** (terminal speed: drag = weight).
The user may have left `m = 4.0` in step2_6_g_force.py (told to restore 1.0).
Also explained: same Cd ≠ same terminal speed (m=1 → 33, m=4 → 66 m/s); what IS universal is 1 g at terminal speed;
same object → same landing speed whether dropped from 1 km or from orbit. Suggested adding
`print("landing speed =", round(speeds[-1]), "m/s")` to 2.6.

**Step 2.7 file `step2_reentry/step2_7_reentry_solve_ivp.py` given:** `dynamics` with gravity + drag; event function
`hit_ground` returns altitude, `.terminal = True`, `.direction = -1`; DOP853 rtol 1e-10, atol 1e-6,
`t_eval = np.arange(0, 3 h, 1 s)`, `events=hit_ground`; results from `sol.t_events[0][0]`, `sol.y_events[0][0]`;
g-force recomputed in a `for k in range(len(sol.t))` loop with `sol.y[:, k]`; same 2-panel plot as 2.6.
Expected: should closely match 2.6 (≈ 7.5 g at ≈ 62 km, landing ≈ 33 m/s); nfev unknown.
Experiment given: dv = 200 (steeper entry; perigee would be ~260 km underground) → peak g goes UP clearly
(exact value not hand-computed), confirming "peak g depends on entry angle". DON'T suggest removing
`.terminal` (below ground the density formula explodes → stiff, may hang) or a dv too small to land
(`sol.t_events[0][0]` → IndexError).
User said "done next" without numbers. **Step 2 is complete**; `step2_reentry/README.md` written (files, formulas,
10 ideas, events, honest limitations, Python learned).

---

## 6b. Step 3 (rocket) — where we are

Folder: `step3_rocket/`. Plan:

| Mini-step | Idea | Status |
|---|---|---|
| 3.1 | **Thrust**: constant force up, constant mass, 1D, flat, constant g; thrust-to-weight | ✅ done |
| 3.2 | Burning fuel: mass decreases (ṁ), acceleration grows as it lightens; engine cuts off when fuel is gone | ✅ done |
| 3.3 | Where thrust comes from: thrust = ṁ × exhaust speed (`step3_3_exhaust.py`) | ✅ done |
| 3.4 | Rocket equation Δv = vₑ·ln(m₀/m_f), checked against the sim (`step3_4_rocket_equation.py`) | ✅ done |
| 3.5 | Fly straight up through air: engine ON phase, then engine OFF coast to apogee (`step3_5_fly_up.py`) + plot | ✅ done |
| 3.5b | Real atmosphere: US Standard Atmosphere 1976 layers (`step3_5b_real_air.py`) | ✅ done |
| 3.5c | Fly 3.5 with the real air; atmosphere moved to its own module `atmosphere.py` (`step3_5c_fly_real_air.py`) | ✅ done |
| 3.5d | Max Q: dynamic pressure q = ½ρv² (`step3_5d_max_q.py`) | ✅ done (user ran ve×2 experiment) |
| 3.5e | Speed of sound + Mach number (`step3_5e_mach.py`; `speed_of_sound(T)` added to `atmosphere.py`) | ✅ done (plot explained) |
| 3.5f | Cd vs Mach drag curve with `np.interp` (`step3_5f_cd_mach.py`) | ✅ done |
| 3.5g | Thrust vs altitude: thrust = thrust_vac − P·Ae (`step3_5g_thrust_altitude.py`) | ✅ done (accepted as a rule) |
| 3.5h | Real rocket numbers: Falcon 9-like first stage straight up (`step3_5h_real_rocket.py`) | ✅ done (Isp re-explained) |
| 3.6a | Same F9 flight on the ROUND Earth: x, y, vx, vy; g = MU/r² (`step3_6a_round_earth.py`) | ✅ done |
| 3.6b | Tilt: thrust leans a fixed 5° from vertical after 10 s (`step3_6b_tilt.py`) | 🔄 **file given, waiting for user** |
| 3.6c | Gravity turn: thrust follows the velocity; plot the path around Earth | ⏳ |
| 3.7 | Reach orbit (solve_ivp) | ⏳ |

**3.1 file `step3_rocket/step3_1_thrust.py`:** m = 1000 kg, thrust = 15000 N, g = 9.82, dt = 0.01,
`for i in range(round(burn_time / dt))` (avoids float drift of a `while t < 10`), `a = (thrust - weight) / m`.
Hand-computed (exact for this scheme): weight = 9820 N; a = 5.18 m/s²; after 10 s: v = 51.8 m/s,
h = a·dt²·n(n+1)/2 = 259.3 m (exact physics: 259.0). Thrust-to-weight = 1.53 (Falcon 9 ≈ 1.4, Saturn V ≈ 1.2).
Experiment: thrust = 9820 → a = 0, sits on the pad (h = 0, v = 0) — hover; T/W must be > 1 to lift off.
Don't suggest thrust < weight: the code has no ground, so it would sink below the pad.
User did 3.1 ("done next", no numbers).

**3.2 file `step3_rocket/step3_2_burn_fuel.py`:** dry 200 kg + fuel 800 kg, ṁ = 10 kg/s (80 s burn), thrust 15000 N,
no air, flat, g = 9.82; loop: a with current m → v → h → `m -= mdot*dt`; `for` over round(80/0.01) slices.
Exact physics (vₑ = T/ṁ = 1500 m/s): v = 1500·ln5 − 9.82·80 = 1628.6 m/s; h = 1500·(800 − 200·ln5)/10 − ½·9.82·80² = 40.29 km.
Expected print: liftoff a = 5.18; engine off after 80 s; mass left 200; a before cutoff ≈ 65.1 (exact at 200 kg: 65.2);
speed ≈ 1628; height ≈ 40.3 km. Compare: constant 1000 kg for 80 s would give only 414 m/s.
Experiment: dry 100 / fuel 900 → 90 s burn, ≈ 2570 m/s, ≈ 60.7 km, ~140 m/s² (14 g) at cutoff.
User did 3.2 ("done next", no numbers).

**3.3 file `step3_rocket/step3_3_exhaust.py`:** same as 3.2 but `ve = 1500.0`, `thrust = mdot * ve` (= 15000 N, so
identical results: 80 s, ≈ 1628 m/s, ≈ 40.3 km). Explained via skateboard-throwing-balls (same picture used for drag),
works in vacuum (pushes on its own exhaust, not on air), Isp = vₑ/9.81 (ours 153 s; kerosene ≈ 300 s → vₑ ≈ 3000;
hydrogen ≈ 450 s → vₑ ≈ 4400).
Experiment: ve = 3000 → thrust 30000 N, ≈ 4042 m/s, ≈ 112 km (exact: 3000·ln5 − 785.6 = 4042.7; h = 112.0 km).
User did 3.3 ("done next", no numbers).

**3.4 file `step3_rocket/step3_4_rocket_equation.py`:** g = 0.0 (deep space), same rocket; prints mass ratio 5.0,
sim ≈ 2414 and formula 2414 (1500·ln5 = 2414.2). Explained: each tiny burn gives ve·(dm/m) → same *fraction* burned =
same speed gain (halving mass always adds 0.693·vₑ) → adding tiny fractions gives ln (reverse of Step 2.1's e);
`math.log` = ln; diminishing returns table; orbit needs ~9,400 m/s → with vₑ = 3000 needs ratio ≈ 23 (96% fuel) →
motivates staging (Big Step 4).
Experiment: g = 9.82 → sim ≈ 1628 vs formula 2414; gap ≈ 786 = g × 80 s = **gravity loss** (why rockets burn fast).
Side question answered: "is there a Gazebo for rockets?" → no single standard; listed RocketPy (Python 6-DOF, Monte Carlo),
Basilisk (Python GNC/orbits), KSP + kRPC (most Gazebo-like, Python autopilot), OpenRocket, JSBSim (can bridge to
Gazebo/PX4), NASA GMAT, NASA Trick, Orbiter, Gazebo/Isaac Sim with a custom plugin. Suggested: finish our own physics
core first; in Step 6 cross-check with RocketPy and visualize with KSP+kRPC or Isaac Sim/Gazebo (user has drone/Isaac/ROS
background).
User asked how many steps are planned → answered: 6 big steps, ≈ 39 mini-steps (1: 8, 2: 7, 3: 7, 4: 6, 5: ≈6, 6: ≈5);
19 done. Proposed split — Step 5: 5.1 booster flies alone after separation → 5.2 boostback burn → 5.3 reentry →
5.4 simple 1D landing burn → 5.5 landing guidance (G-FOLD) → 5.6 full booster return. Step 6: 6.1 save flight to file →
6.2 Cesium globe + launch site → 6.3 play rocket/booster/payload on the timeline → 6.4 plots → 6.5 Monte Carlo.
Offered an early "preview" (Cesium globe with the Step 1 orbit); the user chose to continue instead.
**User asked that context.md be updated EVERY time** (saved as a memory too).

**3.5 file `step3_rocket/step3_5_fly_up.py`:** 1D vertical, constant g = 9.82, `air_density(h)`, same engine/tank as 3.3,
rocket radius 0.25 m (A = 0.196 m²), Cd = 0.5. Phase 1 (for loop, 80 s): `a = (thrust - m*g - drag)/m`;
phase 2 (`while v > 0`): `a = (-m*g - drag)/m`; prints burnout and apogee.
Expected — with air (COARSE hand integration, told the user it's rough): burnout ≈ 1200 m/s at ≈ 31 km;
apogee ≈ 90–100 km at t ≈ 190 s. At burnout drag (~2300 N) > weight (~1960 N).
Experiment: `RHO0 = 0` → exact-ish: burnout 1628 m/s at 40.3 km; apogee ≈ 175 km at t ≈ 246 s
(40.3 + 1628²/(2·9.82)). Lesson: the air cost ~80 km of height, mostly in the thick lower air
(why real rockets go up fast through it and are slim). Constant g at 175 km is a simplification (real ≈ 9.3).
In a new session: get their numbers (check vs the rough estimate); on "next" do 3.6 (tilt over / gravity turn, 2D round Earth).

**Re-explaining the rocket equation (2026-11-19):** after 3.5 was given, the user said "I did not understand the rocket equation".
Re-explained from scratch, no calculus: (1) the question it answers (final speed when tank is empty); (2) why you can't just
do a × t (a grows 15 → 75 m/s² as mass drops); (3) ONE kick: throw 1 kg back at 1500 m/s → rocket of m kg gains 1500/m
(skateboard; 100 kg person throws 1 kg at 10 m/s → 0.1 m/s); (4) same 1 kg gives more kick when lighter (1000 kg → 1.5,
500 → 3, 200 → 7.5 m/s); (5) add 800 kicks → ≈ 2411; ln is the shortcut for "add up 1/m pieces"; (6) halving rule:
every halving of mass gives the same 1040 m/s (0.693·vₑ): 1000→500: 1040, 500→250: 1040, 250→200: 1500·ln1.25 = 335 →
total 2415 ≈ 2414.
New file **`step3_rocket/step3_4b_fuel_chunks.py`**: `chunk = 1.0` kg; loop `kick = ve*chunk/m; v += kick; m -= chunk`.
Expected: first kick 1.5 (1000 kg); last kick 7.46 (201 kg); adding all kicks ≈ 2411.2; rocket equation 2414.2.
Experiment: `chunk = 0.01` → sum ≈ 2414.1 (smaller chunks → matches formula; same lesson as Step 2.1b slices).
Waiting for the user to confirm understanding; 3.5 (`step3_5_fly_up.py`) is still pending after that.
User then asked "is the rocket equation used in real life?" → yes: Tsiolkovsky 1903; Δv budget = like a drone's battery/flight-time
budget; LEO ≈ 7.8 km/s + ~1.5–2 km/s losses ≈ 9.4 km/s; mass-ratio table for vₑ 3000 (≈ 23) vs 4400 (≈ 8.5); used for staging,
engine choice, reusable booster landing-fuel reserve, spacecraft burns (Mars/Moon missions, orbit raising); real budgets add gravity/drag
losses on top (the user saw gravity loss in 3.4). Told them we'll use it in Step 4 (staging) and Step 5 (booster landing fuel).
User: "understood, next, now let's proceed with step3_5" → rocket equation understood (3.4b not reported). 3.5 re-presented.
Refined hand estimate for 3.5 (10 s chunks): burnout ≈ 1215 m/s at ≈ 31.4 km; air matters only until ~60 km
(v ≈ 850 m/s at ~62 km, t ≈ 110 s); apogee ≈ 98 km at t ≈ 196 s. Drag peaks ≈ 3600 N around t ≈ 55–60 s, h ≈ 12–14 km.
Still rough — ask for the user's numbers.

**User asked (2026-11-19): "teach only the things used in real life".** Answered: what we did is real (gravity law, orbit speed,
solve_ivp-type integrators, drag equation, deorbit burns, g-load, rocket equation, Δv budgets, 3.5 = sounding-rocket
flight profile, e.g. ISRO RH-200 from Thumba); listed our toy simplifications with the real replacement.
**Real-life upgrades list (proposed; awaiting user's choice of when):**
| toy now | real method | where |
|---|---|---|
| single-exponential air (H = 8.5 km) | US Standard Atmosphere 1976 (layered table; pressure + temperature + speed of sound) | new 3.5b |
| constant Cd | Cd changes with Mach number (peak near Mach 1, transonic) | new 3.5c |
| constant thrust | thrust changes with altitude (nozzle exit-pressure term: sea-level vs vacuum thrust/Isp) | new 3.5d |
| toy rocket (1000 kg, ve 1500) | real-ish numbers from a real vehicle (e.g. sounding rocket or Falcon 9-like stage) | 3.5e or 3.6 |
| constant g | inverse-square g (Step 1) — later J2 for Earth's bulge | 3.6 |
| hand-written Euler loop | solve_ivp / RK (already learned in 1.8, 2.7) | 3.7 onwards always |
| 2D, non-rotating Earth | 3D ECI/ECEF frames, WGS-84 launch site, Earth rotation | Step 4 |
| instant burns | finite burns with real thrust | Step 4/5 |
Recommendation given: do 3.5b–3.5d (+ real numbers) right now, one idea each, before 3.6.
User then said "explain 3_5" → gave a slow walkthrough of the file in 5 blocks (settings, rocket shape, start, phase 1 loop,
phase 2 loop) with 3 hand-computed snapshots: t = 0 (drag 0, a = 5.18); t ≈ 50 s (h ≈ 9.3 km, v ≈ 424, m = 500,
ρ ≈ 0.41, drag ≈ 3600 N, weight 4910, a ≈ 12.9); burnout (ρ ≈ 0.030, drag ≈ 2200 N > weight 1964 N);
coast at 70 km drag ≈ 8 N (negligible). Explained for vs while, minus sign on drag, apogee, Max Q preview,
"Used in real life": sounding rockets (ISRO RH-200/RH-300/RH-560 from Thumba/Sriharikota, NASA sounding rockets).
Still waiting for the user's actual 3.5 numbers.
User asked "smaller dt → more accurate?" → yes, but: error ∝ dt (halve dt → halve error); at dt 0.01 the dt error is only
~10 m in 175 km (~8 m at burnout = Δv·dt/2); cost: 10× smaller dt = 10× more loops (dt 1e-6 → hundreds of millions of loops,
plus float rounding); the MODEL errors are far bigger (constant g alone ≈ 4 km on the no-air apogee; toy air above 60 km;
constant Cd). Real-life practice taught: **convergence study** (halve dt until the answer stops changing) and adaptive-step
integrators (solve_ivp with rtol/atol). Suggested experiment: dt = 0.1 / 0.01 / 0.001 → only the last digit changes.
User asked for a minimal plot in 3.5 → added to `step3_5_fly_up.py`: `import matplotlib.pyplot as plt`; lists
`on_t, on_h` / `off_t, off_h` (new syntax: `a, b = [], []`), appended each slice (h in km); plot red = engine ON,
blue = coasting, labels, legend, grid, `savefig("step3_5_fly_up.png")`, `plt.show()`. Expected shape: red curve bending
upward (speeding up) to ~31 km at 80 s; blue curve keeps rising but flattens to a rounded top ≈ 98 km at ≈ 195 s.
User: "done next" (no numbers reported for 3.5). **3.5 done.**

**3.5b file `step3_rocket/step3_5b_real_air.py`** (NEW idea: the air comes in LAYERS with different temperatures →
US Standard Atmosphere 1976). Constants G0 = 9.80665, M = 0.0289644, R = 8.31446, R0 = 6356766; `LAYERS` list of tuples
(hb, Tb, L, Pb) with 8 layers (0/11/20/32/47/51/71/84.852 km; top layer isothermal 186.946 K, P 0.3734 — our extension above
86 km); `us_standard_atmosphere(h)` → geopotential hp = R0·h/(R0+h); find layer with `for` + `if hp >= layer[0]`;
L = 0 → P = Pb·exp(−G0·M·dh/(R·Tb)) (= Step 2.1 exponential, H = RT/(Mg)); L ≠ 0 → T = Tb + L·dh, P = Pb·(Tb/T)^(G0·M/(R·L));
ρ = P·M/(R·T); returns `T, P, rho` (multiple return values). Prints table with f-string widths `{km:4}`, `{x:6.1f}`, `{x:<10.3g}`.
Expected (hand-checked against official table values):
0 km 15.0 C 1.23 | 1.23; 10 km −49.9 C 0.414 | 0.378; 20 km −56.5 C 0.0889 | 0.116; 30 km −46.6 C 0.0184 | 0.0359;
50 km −2.5 C 0.00103 | 0.00342; 80 km −74.5 C 1.85e-05 | 0.0001. Old formula: 9% low at 10 km, 2× too high at 30 km,
3.3× at 50 km, 5.4× at 80 km → our 3.5 apogee was too LOW.
Experiment: add 40, 60, 70 km → real 0.0040 / 0.00031 / 8.28e-05 vs old 0.0111 / 0.00105 / 0.000325
(temps −22.8 / −26.1 / −53.6 C).
Used in real life: = ICAO ISA up to 32 km (aircraft altimeters, PX4 baro altitude), RocketPy default, ascent design;
above ~86 km real tools use NRLMSISE-00 / JB2008.
Renumbered upgrade plan: 3.5c = fly 3.5 with real air (apogee goes up) → 3.5d Cd vs Mach + Max Q → 3.5e thrust vs altitude →
3.5f real rocket numbers → 3.6 tilt over.
User: "done" (no numbers) → **3.5b done.**

**3.5c:** NEW module **`step3_rocket/atmosphere.py`** (same constants/LAYERS/`us_standard_atmosphere` as 3.5b, NO prints) —
reused from now on via `from atmosphere import us_standard_atmosphere` (must run from inside `step3_rocket/`).
File **`step3_rocket/step3_5c_fly_real_air.py`** = 3.5 (with plot) but `T, P, rho = us_standard_atmosphere(h)` in both loops;
RHO0/H/air_density removed. New ideas: own module + `from ... import ...` (real practice: one model, one file, reused).
Hand estimate (10 s chunks, ROUGH): burnout ≈ 1240 m/s at ≈ 31 km (about the same as old air: real air is a bit thicker
below ~10 km, much thinner above 20 km); coast loses much less to drag → apogee ≈ 105 km at ≈ 203 s
(old air estimate ≈ 98 km at ≈ 196 s → roughly +7 km). Drag negligible above ~60 km.
Experiment: Cd = 0 → no drag → exactly the 3.5 no-air numbers (40.3 km, 1628 m/s; apogee 175.3 km at 246 s) →
the REAL air costs ≈ 70 km of apogee for this small rocket.
Used in real life: separate model modules (atmosphere, gravity, engine) = how RocketPy/GMAT/Basilisk are organized.
User: "done next" (again no numbers) → **3.5c done.** Plan re-split: Max Q first (3.5d), then Mach + Cd(Mach) (3.5e),
thrust vs altitude (3.5f), real rocket numbers (3.5g).

**3.5d file `step3_rocket/step3_5d_max_q.py`:** 3.5c flight; NEW `q = 0.5*rho*v**2` (dynamic pressure), `drag = q*Cd*A`;
combined lists `ts, hs, vs, qs` (appended at the TOP of each slice, before updating); `max(qs)` + `qs.index()` (as in 2.6);
2 subplots: height vs time and q [kPa] vs time with red dot at Max Q; NEW `plt.axvline(burn_time, color="gray",
linestyle="--")` marks engine-off.
Hand estimate (ROUGH): Max Q ≈ 40 kPa at t ≈ 53–54 s, h ≈ 10.5–11 km, v ≈ 460–470 m/s (≈ Mach 1.5 — preview of 3.5e);
q rises (v grows) then falls (air thins faster than v² grows). Top of flight ≈ 105 km (as 3.5c).
Real-life: Falcon 9 / Shuttle Max Q ≈ 30–35 kPa around 11–13 km, ~1 min after launch; Shuttle throttled down to ~65–72% through it,
Falcon 9 throttles down near Max Q; launch commentary "Max Q"; structure designed for it.
Experiment: ve = 3000 (thrust 30000 N) → faster in thick air → Max Q much higher (rough guess ~100 kPa, ~2–3×, earlier & lower,
not hand-computed precisely) → why real rockets throttle down.
**User ran the experiment (ve = 1500.0 * 2) and shared the plot:** Max Q ≈ 84 kPa at t ≈ 30 s (≈ 2× the ~40 kPa baseline;
my "~100" guess was a bit high); engine off at 80 s at ≈ 90–100 km; apogee ≈ 780 km at ≈ 455 s. Explained: 2× ve → 2× Δv
(4828 vs 2414) but gravity loss stays 786 → burnout speed ~2.5× → coast height ∝ v² → ~7× higher apogee ("Isp is king").
Flagged: constant g = 9.82 is badly wrong at 780 km (real ≈ 7.7) → real apogee would be even higher; fixed when we use
inverse-square g (3.6). Told the user to set ve back to 1500.0 (their line 15 still has `1500.0  * 2`; comment says 15000 N).
User still hasn't sent the baseline (ve = 1500) Max Q line.
User: "next" → **3.5d done.** Plan re-split again: 3.5e Mach only; 3.5f Cd(Mach); 3.5g thrust vs altitude; 3.5h real numbers.

**3.5e:** `atmosphere.py` gained `GAMMA = 1.4` and `speed_of_sound(T) = sqrt(GAMMA*R*T/M)` (15 C → 340.3 m/s; −56.5 C → 295.1).
File `step3_rocket/step3_5e_mach.py` = 3.5d flight (ve = 1500) + `a_sound = speed_of_sound(T)`, `mach = v / a_sound`, list
`machs`; NEW Python `break` (find first slice with Mach ≥ 1); `from atmosphere import us_standard_atmosphere, speed_of_sound`;
plot Mach vs time with `axhline(1.0)` + `axvline(burn_time)`. Name `a_sound` (not `a`, which is acceleration).
Hand estimate (ROUGH): Mach 1 at t ≈ 41 s, h ≈ 6 km, v ≈ 317 m/s; Max Q at ≈ 53 s, Mach ≈ 1.5; top Mach ≈ 4.1 at burnout
(1238 m/s, a ≈ 302 at 31 km); after burnout Mach falls (slower + warmer air at ~47 km → a ≈ 330).
Experiment: `a_sound = 340.0` (sea-level value everywhere) → Mach 1 a bit later (~43 s) and top Mach ≈ 3.6 instead of 4.1 →
lesson: Mach must use the LOCAL temperature.
Real life: "vehicle is supersonic" call ~shortly before Max Q in webcasts; transonic buffeting; drone link: propeller TIP
speed kept below ~Mach 0.7 (noise/efficiency).
**User ran 3.5e and shared the Mach plot** (asked "explain in simple words"): Mach 1 at ≈ 42 s, peak ≈ 4.1 at 80 s (engine off),
fast drop to ≈ 3.2 by ≈ 97 s, kink, slower drop to ≈ 2.3 at ≈ 140 s, then a straight line to 0 at ≈ 204 s (apogee; plot stops
there because the loop stops at v = 0); crosses Mach 1 again at ≈ 176 s while still coasting UP. Matches estimates (41 s, 4.1, ~203 s).
Explained the kinks = the air layers of 3.5b: 31→50 km stratosphere warms (a 302→330) + rocket slows → fast drop;
~47–51 km warm isothermal layer → kink; 51→85 km mesosphere cools (a falls) → partly cancels the slowdown → gentler slope;
>~85 km constant T (a ≈ 274) and no drag → v falls 9.82 m/s each second → straight line; Mach 1 at 176 s = 274/9.82 ≈ 28 s before top.
User: "understood, next" → **3.5e done.**

**3.5f file `step3_rocket/step3_5f_cd_mach.py`:** 3.5e flight + drag curve table (typical slender rocket, told the user real ones
come from wind tunnel/CFD): MACH_TABLE = [0, .6, .8, .9, 1, 1.1, 1.2, 1.5, 2, 3, 5], CD_TABLE = [.30, .30, .32, .38, .50, .55, .54,
.48, .40, .32, .25]; NEW `np.interp(mach, MACH_TABLE, CD_TABLE)` (straight line between points; clamps beyond the ends);
`import numpy as np`; lists ts, qs, machs, cds; prints Max Q (with Mach and Cd) and top of flight; plots drag curve ("o-")
and Cd vs time.
Hand estimate (ROUGH): Cd 0.30 until ~Mach 0.6 (~28 s) → bump to 0.55 at Mach 1.1 (~45 s) → 0.48 near Max Q (Mach 1.5) →
~0.27 at burnout (Mach 4.1) → in the coast Cd follows Mach back down (0.32 at Mach 3 … 0.5 at Mach 1, 0.30 subsonic near the top).
Overall less drag than constant 0.5 → apogee higher than 3.5c/3.5e: roughly 110–120 km; Max Q ≈ 40–43 kPa, Cd ≈ 0.48.
Experiment: replace the `np.interp` line in BOTH loops with `Cd = 0.5` → exactly the 3.5e/3.5c numbers (top at ≈ 204 s)
→ shows how much the real drag curve matters.
Real life: RocketPy takes power-off/power-on drag curves (Cd vs Mach CSV); OpenRocket/DATCOM/CFD/wind tunnels produce them;
transonic drag rise ("sound barrier").
User asked "so Cd is max at Mach 1?" → almost: peak is just ABOVE Mach 1 (~1.05–1.2; ours 1.1); rise starts ~Mach 0.8
(critical Mach: air speeds up over the nose shoulder and goes locally supersonic → small shocks before the rocket hits Mach 1);
peak when the bow shock forms in front (flat-ish, strong); after that the shock cone sweeps back (angle: sin μ = 1/M → Mach 2: 30°,
Mach 4: 14.5°) → weaker → Cd falls. Also: Cd max ≠ drag-force max (force = q·Cd·A; ours ≈ 19.8 kPa·m²/m² at Mach 1.1 vs ≈ 19.2
at Max Q → drag force is near its biggest from ~Mach 1.1 to ~1.5). Sharper/longer nose → smaller peak.
**User did NOT understand that (too much: critical Mach, shoulder, cone angles, q×Cd).** Re-explained with ONE analogy only:
sound = the air's "warning message"; slower than sound → warning arrives first → air steps aside (like people in a corridor
seeing you coming) → Cd small; AT the speed of sound → you arrive together with the warning → air can't move → piles up in a
wall in front → Cd biggest; much faster → the pile becomes a pointy cone you slice through → Cd falls. Peak ≈ "around Mach 1"
(a bit after). Lesson: keep "why" answers to ONE analogy + 3-row table; no extra side facts.
User: "done next" → **3.5f done** (no numbers reported).

**3.5g file `step3_rocket/step3_5g_thrust_altitude.py`:** 3.5f flight; engine now described like a data sheet:
`ve_vac = 1656.0`, `thrust_vac = mdot*ve_vac = 16560 N`, `exit_radius = 0.07` → `Ae = 0.01539 m²`;
NEW `thrust = thrust_vac - P * Ae` (P from atmosphere — first use of P). Chosen so sea-level thrust = 16560 − 101325·0.015394
= 15000 N (same liftoff as before). Isp: sea level 153 s, vacuum 169 s. Lists ts, thrusts (kN); prints thrust at liftoff
(15.0 kN), at engine off (≈ 16.54 kN; P ≈ 1000 Pa at ~31–33 km), burnout line, top of flight; plot thrust vs time (rises
quickly 15 → ~16.5 kN by ~60 s, then flat).
Hand estimate (ROUGH): extra thrust gives ≈ +150 m/s at burnout vs 3.5f, apogee roughly +15–25 km vs the user's 3.5f result.
Experiment: `exit_radius = 0.10` (Ae 0.0314, keep thrust_vac) → liftoff thrust 13.38 kN (−1.6 kN), engine-off ≈ 16.53 kN
→ lower apogee → lesson: big nozzles lose thrust at sea level (Merlin 1D 282 s SL/311 s vac vs MVac huge nozzle on 2nd stage;
Raptor vs RVac). Note told: real bigger nozzle also raises vacuum thrust; we keep it fixed to isolate the
penalty. DON'T suggest nozzles so big that thrust < weight at liftoff: no ground in code → h < 0 → `us_standard_atmosphere`
finds no layer → UnboundLocalError.
User selected `radius = 0.25` / `A = math.pi * radius**2` in 3.5g: "I did not understand this sub-step" → likely confused by
TWO areas now. Explained: A = front circle of the rocket BODY (50 cm wide, 0.196 m²) → used ONLY in drag (air hits the front);
Ae = nozzle opening at the back (14 cm wide, 0.0154 m², ~13× smaller) → used ONLY in thrust (air pushes on the opening);
circle area = π·r² (r = half the width), with worked numbers; side-view + front/back-view ASCII diagram.
User pasted the 3.5g "big idea" (nozzle push-back diagram + straw-under-water analogy + table): "did not understand".
Re-explained with the CORRECT simple physics (no straw analogy): air presses on every surface (~10 t per m² at sea level);
top/nose pushed DOWN, bottom pushed UP → normally cancel; but the bottom has a HOLE (nozzle opening) where air has nothing
to push on → bottom gets less upward push → net leftover push DOWN = P × Ae. Tiny numbers: 10 squares on top, 9 squares +
1 hole on the bottom, 1 N per square → 10 down, 9 up → 1 N lost. In space P = 0 → nothing lost. Sea level: 101,325 × 0.0154
= 1560 N lost (engine 16,560 → 15,000).
User: "no I did not understand this" (2nd failure). 3rd attempt: dropped pressure physics entirely → "accept the rule" +
one everyday analogy (running out of a door into an empty street vs a crowded street; the crowd pushes back at the door;
wider door = more people pushing) + the 2 numbers (15.0 kN ground, 16.56 kN space, ~10%) + "run it and watch the thrust plot
rise". Told them it's a small (~10%) correction and fine to accept for now. If still unclear: ASK which word/idea blocks them.
User: "next" → **3.5g done.**
**User later ran 3.5g and pasted the output (2026-11-19):** liftoff 15.0 kN; engine off 16.55 kN; burnout t = 80 s, 34.8 km, 1482 m/s;
top 145.1 km at 230 s. Checked: no-air coast 34.8 + 1482²/(2·9.82) = 146.6 km, 231 s → coast drag cost only ~1.5 km. My rough guess
(~125–145 km) was at the low side. The output also showed matplotlib loaded from `/home/shivraj/venv-ardupilot/...` while the prompt
showed `(rocket)` → environments mixed (see §8 #7). Asked the user to run `which python` (and `deactivate` if it's the venv).

**3.5h file `step3_rocket/step3_5h_real_rocket.py`:** same physics as 3.5g, only NUMBERS change — Falcon 9 FT-like
(approximate public data): m0 = 549,000 kg; fuel 395,700 kg; dry_mass = m0 − fuel = 153,300 (empty S1 + full S2 + payload);
9 × Merlin 1D: thrust_vac_1 = 914 kN, isp_vac = 311 s → ve_vac = 3050 m/s, Ae_1 = 0.681 m² (from 914 vs 845 kN SL);
mdot = 8,226,000/3050 ≈ 2697 kg/s; radius 1.85 m → A ≈ 10.75 m²; same drag table. Prints before flight:
liftoff thrust 7605 kN (= 9 × 845 ✓), T/W 1.41; burn rate 2697 kg/s, burn time 146.7 s (real ≈ 162 s: throttling);
mass per front area: toy 5093 vs F9 51,060 kg/m² (10×). Then Max Q, burnout, top; plots height and q.
Hand estimate (ROUGH): Max Q ≈ 33 kPa at ≈ 60 s, ≈ 10.5 km, Mach ≈ 1.4 (real F9 ≈ 30–35 kPa ~ 70 s ~ 12 km ✓);
losses: gravity ≈ 1441 m/s (!), sea-level thrust ≈ 60 m/s, drag only ≈ 35 m/s; vacuum Δv 3891 → burnout ≈ 2350 m/s at ≈ 111 km
(t = 147 s); top ≈ 390 km at ≈ 385 s (constant g → real would be higher).
Lesson: big rocket = 10× more mass per area → drag barely matters; GRAVITY is the big enemy, and straight up gives no
sideways speed (orbit needs 7.7 km/s sideways) → real rockets tilt over → motivates 3.6 gravity turn.
Experiment: `Cd = 0` (both loops) → top only ≈ +10 km (toy rocket: +70 km).
User: "I am not able to understand isp_vac" → explained: name = Isp + vac; Isp = engine's fuel-efficiency score (like car km/L
or drone minutes per battery); it is just ve in another unit (ve = Isp × 9.81; toy 1500 ↔ 153 s; F9 3050 ↔ 311 s); why
"seconds": 1 kg of fuel can hold up 1 kg (9.81 N) for Isp seconds (3050/9.81 = 311); engineers use it because it's the same
number in metric and imperial units; "vac" = measured in space (Merlin 311 vac vs 282 sea level, 3.5g rule); in the code it
only feeds ve_vac → mdot. Table: ours 153, Merlin 1D 282/311, Raptor ~330/~350+, hydrogen engines ~450.
User: "understood, next" → **3.5h done** (no numbers reported). 3.6 split into 3.6a/b/c (see table).

**3.6a file `step3_rocket/step3_6a_round_earth.py`:** F9 numbers as 3.5h (compacted); MU, RE; start (0, RE), v = 0
(no Earth rotation yet — Step 4.3); each slice: r, h = r − RE, speed, atmosphere, thrust − P·Ae, Cd(Mach), drag,
NEW `g = MU / r**2`; thrust along (x/r, y/r), gravity along (−x/r, −y/r); drag `-(drag/m)*vx/speed` only `if speed > 0`
(avoid ÷0 on the pad); phase 2 `while v_up > 0` with `v_up = (vx*x + vy*y)/r` (2.5b "away" speed). Prints engine-off,
top, gravity at the top; plot height vs time. Euler loop kept (solve_ivp from 3.7).
Hand estimate (ROUGH, relative to 3.5h): weaker g → gravity loss ≈ 1416 instead of 1441 → engine off ≈ 112 km, ≈ 2375 m/s;
top via energy (½v² − MU/r) ≈ 420–430 km (≈ +30 km vs 3.5h) at ≈ 405 s; g at top ≈ 8.6 m/s².
Experiment: `g = 9.82` in BOTH loops → reproduces the user's 3.5h numbers (regression test: new code = old code when
the new physics is switched off) — real-life verification practice.
User: "done next" → **3.6a done** (no numbers).

**3.6b file `step3_rocket/step3_6b_tilt.py`:** 3.6a + `tilt_start = 10.0`, `tilt_deg = 5.0`; NEW thrust direction:
`tilt = 0` if t < 10 else `math.radians(tilt_deg)`; up = (x/r, y/r); sideways/east = (y/r, −x/r) (⟂ to up, +x at the top);
`dir = cos(tilt)·up + sin(tilt)·side`; ax = (thrust/m)·dir_x − g·x/r. New Python: `math.radians`, `math.cos/sin`,
`str()` in the title. Prints at engine off: height, v_up = (vx·x+vy·y)/r, v_side = (vx·y − vy·x)/r, orbit speed √(MU/r);
top: height + downrange x. Plot: PATH (x km vs height km).
Hand estimate (ROUGH): engine off ≈ 111 km, up ≈ 2360, sideways ≈ 320 m/s (≈ sin5° × ~3700), orbit needs ≈ 7840;
top ≈ 415 km, downrange ≈ 95 km. Lesson: tilt splits thrust (cos = up part, sin = sideways part); sideways speed is what
orbit needs, but 320 ≪ 7840 → need much more tilt, but tilting too early/much in thick air is bad → gravity turn (3.6c).
Experiment: tilt_deg = 10 → sideways ≈ 640 m/s, top lower (≈ 400 km), downrange ≈ 190 km (rough).
Don't suggest big tilts like 45° with fixed angle (near-zero climb, ugly; not tested by hand).
User asked "what is the next step, what all is left?" → gave the remaining list (≈ 20 mini-steps; 29 done):
Step 3: 3.6b tilt (current, file given) → 3.6c gravity turn → 3.7 ascent with solve_ivp + events (first stage ends like a
real F9 MECO ≈ 70 km, ≈ 2 km/s; honest: one stage CAN'T reach orbit). PROPOSED Step 4 reorder (orbit first, then globe
details): 4.1 stage separation (2 objects) → 4.2 second-stage burn → payload in ORBIT → 4.3 3D → 4.4 launch site lat/long →
4.5 rotating Earth + launch time → 4.6 countdown. Step 5: 5.1 booster alone → 5.2 boostback → 5.3 entry burn/reentry →
5.4 landing burn (1D) → 5.5 G-FOLD guidance → 5.6 full return. Step 6: 6.1 save to file → 6.2 Cesium globe + site →
6.3 timeline playback → 6.4 plots → 6.5 Monte Carlo. Waiting for user to accept the reorder (or not) and run 3.6b.

---

## 7. Exact next steps

### Step 2.2 — Air drag on a falling ball (ONE new idea: drag)

Build `step2_reentry/step2_2_drag.py` as a copy of Step 1.2's 1D drop loop + drag:
- Drag force: `F_drag = ½ · ρ · v² · Cd · A`, opposing motion. Acceleration `a_drag = F_drag / m`.
- Suggested ball: a sphere, `Cd = 0.47`, pick simple `m` and radius (e.g. m = 1 kg, radius 0.1 m → A = π·0.1²).
- Keep it 1D, flat ground, constant `g = 9.82`. Consider **constant density 1.225 first**
  (one idea), and use `air_density(h)` only later or as the experiment.
- Show **terminal speed**: speed stops growing at `v_t = √(2·m·g / (ρ·Cd·A))`. Explain as
  "drag grows with v² until it equals weight".
- Sign care: drag must point **opposite to velocity** (use `-sign(v)` or `-v*abs(v)` — explain).
- Experiment: change the mass (heavier ball → higher terminal speed) — guess first.
- Compute expected outputs by hand before giving them.
- Explain `½ρv²` intuitively (the air you hit per second × how hard you hit it), Cd (shape), A (frontal area).

### Step 2.4 — Drag in the orbit

- Add drag to `dynamics()` from Step 1.8: `a_drag = -(½ρ|v|Cd A/m) · v_vector` (components again!).
- **⚠ Decision needed (see Known issues #1):** with our simple atmosphere, a 400 km orbit feels
  essentially zero drag (4.47e-21 kg/m³). Options:
  a) demonstrate decay with a **low orbit** (e.g. ~150–200 km) and say honestly the model is rough there;
  b) upgrade `air_density` to a piecewise exponential table (different H per altitude band) — its own mini-step.
  Recommendation: (a) for now, keep it simple; offer (b) later as an upgrade.
- Introduce the **ballistic coefficient** `m / (Cd·A)` when useful.

### Step 2.5 — Deorbit burn

- Start in the 400 km circular orbit, apply a **retrograde Δv** (slow down by ~100–150 m/s) instantly.
- Show (with plot) that the new orbit's lowest point (perigee) dips into the atmosphere (~50–80 km),
  where the simple density model is reasonable.
- Likely needs `solve_ivp` **events** (`terminal=True`) to stop at the ground — introduce as one idea.

### Step 2.6 — Reentry to landing

- Capsule-like parameters (mass, Cd, area). Plots: altitude vs time, speed vs altitude,
  deceleration in g's (peak g-load). Possibly a parachute (bigger Cd·A below some altitude).
- Write `step2_reentry/README.md` summarizing Step 2 (same style as Step 1's README).

### After Step 2

Big Step 3: replace the ball with a rocket — mass that decreases as fuel burns, thrust,
rocket equation; then Steps 4–6 per the roadmap. Keep the same mini-step method.

---

## 8. Known issues / things to watch

1. **Atmosphere model is only good below ~80 km.** Single exponential with H = 8.5 km gives
   4.47e-21 kg/m³ at 400 km (real ≈ 1e-12, about a billion× more) and ~9.5e-6 at 100 km
   (real ≈ 5.6e-7, so ours is too high there). Fine for reentry; **blocks orbital decay at 400 km**.
   Already told to the user honestly.
2. **User edits to Step 1 files** (they experiment directly in the files; that's fine, don't revert):
   - `step1_orbit/step1_6_orbit.py`: `t_end = 1000000 * 60` (≈ 2 years). With dt = 0.1 that's
     ~600 million loop steps — effectively hangs. The user was warned (Ctrl+C; set back to `100 * 60`).
     The comment on that line still says "100 minutes". Unknown if they changed it back.
   - `step1_orbit/step1_5_fall_from_space.py`: `dt = 0.001` (slower, ~300k steps, still fine).
   - `step1_orbit/step1_7_draw.py`: has an extra commented line `# vx= 1000` (harmless).
   - `step1_orbit/step1_2_drop.py`: `dt = 0.01`.
3. **Expected outputs from 1.5 onward were computed by hand, never executed by the assistant**
   (per the no-commands rule). The user said "done" for each but reported actual numbers only for 1.1.
   Hand-calculated values most likely to differ slightly: 1.5 (300.3 s, 2719 m/s), 1.8 (`nfev`
   unknown, gap/energy approximate). If the user reports different numbers, check them.
4. The README in `step1_orbit/` says to run from inside the folder; scripts save PNGs relative to the
   current directory.
5. `.venv/` and `requirements.txt` in the project root may still exist (see §3).
6. **Semi-implicit Euler "wobble" in the hand-written orbit loops (1.6, 1.7, 2.4).** With dt = 0.1 the
   circular orbit becomes very slightly elliptical: altitude oscillates ±0.4 km once per lap (velocity is
   effectively half a step ahead → ~0.43 m/s inward radial velocity at start → e ≈ 6e-5). It is bounded,
   doesn't grow, and scales with dt (dt = 0.01 → ±0.04 km). The user saw it in 2.4 with `RHO0 = 0` and it
   was explained. Cure: solve_ivp (use it for reentry steps). The user's 2.4 file may still have
   `RHO0 = 0` and/or `dt = 0.01` — they were told to restore 1.225 and 0.1.
7. **Env mix-up (seen 2026-11-19):** running `python` with `(rocket)` active loaded matplotlib from
   `/home/shivraj/venv-ardupilot/lib/python3.12/site-packages` (warning "Unable to import Axes3D"). Either the ArduPilot
   venv is also active (fix: `deactivate`) or `PYTHONPATH` points into it. Waiting for the user's `which python` output.

---

## 9. Key constants & formulas (quick reference)

| Name | Value / formula |
|---|---|
| `MU` | 3.986004418e14 m³/s² (Earth GM) |
| `RE` | 6371e3 m |
| `RHO0` | 1.225 kg/m³ |
| `H` | 8500 m (scale height) |
| gravity | g = MU / r² (9.82 at surface, 8.69 at 400 km) |
| gravity components | ax = −g·x/r, ay = −g·y/r |
| circular orbit speed | √(MU/r) = 7673 m/s at 400 km |
| escape speed | √(2MU/r) = 10,851 m/s at 400 km |
| period | 2πr / v = 92.41 min at 400 km |
| specific energy | E = ½v² − MU/r (constant without drag/thrust) |
| air density | ρ = RHO0 · e^(−h/H) |
| drag (next) | F = ½ ρ v² Cd A, opposite to velocity |
