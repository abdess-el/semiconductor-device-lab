import math
import numpy as np
import pytest
from semilab import cv_varactor as cv, four_probe as fp, bjt, opamp as op, mosfet as mo, probe_station as ps


def test_cv_inverse_square_value_at_1p4V():
    v, c = cv.load()
    assert cv.inv_c2([c[7]])[0] == pytest.approx(9.9e21, rel=0.01)   # report wrote 9.7e21


def test_cv_junction_is_linearly_graded():
    v, c = cv.load()
    r = cv.analyse(v, c)
    assert r.r2_inv_c3 > 0.9999 and r.r2_inv_c3 > r.r2_inv_c2
    assert r.gamma == pytest.approx(1 / 3, abs=0.04)
    assert "linearly graded" in r.junction
    assert r.vbi_graded == pytest.approx(0.75, abs=0.1)
    assert r.nb_high > 1.5 * r.nb_low   # apparent N_B not constant -> not uniform


def test_four_probe_chain():
    mean = (11.33 + 11.48) / 2
    assert mean == pytest.approx(11.405)
    r300 = fp.rho_300(mean, 303, 0.0084)
    assert r300 == pytest.approx(11.12, abs=0.01)
    assert fp.carrier_density(r300, "n") == pytest.approx(4.05e14, rel=0.03)
    assert fp.rho_300(mean, 303, 0.89) < 0      # literal reading of the report is unphysical
    assert fp.rho_from_VI(1e-3, 1e-3, 0.1) == pytest.approx(2 * math.pi * 0.1)


def test_bjt_gain():
    assert bjt.hfe_ac(0.8, 2.6, 5, 20) == pytest.approx(120)
    assert bjt.hfe_dc(2.6, 20) == pytest.approx(130)
    assert bjt.hfe_dc(0.8, 5) == pytest.approx(160)
    assert 3 < bjt.hfe_uncertainty(0.8, 2.6, 5, 20, 0.05) < 8


def test_opamp_parameters():
    assert op.v_io(0.33, 100, 1e5) == pytest.approx(0.33e-3, rel=0.01)
    assert op.i_ib(2.66, 3.41, 1e5, 100, 1e5) == pytest.approx(3.746e-9, rel=1e-3)
    assert op.i_io(0.33, 0.40, 1e5, 100, 1e5) == pytest.approx(6.99e-10, rel=1e-2)
    assert op.i_io(0.33, 0.40, 1e5, 100, 1e5) < op.i_ib(2.66, 3.41, 1e5, 100, 1e5)
    assert op.avd(1.0, 0.001, 100, 1e5) == pytest.approx(1001e3)


def test_opamp_bandwidth():
    f = [1, 10, 100, 1e3]; v = [1.0, 1.0, 0.9, 0.5]
    assert 100 < op.bandwidth(f, v) < 1e3


def test_mosfet_extraction():
    vg, i, ok = mo.load_transfer()
    vt, k, r2, gm = mo.fit_square_law(vg, i, ok)
    assert vt == pytest.approx(1.06, abs=0.05)
    assert k == pytest.approx(0.459, rel=0.05)
    assert r2 > 0.99
    vd, io, ok2 = mo.load_output()
    assert not ok2[-1] and ok2[:-1].all()
    _, ro, lam = mo.output_resistance(vd, io, ok2)
    assert 15 < ro < 60 and 0 < lam < 0.1
    assert float(mo.model(2.5, 2.5, vt, k)) == pytest.approx(0.94, rel=0.06)


def test_probe_station_order():
    assert ps.check_order(list(range(1, 10))) == []
    assert (8, 9) in ps.check_order([1, 2, 3, 4, 5, 6, 7, 9, 8])
