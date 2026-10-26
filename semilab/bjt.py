"""Experiment 4 - DC parameters of a bipolar transistor with a curve tracer."""
from __future__ import annotations
import json
import math
from pathlib import Path
from . import ui

DATA = Path(__file__).resolve().parents[1] / "data" / "bjt_curve_tracer.json"
TITLE = "BJT curve tracer (JT-1 / XJ4810)"
OBJECTIVE = "Measure transistor DC current gain from the output characteristic family"
PROCEDURE = [
    "Power on and pre-heat for 5 minutes; adjust brightness, focus and auxiliary focus.",
    "Select NPN or PNP and set the spot (light-spot) zero position.",
    "Set test conditions (V_CE scale, I_B step, I_C scale) from the given table.",
    "Read two points of the I_C-V_CE family at the same V_CE using the grid scale.",
    "Compute h_fe; finally return 'peak voltage' to zero and power off.",
]


def ic_from_screen(div, mA_per_div):
    return div * mA_per_div


def hfe_ac(ic1_mA, ic2_mA, ib1_uA, ib2_uA):
    """Small-signal gain  h_fe = dI_C / dI_B  (dimensionless)."""
    return (ic2_mA - ic1_mA) * 1e-3 / ((ib2_uA - ib1_uA) * 1e-6)


def hfe_dc(ic_mA, ib_uA):
    """DC gain  h_FE = I_C / I_B."""
    return ic_mA * 1e-3 / (ib_uA * 1e-6)


def hfe_uncertainty(ic1, ic2, ib1, ib2, d_ic):
    d = math.sqrt(2) * d_ic / (ic2 - ic1)
    return hfe_ac(ic1, ic2, ib1, ib2) * d


def run(auto=False):
    ui.header(TITLE, OBJECTIVE)
    ui.steps("Procedure", PROCEDURE, auto)
    d = json.loads(DATA.read_text())
    sc = ui.ask_float("I_C scale (mA/div)", d["ic_scale_mA_per_div"], auto)
    n1 = ui.ask_float("I_C divisions, curve 1", d["ic_divisions"][0], auto)
    n2 = ui.ask_float("I_C divisions, curve 2", d["ic_divisions"][1], auto)
    ib1 = ui.ask_float("I_B1 (uA)", d["ib_uA"][0], auto)
    ib2 = ui.ask_float("I_B2 (uA)", d["ib_uA"][1], auto)
    ic1, ic2 = ic_from_screen(n1, sc), ic_from_screen(n2, sc)
    h = hfe_ac(ic1, ic2, ib1, ib2)
    u = hfe_uncertainty(ic1, ic2, ib1, ib2, d["reading_uncertainty_div"] * sc)
    print(f"\nI_C1 = {ic1:.2f} mA, I_C2 = {ic2:.2f} mA, dI_C = {ic2-ic1:.2f} mA, dI_B = {ib2-ib1:g} uA")
    print(f"h_fe (AC, dIc/dIb) = {h:.0f} +/- {u:.0f}   (dimensionless)")
    print(f"h_FE (DC, Ic/Ib)   = {hfe_dc(ic1, ib1):.0f} @point1, {hfe_dc(ic2, ib2):.0f} @point2")
    return h
