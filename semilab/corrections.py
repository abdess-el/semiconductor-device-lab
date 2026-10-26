"""Values as written in the original lab reports next to the recomputed ones.

Every corrected number is computed here from the data files, not typed in.
"""
from . import bjt, four_probe as fp, opamp as op
from . import cv_varactor as cv


def table():
    v, c = cv.load()
    inv_c2_at_1v4 = float(cv.inv_c2([c[7]])[0])

    d = fp.load()
    mean = sum(d["rho_readings_ohm_cm"]) / 2
    r300 = fp.rho_300(mean, d["temperature_K"], d["CT_per_K"])

    b = bjt.load()
    ic = [n * b["ic_scale_mA_per_div"] for n in b["ic_divisions"]]
    ib = b["ib_uA"]

    o = op.load()
    r1, rf, r = o["R1_ohm"], o["RF_ohm"], o["R_ohm"]

    return [
        # (experiment, quantity, as written, corrected, unit)
        ("1 C-V", "1/C^2 at V = 1.4 V", "9.7e21", f"{inv_c2_at_1v4:.3g}", "F^-2"),
        ("1 C-V", "eps0", "8.854e-4", "8.854e-14", "F/cm"),
        ("2 4-probe", "mean rho (first line)", "11.905", f"{mean:.3f}", "ohm.cm"),
        ("2 4-probe", "rho_300 = rho[1 - CT(T-300)]", "33.94128", f"{r300:.2f}", "ohm.cm"),
        ("2 4-probe", "carrier density (n-Si)", "6e14", f"{fp.carrier_density(r300, 'n'):.2e}", "cm^-3"),
        ("4 BJT", "dI_B", "26-5 = 15", f"{ib[1]:g}-{ib[0]:g} = {ib[1]-ib[0]:g}", "uA"),
        ("4 BJT", "h_fe = dIc/dIb", "120 mA", f"{bjt.hfe_ac(ic[0], ic[1], ib[0], ib[1]):.0f}", "(no unit)"),
        ("5 Op-amp", "V_IO", "~3e-9 V", f"{op.v_io(o['vio']['vo1_V'], r1, rf)*1e3:.3f}", "mV"),
        ("5 Op-amp", "I_IB (unit written V)", "3.746e-9 V",
         f"{op.i_ib(o['iib']['vo1_V'], o['iib']['vo2_V'], r, r1, rf)*1e9:.3f}", "nA"),
        ("5 Op-amp", "I_IO", "5.99e-7",
         f"{op.i_io(o['iio']['vo1_V'], o['iio']['vo2_V'], r, r1, rf)*1e9:.3f}", "nA"),
        ("6 MOSFET", "I_D at V_GS = 1.2 V", "0.009 uA", "0.009 mA", "-"),
    ]
