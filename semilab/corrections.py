"""Original (as written in the report) vs corrected values - every corrected number is recomputed here."""
from . import cv_varactor as cv, four_probe as fp, bjt, opamp as op

def table():
    v, c = cv.load()
    i1_4 = float(cv.inv_c2([c[7]])[0])
    d = op
    mean = (11.33 + 11.48) / 2
    r300 = fp.rho_300(mean, 303, 0.0084)
    return [
        # experiment, quantity, as written, corrected, unit
        ("1 C-V", "1/C^2 at V=1.4 V", "9.7e21", f"{i1_4:.3g}", "F^-2"),
        ("1 C-V", "eps0 in the report", "8.854e-4", "8.854e-14", "F/cm"),
        ("2 4-probe", "mean rho (first line)", "11.905", f"{mean:.3f}", "ohm.cm"),
        ("2 4-probe", "rho_300 = rho[1-CT(T-300)]", "33.94128", f"{r300:.2f}", "ohm.cm"),
        ("2 4-probe", "carrier density (n-Si)", "6e14", f"{fp.carrier_density(r300,'n'):.2e}", "cm^-3"),
        ("4 BJT", "dI_B", "26-5 = 15", "20-5 = 15", "uA"),
        ("4 BJT", "h_fe = dIc/dIb", "120 mA", f"{bjt.hfe_ac(0.8,2.6,5,20):.0f}", "(no unit)"),
        ("5 Op-amp", "V_IO", "~3e-9 V", f"{d.v_io(0.33,100,1e5)*1e3:.3f}", "mV"),
        ("5 Op-amp", "I_IB (unit written V)", "3.746e-9 V", f"{d.i_ib(2.66,3.41,1e5,100,1e5)*1e9:.3f}", "nA"),
        ("5 Op-amp", "I_IO", "5.99e-7", f"{d.i_io(0.33,0.40,1e5,100,1e5)*1e9:.3f}", "nA"),
        ("6 MOSFET", "I_D at V_GS=1.2 V", "0.009 uA", "0.009 mA", "-"),
    ]
