"""Command-line interface: semilab list | run <experiment|all> [--auto] | verify."""
import argparse

from . import bjt, corrections, cv_varactor, four_probe, mosfet, opamp, probe_station

EXPERIMENTS = {
    "cv": cv_varactor,
    "four-probe": four_probe,
    "probe-station": probe_station,
    "bjt": bjt,
    "opamp": opamp,
    "mosfet": mosfet,
}


def build_parser():
    ap = argparse.ArgumentParser(prog="semilab", description="Semiconductor-device laboratory experiments")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list", help="list the available experiments")
    run = sub.add_parser("run", help="run an experiment")
    run.add_argument("exp", choices=[*EXPERIMENTS, "all"])
    run.add_argument("--auto", action="store_true", help="use the reference data without prompting")
    sub.add_parser("verify", help="compare values in the original reports with the recomputed ones")
    return ap


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.cmd == "list":
        for key, module in EXPERIMENTS.items():
            print(f"{key:14s} {module.TITLE}")
    elif args.cmd == "run":
        for key in EXPERIMENTS if args.exp == "all" else [args.exp]:
            EXPERIMENTS[key].run(args.auto)
    else:
        print(f"{'Exp':10s}{'Quantity':32s}{'As written':14s}{'Corrected':14s}Unit")
        for row in corrections.table():
            print(f"{row[0]:10s}{row[1]:32s}{row[2]:14s}{row[3]:14s}{row[4]}")


if __name__ == "__main__":
    main()
