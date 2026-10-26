"""Experiment 5 - input offset voltage / bias current / offset current of an op-amp."""
from __future__ import annotations
import json
from pathlib import Path
from . import ui

DATA = Path(__file__).resolve().parents[1] / "data" / "opamp.json"
TITLE = "Operational amplifier parameters"
OBJECTIVE = "Measure V_IO, I_IB, I_IO (and understand A_vd and bandwidth)"
PROCEDURE = [
    "A_vd: fix frequency, raise input amplitude to the largest undistorted output; A_vd = dVo/dVid.",
    "Bandwidth: hold input constant, raise frequency until Vo falls to 0.707 of its low-frequency value.",
    "V_IO: close S1 and S2, read V_O1;   V_IO = R1/(R1+RF) * V_O1.",
    "I_IB: open S1 and S2, read V_O2;    I_IB = |V_O2-V_O1| / (2 R (1+RF/R1)).",
    "I_IO: close S1, open S2 (or per manual), read V_O2; I_IO = R1/(R1+RF) * |V_O2-V_O1| / R.",
]


def avd(vo, vs, r1, r2):
    """A_vd = (R1+R2)/R1 * Vo/Vs   (report, circuit 1)."""
    return (r1 + r2) / r1 * vo / vs


def v_io(vo1, r1, rf):
    return r1 / (r1 + rf) * vo1


def i_ib(vo1, vo2, r, r1, rf):
    return abs(vo2 - vo1) / (2 * r * (1 + rf / r1))


def i_io(vo1, vo2, r, r1, rf):
    return r1 / (r1 + rf) * abs(vo2 - vo1) / r


def bandwidth(freqs, vout):
    """First frequency where vout <= 0.707*vout[0] (linear interpolation)."""
    target = 0.7071 * vout[0]
    for k in range(1, len(freqs)):
        if vout[k] <= target:
            f0, f1, v0, v1 = freqs[k - 1], freqs[k], vout[k - 1], vout[k]
            return f0 + (v0 - target) * (f1 - f0) / (v0 - v1)
    return None


def run(auto=False):
    ui.header(TITLE, OBJECTIVE)
    ui.steps("Procedure", PROCEDURE, auto)
    d = json.loads(DATA.read_text())
    r1 = ui.ask_float("R1 (ohm)", d["R1_ohm"], auto)
    rf = ui.ask_float("RF (ohm)", d["RF_ohm"], auto)
    r = ui.ask_float("R (ohm)  <-- 100 kOhm, NOT 100 Ohm", d["R_ohm"], auto)
    v1 = ui.ask_float("V_O1 for V_IO (V)", d["vio"]["vo1_V"], auto)
    a1 = ui.ask_float("V_O1 for I_IO (V)", d["iio"]["vo1_V"], auto)
    a2 = ui.ask_float("V_O2 for I_IO (V)", d["iio"]["vo2_V"], auto)
    b1 = ui.ask_float("V_O1 for I_IB (V)", d["iib"]["vo1_V"], auto)
    b2 = ui.ask_float("V_O2 for I_IB (V)", d["iib"]["vo2_V"], auto)
    print(f"\nV_IO = {v_io(v1, r1, rf)*1e3:.3f} mV")
    print(f"I_IB = {i_ib(b1, b2, r, r1, rf)*1e9:.3f} nA")
    print(f"I_IO = {i_io(a1, a2, r, r1, rf)*1e9:.3f} nA")
    if a1 != b1:
        print("WARNING: V_O1 differs between the I_IO and I_IB sets - repeat with one consistent measurement.")
    return v_io(v1, r1, rf), i_ib(b1, b2, r, r1, rf), i_io(a1, a2, r, r1, rf)
