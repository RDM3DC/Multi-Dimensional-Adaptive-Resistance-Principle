
import argparse, os
from md_arp.simulator import Params, Caps, simulate, current_input
from md_arp.controller import MetaController, Targets, Gains
from md_arp.io import save_run

def run_demo(T=2.0, plot=True, out="out"):
    p0 = Params(aG=1.0,mG=0.5,aC=0.25,mC=0.1,aL=0.25,mL=0.1)
    ctrl = MetaController(p0, Targets(E_star=0.05), Gains(kE=0.8,kV=0.2))
    arr = simulate(T=T, params=p0, controller=ctrl, input_fn=current_input)
    path = save_run(out, "demo", arr, make_plots=plot)
    print("Saved:", path)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    d = sub.add_parser("demo")
    d.add_argument("--T", type=float, default=2.0)
    d.add_argument("--plot", action="store_true")
    d.add_argument("--out", type=str, default="out")
    args = ap.parse_args()
    if args.cmd=="demo":
        run_demo(T=args.T, plot=args.plot, out=args.out)
    else:
        ap.print_help()
