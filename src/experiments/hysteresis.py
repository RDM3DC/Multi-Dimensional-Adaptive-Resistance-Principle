
import argparse, os
from md_arp.simulator import Params, simulate, triangle_input
from md_arp.io import save_run

if __name__=="__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--T", type=float, default=4.0)
    ap.add_argument("--freq", type=float, default=0.25)
    ap.add_argument("--out", type=str, default="out/hysteresis")
    args = ap.parse_args()
    p = Params()
    arr = simulate(T=args.T, params=p, controller=None, input_fn=triangle_input, input_kwargs={"f":args.freq})
    csv = save_run(args.out, "hysteresis", arr, make_plots=True)
    print("Saved:", csv)
