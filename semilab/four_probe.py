"""Experiment 2 - resistivity of a semiconductor by the four-probe method."""
from __future__ import annotations
import json
import math
from pathlib import Path
from . import ui

DATA = Path(__file__).resolve().parents[1] / "data" / "four_probe.json"
TITLE = "Four-probe resistivity"
OBJECTIVE = "Measure resistivity and its temperature dependence; refer to 300 K"
PROCEDURE = [
    "Plug the 220 V cable, power switch OFF, mode switch on 'short select', current switch on 'pop-up cut-off'.",
    "Connect the test stand to the main unit; loosen the column height wheel; clamp the sample (probe spacing 1 mm).",
    "Set the oven/sample temperature as required and record T.",
    "Power ON and pre-heat the instrument for 30 minutes.",
    "Polarity switch UP, state switch to 'measurement', choose current/voltage ranges, zero the voltmeter.",
    "Press the current switch -> constant current flows; read V (and I) directly.",
    "Repeat with reversed polarity; compute rho for both readings and average.",
    "Correct to 300 K:  rho_300 = rho_T [1 - C_T (T - 300)].",
]


def rho_from_VI(v, i, s_cm, b0=1.0):
    """rho = 2*pi*S*V/I (semi-infinite sample); divide by correction factor b0 for finite samples."""
    return 2 * math.pi * s_cm * v / i / b0


def rho_300(rho_T, T, CT):
    return rho_T * (1 - CT * (T - 300.0))


def _mu(n, kind):  # Caughey-Thomas mobility of Si at 300 K [cm^2/Vs]
    if kind == "n":
        return 68.5 + (1414 - 68.5) / (1 + (n / 9.2e16) ** 0.711)
    return 44.9 + (470.5 - 44.9) / (1 + (n / 2.23e17) ** 0.719)


def carrier_density(rho_ohm_cm, kind="n"):
    q, n = 1.602176634e-19, 1e15
    for _ in range(200):
        n = 1.0 / (q * _mu(n, kind) * rho_ohm_cm)
    return n


def run(auto=False):
    ui.header(TITLE, OBJECTIVE)
    ui.steps("Procedure", PROCEDURE, auto)
    d = json.loads(DATA.read_text())
    r1 = ui.ask_float("rho reading 1 (ohm.cm)", d["rho_readings_ohm_cm"][0], auto)
    r2 = ui.ask_float("rho reading 2 (ohm.cm)", d["rho_readings_ohm_cm"][1], auto)
    T = ui.ask_float("Temperature T (K)", d["temperature_K"], auto)
    ct = ui.ask_float("C_T (1/K), report: 0.84 %/K = 0.0084", d["CT_per_K"], auto)
    kind = ui.ask_str("Carrier type n/p", d["carrier_type"], auto)
    mean = (r1 + r2) / 2
    r300 = rho_300(mean, T, ct)
    print(f"\nmean rho_T = {mean:.3f} ohm.cm")
    print(f"rho_300    = {r300:.3f} ohm.cm")
    print(f"carrier density ({kind}-type Si) = {carrier_density(r300, kind):.2e} cm^-3")
    return r300
