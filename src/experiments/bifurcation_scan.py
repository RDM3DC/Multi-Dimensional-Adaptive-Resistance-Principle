
import argparse, os, numpy as np, pandas as pd
from md_arp.simulator import Params, Caps, current_input
from md_arp.stability import settle_equilibrium, local_eigs

if __name__=="__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ratios", type=float, nargs="+", default=[0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0])
    ap.add_argument("--T", type=float, default=3.0)
    ap.add_argument("--out", type=str, default="out/bifurcation_scan")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    rows=[]
    caps = Caps()
    for r in args.ratios:
        muG,muC,muL = 0.5,0.1,0.1
        p = Params(aG=r*muG, mG=muG, aC=r*muC, mC=muC, aL=r*muL, mL=muL)
        y_star, arr = settle_equilibrium(y0=(0.0,0.0,0.2,1.0,1.0), params=p, caps=caps, input_fn=current_input, input_kwargs=None, T=args.T)
        evals = local_eigs(t=arr[-1,0], y=y_star[1:], params=p, caps=caps)  # y_star is [t,v,iL,G,C,L]? No: settle_equilibrium returns last row of arr -> [t,v,iL,G,C,L]
        # ensure we extracted correct slice
        lam = local_eigs(t=arr[-1,0], y=arr[-1,1:].copy(), params=p, caps=caps)
        max_real = float(np.max(np.real(lam)))
        rows.append(dict(ratio=r, max_real=max_real,
                         v=float(arr[-1,1]), iL=float(arr[-1,2]),
                         G=float(arr[-1,3]), C=float(arr[-1,4]), L=float(arr[-1,5])))
    df = pd.DataFrame(rows)
    csv = os.path.join(args.out, "bif_scan.csv")
    df.to_csv(csv, index=False)
    print(df)
