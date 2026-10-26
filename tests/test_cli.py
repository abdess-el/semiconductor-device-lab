import pytest
from semilab import cli, ui


def test_list_and_verify(capsys):
    cli.main(["list"]); cli.main(["verify"])
    out = capsys.readouterr().out
    assert "cv" in out and "0.699" in out and "11.12" in out


def test_run_all_auto(capsys):
    cli.main(["run", "all", "--auto"])
    out = capsys.readouterr().out
    assert "linearly graded" in out and "I_IB = 3.746 nA" in out and "V_T = 1.06" in out


def test_interactive_default_is_enter(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda *_: "")
    assert ui.ask_float("x", 2.5, False) == 2.5
    monkeypatch.setattr("builtins.input", lambda *_: "7")
    assert ui.ask_float("x", 2.5, False) == 7.0
