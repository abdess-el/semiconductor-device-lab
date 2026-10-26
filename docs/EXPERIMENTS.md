# Experiment guides
Run any of them with `python -m semilab run <id>`.

1. **cv** – Sweep reverse bias 0–10 V (0.2 V steps) on a 1S2638 varactor with the Agilent 4277 C-V meter and 16047A fixture
   (open/short compensation first). Theory: C = εA/W, W = [2ε(V_bi+V)/(qN)]^½; test 1/C² vs V (abrupt) and 1/C³ vs V (graded).
2. **four-probe** – ρ = 2πS·V/I (S = 1 mm), finite-size factor 1/B₀; ρ₃₀₀ = ρ_T[1 − C_T(T−300)]; n = 1/(qμρ).
3. **probe-station** – ordered 9-step procedure; `probe_station.check_order` validates a learner's order.
4. **bjt** – read I_C at two I_B steps from the I_C–V_CE family; h_fe = ΔI_C/ΔI_B, h_FE = I_C/I_B.
5. **opamp** – V_IO = R₁V_O1/(R₁+R_F); I_IB = |V_O2−V_O1|/[2R(1+R_F/R₁)]; I_IO = R₁|V_O2−V_O1|/[(R₁+R_F)R]; A_vd = (1+R₂/R₁)V_o/V_s; f_H at 0.707.
6. **mosfet** – saturation √I_D = √K(V_GS−V_T); r_o = 1/(dI_D/dV_DS); digital levels V_OH/V_OL of the CMOS inverter.
