import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from . import cv_varactor as cv, mosfet as mo

OUT = Path(__file__).resolve().parents[1] / "results"


def plot_cv(v, c_pF, area=cv.DEFAULT_AREA_CM2):
    OUT.mkdir(exist_ok=True)
    r = cv.analyse(v, c_pF, area)
    fig, ax = plt.subplots(1, 3, figsize=(14, 4))
    ax[0].plot(v, c_pF, "o-", ms=3); ax[0].set(xlabel="Reverse bias V (V)", ylabel="C (pF)", title="C-V")
    ax[1].plot(v, cv.inv_c2(c_pF) / 1e21, "o", ms=3, label="1/C$^2$ (x1e21)")
    ax[1].plot(v, 1 / (c_pF * 1e-12) ** 3 / 1e32, "s", ms=3, label="1/C$^3$ (x1e32)")
    ax[1].set(xlabel="V (V)", title=f"R$^2$(1/C$^2$)={r.r2_inv_c2:.3f}  R$^2$(1/C$^3$)={r.r2_inv_c3:.5f}"); ax[1].legend()
    w, n = cv.profile(v, c_pF, area)
    ax[2].semilogy(w[1:-1], n[1:-1]); ax[2].set(xlabel="W (um)", ylabel="N (cm$^{-3}$)", title="Apparent doping profile")
    fig.tight_layout(); p = OUT / "cv_varactor.png"; fig.savefig(p, dpi=130); plt.close(fig)
    return p


def plot_mosfet():
    OUT.mkdir(exist_ok=True)
    vg, i1, ok = mo.load_transfer(); vd, i2, ok2 = mo.load_output()
    vt, k, _, _ = mo.fit_square_law(vg, i1, ok); _, _, lam = mo.output_resistance(vd, i2, ok2)
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    x = np.linspace(0, 2.4, 100)
    ax[0].semilogy(vg[i1 > 0], i1[i1 > 0], "o", label="measured"); ax[0].semilogy(x[x > vt], mo.model(x[x > vt], 1.8, vt, k), "-", label=f"model V_T={vt:.2f} V")
    ax[0].set(xlabel="V_GS (V)", ylabel="I_D (mA)", title="Transfer, V_DS=1.8 V"); ax[0].legend()
    y = np.linspace(0, 1.8, 100)
    ax[1].plot(vd[ok2], i2[ok2], "o", label="measured"); ax[1].plot(vd[~ok2], i2[~ok2], "rx", label="flagged")
    ax[1].plot(y, mo.model(2.5, y, vt, k, lam), "-", label="model"); ax[1].set(xlabel="V_DS (V)", ylabel="I_D (mA)", title="Output, V_GS=2.5 V"); ax[1].legend()
    fig.tight_layout(); p = OUT / "mosfet.png"; fig.savefig(p, dpi=130); plt.close(fig)
    return p
