import argparse
from . import cv_varactor, four_probe, probe_station, bjt, opamp, mosfet, corrections

EXPERIMENTS = {"cv": cv_varactor, "four-probe": four_probe, "probe-station": probe_station,
               "bjt": bjt, "opamp": opamp, "mosfet": mosfet}


def main(argv=None):
    ap = argparse.ArgumentParser(prog="semilab", description="Interactive semiconductor-device lab")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    r = sub.add_parser("run"); r.add_argument("exp", choices=[*EXPERIMENTS, "all"])
    r.add_argument("--auto", action="store_true", help="accept reference values, no prompts")
    sub.add_parser("verify")
    a = ap.parse_args(argv)
    if a.cmd == "list":
        for k, m in EXPERIMENTS.items():
            print(f"{k:14s} {m.TITLE}")
    elif a.cmd == "run":
        for k in (EXPERIMENTS if a.exp == "all" else [a.exp]):
            EXPERIMENTS[k].run(a.auto)
    else:
        print(f"{'Exp':10s}{'Quantity':32s}{'As written':14s}{'Corrected':14s}Unit")
        for row in corrections.table():
            print(f"{row[0]:10s}{row[1]:32s}{row[2]:14s}{row[3]:14s}{row[4]}")

if __name__ == "__main__":
    main()
