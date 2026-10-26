"""Experiment 3 - manual probe station (qualitative, procedure-ordering exercise)."""
from __future__ import annotations
from . import ui

TITLE = "Manual probe station (ST-103A)"
OBJECTIVE = "Learn the probe-station procedure used for IC/wafer testing"
PROCEDURE = [
    "Turn on the probe lighting system.",
    "Raise all probes higher than (base height + chip height).",
    "Use the front/rear handles to level the base; place the chip; align it (left-right, front-back, rotation).",
    "Adjust microscope magnification until the chip is centred in the field of view.",
    "Move each probe above its pad and adjust the probe height.",
    "Connect probes to the instruments (oscilloscope, supply, generator) and check continuity with a multimeter.",
    "Slowly turn the lifting knob (left side) to raise the base; watch pad/needle contact in the microscope.",
    "Check/adjust needle contact (up/down) so every probe touches properly.",
    "Ground and shield first, then apply the supply and test signals.",
]
# Safety-critical ordering constraints: (earlier, later) using 1-based step numbers
CONSTRAINTS = [(1, 3), (2, 7), (5, 7), (6, 7), (7, 8), (8, 9)]


def check_order(order):
    """order = list of step numbers chosen by the learner. Returns list of violated constraints."""
    pos = {s: i for i, s in enumerate(order)}
    return [(a, b) for a, b in CONSTRAINTS if pos[a] > pos[b]]


def run(auto=False):
    ui.header(TITLE, OBJECTIVE)
    ui.steps("Procedure", PROCEDURE, auto)
    print("\nThe station lets you test many chip types; the relay armature drives the needle core to mark bad dice.")
    bad = check_order(list(range(1, len(PROCEDURE) + 1)))
    print("Reference order is valid." if not bad else f"Violations: {bad}")
    return bad
