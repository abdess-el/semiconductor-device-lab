# Corrections to the original lab reports

Status values: `fixed` means recomputed and covered by a test; `flagged` means it cannot be resolved without new measurements; `assumed` means the interpretation is stated explicitly.

## 1. Varactor C-V
| Item | In report | Correct | Status |
|---|---|---|---|
| 1/C² at 1.4 V (C = 10.05 pF) | 9.7×10²¹ | 9.90×10²¹ F⁻² (all other 50 rows agree within 1.5 %) | fixed |
| ε₀ | 8.854×10⁻⁴ | 8.854×10⁻¹⁴ F/cm | fixed |
| Eq. (7) | d(1/C²)/dV = +2/(A²qεN_B) with V as forward bias | positive only for reverse bias V_R; use V_R consistently | fixed |
| Objective 2 (N_B) | never computed; uniform doping assumed | 1/C² is **not** linear (R²=0.991); 1/C³ is (R²=0.99995) ⇒ linearly graded junction, γ=0.32≈1/3, V_bi≈0.75 V. Apparent N_B rises with depth (×1.8 from 0–2 V to 8–10 V) | fixed |
| Junction area | not given | placeholder 1×10⁻⁴ cm² (absolute N_B/grade scale with it) | assumed |
| Plot | y-axis without unit | C (pF) vs reverse bias (V); generated in `results/cv_varactor.png` | fixed |

## 2. Four-probe resistivity
| Item | In report | Correct | Status |
|---|---|---|---|
| Mean ρ | (11.33+11.48)/2 = 11.905 (later 11.405) | 11.405 Ω·cm | fixed |
| C_T | 0.84 and later 0.890 | single value 0.84 %/K = 0.0084 K⁻¹ | assumed |
| ρ₃₀₀ = ρ[1−C_T(T−300)] | 33.94128 Ω·cm (literal 0.89 gives −19.05, i.e. negative) | 11.405×(1−0.0084×3) = **11.12 Ω·cm** | fixed |
| Carrier density | 6×10¹⁴ cm⁻³ (no derivation) | 4.05×10¹⁴ cm⁻³ if n-type (1.22×10¹⁵ if p-type), Caughey-Thomas mobility | fixed/assumed (type not stated) |

## 3. Probe station
Qualitative. Procedure kept; safety ordering encoded (lift base only after probes are positioned/connected; ground before signals).

## 4. BJT curve tracer
| Item | In report | Correct | Status |
|---|---|---|---|
| ΔI_B | "26−5 = 15 µA" | 20−5 = 15 µA | fixed |
| h_fe | "120 mA" | 120 (dimensionless) ± 5 (±0.1 div reading error) | fixed |
| Symbol | h_FE used for ΔI_C/ΔI_B | ΔI_C/ΔI_B is the AC gain h_fe; DC gain h_FE = I_C/I_B = 160 (5 µA), 130 (20 µA) | fixed |
| Principle text | "I_C = f(I_CE/V_EC)", "V_EB step voltage" | I_C = f(V_CE) at fixed I_B; the step generator supplies base current steps | fixed |

## 5. Op-amp (R₁ = 100 Ω, R_F = R = 100 kΩ)
| Item | In report | Correct | Status |
|---|---|---|---|
| V_IO | ≈3×10⁻⁹ V (copied from I_IB line) | R₁V_O1/(R₁+R_F) = **0.330 mV** | fixed |
| I_IB | substituted R = 100 Ω, unit "V" | 0.75/(2·10⁵·1001) = **3.746 nA** | fixed |
| I_IO | 5.99×10⁻⁷ (R = 100 Ω used) | (100/100100)·(0.07/10⁵) = **0.699 nA** (smaller than I_IB, as expected) | fixed |
| V_O1 | 2.66 V for I_IB but 0.33 V for V_IO/I_IO | inconsistent; repeat with one set | flagged |
| A_vd, bandwidth | method only, no data | functions provided (`avd`, `bandwidth`) | n/a |

## 6. MOSFET (CD4069UB)
| Item | In report | Correct | Status |
|---|---|---|---|
| I_D at V_GS = 1.2 V | 0.009 µA (breaks monotonic trend) | 0.009 mA = 9 µA | fixed |
| Table layout | V_GS header over both curves | row V_DS = 1.8 V = transfer curve; row 2.5 V = output curve at V_GS = 2.5 V vs V_DS | assumed |
| I_D at V_DS=1.8 V (output) | 0.931 < 0.940 | saturation current cannot decrease; point excluded from fit | flagged |
| Rows V_DS = 0.2, 0.5 V | empty | not measured; use `mosfet.predict_table` (model-predicted, not data) | flagged |
| Parameters | none extracted | V_T = 1.06 V, K = 459 µA/V², g_m = 0.68 mA/V, r_o ≈ 19 kΩ | fixed |
| Procedure text | "V2 = V_GS" and "V2 = V_DS" mixed | V1 = V_DS, V2 = V_GS | fixed |
