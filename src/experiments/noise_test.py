
import argparse, os, numpy as np
from md_arp.simulator import Params, simulate, current_input
from md_arp.io import save_run

def noisy_sine(t, A=1.0, f=1.0, bias=0.0, sigma=0.1):
    base = bias + A*np.sin(2*np.pi*f*t)
    return base + np.random.normal(0.0, sigma)

if __name__=="__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--T", type=float, default=2.0)
    ap.add_argument("--sigma", type=float, default=0.1)
    ap.add_argument("--out", type=str, default="out/noise")
    args = ap.parse_args()
    p = Params()
    arr = simulate(T=args.T, params=p, controller=None, input_fn=noisy_sine, input_kwargs={"sigma":args.sigma})
    csv = save_run(args.out, "noise", arr, make_plots=True)
    print("Saved:", csv)
