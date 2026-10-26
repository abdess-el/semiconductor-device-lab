"""Figures written to results/."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from . import cv_varactor as cv
from . import mosfet as mo

OUT = Path(__file__).resolve().parents[1] / "results"


def plot_cv(v, c_pF, area=cv.DEFAULT_AREA_CM2):
    OUT.mkdir(exist_ok=True)
    r = cv.analyse(v, c_pF, area)
    c = c_pF * 1e-12
    fig, ax = plt.subplots(2, 2, figsize=(10, 7.5))

    ax[0, 0].plot(v, c_pF, "o-", ms=3)
    ax[0, 0].set(xlabel="Reverse bias (V)", ylabel="C (pF)", title="C-V characteristic")

    for a, y, scale, label, r2 in (
        (ax[0, 1], 1 / c**2, 1e21, r"$1/C^2$ ($10^{21}$ F$^{-2}$)", r.r2_inv_c2),
        (ax[1, 0], 1 / c**3, 1e32, r"$1/C^3$ ($10^{32}$ F$^{-3}$)", r.r2_inv_c3),
    ):
        a.plot(v, y / scale, "o", ms=3, label="data")
        a.plot(v, np.polyval(np.polyfit(v, y, 1), v) / scale, "-", label="linear fit")
        a.set(xlabel="Reverse bias (V)", ylabel=label, title=f"R$^2$ = {r2:.5f}")
        a.legend()

    w, n = cv.profile(v, c_pF, area)
    ax[1, 1].semilogy(w[1:-1], n[1:-1])
    ax[1, 1].set(xlabel="Depletion width (um)", ylabel=r"N (cm$^{-3}$)",
                 title=f"Apparent doping profile (A = {area:g} cm$^2$)")

    fig.tight_layout()
    path = OUT / "cv_varactor.png"
    fig.savefig(path, dpi=130)
    plt.close(fig)
    return path


def plot_mosfet():
    OUT.mkdir(exist_ok=True)
    vg, i_tr, ok_tr = mo.load_transfer()
    vd, i_out, ok_out = mo.load_output()
    vt, k, _, _ = mo.fit_square_law(vg, i_tr, ok_tr)
    _, _, lam = mo.output_resistance(vd, i_out, ok_out)

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    x = np.linspace(0, 2.4, 100)
    pos = i_tr > 0
    ax[0].semilogy(vg[pos], i_tr[pos], "o", label="measured")
    ax[0].semilogy(x[x > vt], mo.model(x[x > vt], 1.8, vt, k), "-", label=f"square-law fit, V_T = {vt:.2f} V")
    ax[0].set(xlabel="V_GS (V)", ylabel="I_D (mA)", title="Transfer characteristic, V_DS = 1.8 V")
    ax[0].legend()

    y = np.linspace(0, 1.8, 100)
    ax[1].plot(vd[ok_out], i_out[ok_out], "o", label="measured")
    ax[1].plot(vd[~ok_out], i_out[~ok_out], "rx", label="excluded")
    ax[1].plot(y, mo.model(2.5, y, vt, k, lam), "-", label="model")
    ax[1].set(xlabel="V_DS (V)", ylabel="I_D (mA)", title="Output characteristic, V_GS = 2.5 V")
    ax[1].legend()

    fig.tight_layout()
    path = OUT / "mosfet.png"
    fig.savefig(path, dpi=130)
    plt.close(fig)
    return path
