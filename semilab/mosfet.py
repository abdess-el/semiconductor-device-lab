"""Experiment 6 - DC input/output characteristics of a MOSFET (CD4069UB inverter used as NMOS)."""
from __future__ import annotations
import csv
from pathlib import Path
import numpy as np
from . import ui

D = Path(__file__).resolve().parents[1] / "data"
TITLE = "MOSFET DC characteristics (CD4069UB)"
OBJECTIVE = "Measure I_D-V_GS and I_D-V_DS; extract V_T, K, g_m, r_o"
PROCEDURE = [
    "Use one inverter of the CD4069UB: input A = gate, output = drain, V_SS = source/bulk; tie unused pins to V_SS.",
    "Build the test circuit (supply, R_W1, R_W2, voltmeters V1/V2, ammeter in the drain).",
    "Transfer curve: fix V_DS (R_W2), sweep V_GS (R_W1) from 0.2 V upwards, record I_D.",
    "Output curve: fix V_GS = 2.5 V, sweep V_DS from 0.2 V upwards, record I_D.",
    "Digital levels: measure V_OH (pins 2,4,6 to V_SS) and V_OL (pins 12,10,8 to V_SS).",
]


def _load(name, xcol):
    with open(D / name) as f:
        rows = list(csv.DictReader(f))
    return (np.array([float(r[xcol]) for r in rows]),
            np.array([float(r["id_mA"]) for r in rows]),
            np.array([int(r["valid"]) for r in rows], bool))


def load_transfer():
    return _load("mosfet_transfer.csv", "vgs_V")


def load_output():
    return _load("mosfet_output.csv", "vds_V")


def fit_square_law(vgs, id_mA, valid=None, i_min_mA=0.005):
    """Saturation: sqrt(I_D) = sqrt(K)(V_GS - V_T). Uses points with I_D >= i_min_mA.
    Returns V_T [V], K [mA/V^2], R^2, g_m at the largest V_GS [mA/V]."""
    m = (id_mA >= i_min_mA) if valid is None else (id_mA >= i_min_mA) & valid
    p = np.polyfit(vgs[m], np.sqrt(id_mA[m]), 1)
    fit = np.polyval(p, vgs[m])
    y = np.sqrt(id_mA[m])
    r2 = 1 - ((y - fit) ** 2).sum() / ((y - y.mean()) ** 2).sum()
    vt, k = -p[1] / p[0], p[0] ** 2
    return vt, k, r2, 2 * k * (vgs.max() - vt)


def output_resistance(vds, id_mA, valid, v_sat_min=0.8):
    """Slope of I_D vs V_DS in saturation -> g_ds [mA/V], r_o [kOhm], lambda [1/V]."""
    m = valid & (vds >= v_sat_min)
    slope, icept = np.polyfit(vds[m], id_mA[m], 1)
    return slope, 1.0 / slope, slope / icept


def model(vgs, vds, vt, k, lam=0.0):
    """Level-1 square-law model, I_D in mA (k in mA/V^2)."""
    vov = np.maximum(np.asarray(vgs, float) - vt, 0.0)
    vds = np.asarray(vds, float)
    tri = k * (2 * vov * vds - vds ** 2)
    sat = k * vov ** 2 * (1 + lam * vds)
    return np.where(vds < vov, tri * (1 + lam * vds), sat)


def predict_table(vgs_list, vds_list, vt, k, lam):
    """MODEL-PREDICTED I_D table (NOT measured) for the cells left empty in the report."""
    return {vds: [float(model(vg, vds, vt, k, lam)) for vg in vgs_list] for vds in vds_list}


def run(auto=False):
    ui.header(TITLE, OBJECTIVE)
    ui.steps("Procedure", PROCEDURE, auto)
    vg, idg, ok = load_transfer()
    vt, k, r2, gm = fit_square_law(vg, idg, ok)
    vd, ido, ok2 = load_output()
    gds, ro, lam = output_resistance(vd, ido, ok2)
    print(f"\nTransfer (V_DS=1.8 V): V_T = {vt:.2f} V, K = {k*1e3:.0f} uA/V^2, R^2 = {r2:.4f}, g_m(1.8V) = {gm:.2f} mA/V")
    print(f"Output (V_GS=2.5 V)  : g_ds = {gds*1e3:.0f} uS, r_o = {ro:.0f} kOhm, lambda = {lam:.3f} 1/V")
    print(f"Model I_Dsat(V_GS=2.5) = {float(model(2.5, 2.5, vt, k)):.3f} mA  (measured ~0.93 mA)")
    if (~ok2).any():
        print("Flagged point(s) excluded from the fit:", vd[~ok2], "-> repeat the measurement.")
    from .plots import plot_mosfet
    print("Figure saved:", plot_mosfet())
    return vt, k, ro
