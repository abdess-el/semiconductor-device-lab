"""Experiment 1 - high-frequency C-V characteristic of a varactor diode (1S2638)."""
from __future__ import annotations
import csv
from dataclasses import dataclass
from pathlib import Path
import numpy as np
from scipy.optimize import curve_fit
from .constants import Q, EPS0_F_PER_CM, EPS_R_SI
from . import ui

DATA = Path(__file__).resolve().parents[1] / "data" / "cv_varactor.csv"
# The junction area is not part of the source data. Replace this placeholder with the datasheet
# value to obtain absolute doping and grade figures; shape results do not depend on it.
DEFAULT_AREA_CM2 = 1.0e-4

TITLE = "Varactor diode C-V characteristic"
OBJECTIVE = "Study C-V / barrier capacitance and extract doping information"
PROCEDURE = [
    "Turn on the C-V meter and warm it up.",
    "Connect the test fixture (16047A).",
    "Set cable length to 0 m.",
    "Set DC bias to 0 V.",
    "Do the OPEN-circuit compensation.",
    "Do the SHORT-circuit compensation (shorting bar), then remove the bar.",
    "Insert the varactor (1S2638), cathode (black band) to the positive terminal.",
    "Sweep the reverse bias from 0 V to 10 V in 0.2 V steps.",
    "Record the capacitance at every voltage.",
]


def load(path=DATA):
    with open(path) as f:
        rows = list(csv.DictReader(f))
    return (np.array([float(r["v_V"]) for r in rows]),
            np.array([float(r["c_pF"]) for r in rows]))


def _lin(x, y):
    p = np.polyfit(x, y, 1)
    res = y - np.polyval(p, x)
    return p, 1 - (res @ res) / ((y - y.mean()) @ (y - y.mean()))


def inv_c2(c_pF):
    return 1.0 / (np.asarray(c_pF) * 1e-12) ** 2


def apparent_nb(v, c_pF, v_lo, v_hi, area_cm2=DEFAULT_AREA_CM2, eps_r=EPS_R_SI):
    """Uniform-doping estimate N_B = 2 / (A^2 q eps d(1/C^2)/dV) over a voltage window (cm^-3)."""
    m = (v >= v_lo) & (v <= v_hi)
    slope = np.polyfit(v[m], inv_c2(c_pF[m]), 1)[0]
    return 2.0 / (area_cm2 ** 2 * Q * eps_r * EPS0_F_PER_CM * slope)


def classify(gamma):
    if abs(gamma - 1 / 3) < 0.06:
        return "linearly graded junction (gamma ~ 1/3)"
    if abs(gamma - 0.5) < 0.06:
        return "abrupt junction (gamma ~ 1/2)"
    return "hyperabrupt (gamma > 0.56)" if gamma > 0.56 else "intermediate profile"


@dataclass
class CVResult:
    r2_inv_c2: float
    r2_inv_c3: float
    vbi_graded: float
    gamma: float
    vbi_fit: float
    c0_pF: float
    junction: str
    nb_low: float
    nb_high: float
    grade_cm4: float


def analyse(v, c_pF, area_cm2=DEFAULT_AREA_CM2, eps_r=EPS_R_SI) -> CVResult:
    c = c_pF * 1e-12
    p2, r2_2 = _lin(v, 1 / c ** 2)
    p3, r2_3 = _lin(v, 1 / c ** 3)
    f = lambda x, c0, vb, g: c0 * (1 + x / vb) ** (-g)
    (c0, vb, g), _ = curve_fit(f, v, c_pF, p0=[15, 0.7, 0.4])
    eps = eps_r * EPS0_F_PER_CM
    grade = 12.0 / (area_cm2 ** 3 * Q * eps ** 2 * p3[0])   # C^3 = A^3 q a eps^2 / (12 (Vbi+V))
    return CVResult(r2_2, r2_3, p3[1] / p3[0], g, vb, c0, classify(g),
                    apparent_nb(v, c_pF, 0, 2, area_cm2, eps_r),
                    apparent_nb(v, c_pF, 8, 10, area_cm2, eps_r), grade)


def profile(v, c_pF, area_cm2=DEFAULT_AREA_CM2, eps_r=EPS_R_SI):
    """Local doping profile N(W): W [um], N [cm^-3] (uniform-doping formula applied point-wise)."""
    eps = eps_r * EPS0_F_PER_CM
    w_um = eps * area_cm2 / (c_pF * 1e-12) * 1e4
    n = 2.0 / (area_cm2 ** 2 * Q * eps * np.gradient(inv_c2(c_pF), v))
    return w_um, n


def run(auto=False):
    ui.header(TITLE, OBJECTIVE)
    ui.steps("Procedure", PROCEDURE, auto)
    area = ui.ask_float("Junction area (cm^2)", DEFAULT_AREA_CM2, auto)
    path = ui.ask_str("CSV with columns v_V,c_pF", str(DATA), auto)
    v, c = load(path)
    r = analyse(v, c, area)
    print(f"\nC(0 V) = {c[0]} pF -> C(10 V) = {c[-1]} pF  (ratio {c[0]/c[-1]:.2f})")
    print(f"Linearity R^2: 1/C^2 vs V = {r.r2_inv_c2:.4f} | 1/C^3 vs V = {r.r2_inv_c3:.5f}")
    print(f"Power-law fit  C = C0 (1+V/Vbi)^-gamma : gamma = {r.gamma:.3f}, Vbi = {r.vbi_fit:.2f} V")
    print(f"Built-in potential from 1/C^3 line      : {r.vbi_graded:.2f} V")
    print(f"Conclusion: {r.junction}")
    print(f"Apparent N_B (uniform formula) 0-2 V : {r.nb_low:.2e} cm^-3")
    verdict = "not constant, so the doping is not uniform" if r.nb_high > 1.5 * r.nb_low else "roughly constant"
    print(f"Apparent N_B (uniform formula) 8-10 V: {r.nb_high:.2e} cm^-3  ({verdict})")
    print(f"Grade coefficient a = {r.grade_cm4:.2e} cm^-4   (depends on area A: a ~ A^-3)")
    from .plots import plot_cv
    print("Figure saved:", plot_cv(v, c, area))
    return r
