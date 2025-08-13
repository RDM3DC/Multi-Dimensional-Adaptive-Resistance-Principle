
import argparse, os, numpy as np, pandas as pd
from md_arp.simulator import Params, simulate
from md_arp.io import save_run

def u_dc(t, A=1.0):
    return A

if __name__=="__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--T", type=float, default=2.0)
    ap.add_argument("--A", type=float, default=1.0)
    ap.add_argument("--out", type=str, default="out/dc_step")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    p = Params()
    from md_arp.simulator import current_input
    arr = simulate(T=args.T, params=p, controller=None, input_fn=u_dc, input_kwargs={"A":args.A})
    csv = save_run(args.out, "dc_step", arr, make_plots=True)
    print("Saved:", csv)
