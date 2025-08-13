
import argparse, numpy as np, pandas as pd, os
from md_arp.simulator import Params, simulate, current_input
from md_arp.io import save_run

def classify(df, G_max=10.0, C_max=10.0, L_max=10.0):
    near_cap = (df["G"].iloc[-1] > 0.95*G_max) or (df["C"].iloc[-1] > 0.95*C_max) or (df["L"].iloc[-1] > 0.95*L_max)
    if near_cap: return "runaway"
    w = slice(int(0.75*len(df)), len(df))
    stds = np.std(df[["G","C","L"]].iloc[w].values, axis=0)
    means = np.mean(df[["G","C","L"]].iloc[w].values+1e-6, axis=0)
    if (stds/means).max() < 0.02: return "convergent"
    return "limit_cycle"

def to_df(arr):
    import pandas as pd
    t,v,iL,G,C,L = arr.T
    return pd.DataFrame({"t":t,"v":v,"iL":iL,"G":G,"C":C,"L":L})

if __name__=="__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ratios", type=float, nargs="+", default=[0.5,1,2,3.5,5,7,8])
    ap.add_argument("--T", type=float, default=2.0)
    ap.add_argument("--out", type=str, default="out/phase_scan")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    rows=[]
    for r in args.ratios:
        muG,muC,muL = 0.5,0.1,0.1
        p = Params(aG=r*muG, mG=muG, aC=r*muC, mC=muC, aL=r*muL, mL=muL)
        arr = simulate(T=args.T, params=p, controller=None, input_fn=current_input)
        csv = save_run(args.out, f"ratio_{r}", arr, make_plots=False)
        df = to_df(arr)
        cls = classify(df)
        rows.append(dict(ratio=r, cls=cls, v_rms=float((df["v"]**2).mean()**0.5),
                         iL_rms=float((df["iL"]**2).mean()**0.5),
                         G_final=float(df["G"].iloc[-1]),
                         C_final=float(df["C"].iloc[-1]),
                         L_final=float(df["L"].iloc[-1])))
    tab = pd.DataFrame(rows)
    tab.to_csv(os.path.join(args.out, "summary.csv"), index=False)
    print(tab)
