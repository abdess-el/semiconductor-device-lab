# Experiment formulas

Run any experiment with `semilab run <id>`.

## cv: varactor C-V (1S2638)

Reverse bias is swept from 0 V to 10 V in 0.2 V steps with a C-V meter and a 16047A test fixture, after open and short compensation.

C = εA/W, with W = [2ε(V_bi + V_R) / (qN)]^½ for uniform doping.

* Uniform (abrupt) junction: 1/C² is linear in V_R, with slope 2/(A²qεN).
* Linearly graded junction: 1/C³ is linear in V_R.
* The exponent γ in C = C₀(1 + V_R/V_bi)^(−γ) is about 1/2 for an abrupt junction and about 1/3 for a linearly graded one.

## four-probe: resistivity

* ρ = 2πS·V/I for a semi-infinite sample, with probe spacing S = 1 mm. Divide by the finite-size factor for thin or small samples.
* Temperature correction: ρ₃₀₀ = ρ_T [1 − C_T (T − 300)].
* Carrier density: n = 1/(qμρ), with the mobility μ(n) from the Caughey-Thomas expression for silicon at 300 K, solved by iteration.

## probe-station: manual probe station

A nine-step procedure. `probe_station.check_order` returns the ordering constraints that a given sequence of steps violates, for example raising the base before the probes are positioned and connected.

## bjt: curve tracer

* h_fe = ΔI_C / ΔI_B, read from two curves of the I_C-V_CE family at the same V_CE (small-signal gain, dimensionless).
* h_FE = I_C / I_B (DC gain).
* Uncertainty from the reading error in screen divisions.

## opamp: offset and bias parameters

With R₁, R_F and R as in the test circuit:

* V_IO = R₁ V_O1 / (R₁ + R_F)
* I_IB = |V_O2 − V_O1| / [2R(1 + R_F/R₁)]
* I_IO = R₁ |V_O2 − V_O1| / [(R₁ + R_F) R]
* A_vd = (1 + R₂/R₁) V_o / V_s
* Bandwidth: the frequency at which the output falls to 0.707 of its low-frequency value (linear interpolation).

## mosfet: CD4069UB used as an NMOS device

* Saturation: √I_D = √K (V_GS − V_T), fitted over points with I_D above a threshold current.
* Output resistance: r_o = 1 / (dI_D/dV_DS) in saturation.
* Digital levels V_OH and V_OL of the CMOS inverter.
