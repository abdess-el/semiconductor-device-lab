# semiconductor-device-lab

An interactive, tested, GitHub-ready re-implementation of six microelectronics lab experiments
(Physics Teaching Experimental Center, Yangzhou University — Laboratory of Microelectronics Science and Engineering).
Anyone can clone the repo, **walk through each experiment step by step, enter (or reuse) the measurements, and get
verified results**. The original handwritten reports contained arithmetic, unit and interpretation errors; the
corrected values are recomputed by code and locked by unit tests. See [`docs/CORRECTIONS.md`](docs/CORRECTIONS.md).

| id | Experiment | Key result (corrected) |
|----|-----------|------------------------|
| `cv` | Varactor C-V (1S2638) | 1/C³ is linear (R²=0.99995) → **linearly graded junction**, γ≈0.32, V_bi≈0.75 V |
| `four-probe` | Four-probe resistivity | ρ₃₀₀ = **11.12 Ω·cm**, n ≈ 4.05×10¹⁴ cm⁻³ (n-Si) |
| `probe-station` | Manual probe station | procedure-order checker |
| `bjt` | Curve tracer, DC gain | h_fe = **120 ± 5** (dimensionless); h_FE(DC) = 160 / 130 |
| `opamp` | Op-amp V_IO, I_IB, I_IO | **0.330 mV, 3.746 nA, 0.699 nA** |
| `mosfet` | CD4069UB MOSFET | V_T ≈ 1.06 V, K ≈ 459 µA/V², r_o ≈ 28 kΩ |

## Quick start
```bash
git clone https://github.com/abdess-el/semiconductor-device-lab.git && cd semiconductor-device-lab
pip install -e ".[dev]"   # installs the `semilab` command
semilab run cv
```
Or without installing:
```bash
pip install -r requirements.txt
python -m semilab list
python -m semilab run cv            # interactive: Enter = next step; press Enter at prompts to keep the reference value
python -m semilab run all --auto    # non-interactive, uses the reference data
python -m semilab verify            # table: value as written in the report vs corrected value
pytest -q
```
Figures are written to `results/`. Experiment guides: [`docs/EXPERIMENTS.md`](docs/EXPERIMENTS.md).
Add your own data by editing the files in `data/` (CSV/JSON) or typing values at the prompts.

## Important assumptions (not stated in the source report)
* Varactor junction area is unknown → default `1e-4 cm²` placeholder. Shape results (γ, V_bi, junction type) do not
  depend on it; absolute doping/grade values do. Use the datasheet area.
* C_T "0.84" is read as 0.84 %/K = 0.0084 K⁻¹ (the literal value gives a negative resistivity).
* MOSFET "2.5 V" row is interpreted as the output curve at V_GS = 2.5 V (unit mA).
* Author: Abdessamad El Omary. The student ID from the cover pages is intentionally not included (public repo).
