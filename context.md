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
| 2 | Make it fall back and land: air drag + deorbit burn → reentry | 🔄 **In progress** (at 2.1) |
| 3 | Replace the object with a rocket: mass, engine, thrust, fly up | ⏳ |
| 4 | Countdown (timer + checks) and stage separation (split into two objects) | ⏳ |
| 5 | Bring the booster back: boostback, descent, G-FOLD landing burn | ⏳ |
| 6 | Make it look good: 3D viewer, plots, Monte Carlo runs | ⏳ |

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
- Not a git repository (no version control yet — could suggest `git init` at a natural break).
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
| 2.6 | Reentry all the way to landing, with plots | ⏳ |

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
In a new session: ask for their numbers; on "next" start Step 2.6 (switch to solve_ivp + events,
reentry plots: speed vs altitude, deceleration in g's).

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
