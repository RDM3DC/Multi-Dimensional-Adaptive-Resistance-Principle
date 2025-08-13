
import os, pandas as pd, numpy as np, matplotlib.pyplot as plt

def to_df(arr):
    t,v,iL,G,C,L = arr.T
    return pd.DataFrame({"t":t,"v":v,"iL":iL,"G":G,"C":C,"L":L})

def save_run(out_dir, name, arr, make_plots=True):
    os.makedirs(out_dir, exist_ok=True)
    df = to_df(arr)
    csv_path = os.path.join(out_dir, f"{name}.csv")
    df.to_csv(csv_path, index=False)

    if make_plots:
        # v(t)
        plt.figure(figsize=(8,3))
        plt.plot(df["t"], df["v"], label="v")
        plt.title("v(t)"); plt.xlabel("t"); plt.ylabel("v"); plt.legend(); plt.tight_layout()
        plt.savefig(os.path.join(out_dir, f"{name}_v.png")); plt.close()

        # iL(t)
        plt.figure(figsize=(8,3))
        plt.plot(df["t"], df["iL"], label="iL")
        plt.title("iL(t)"); plt.xlabel("t"); plt.ylabel("iL"); plt.legend(); plt.tight_layout()
        plt.savefig(os.path.join(out_dir, f"{name}_iL.png")); plt.close()

        # params
        plt.figure(figsize=(8,3.2))
        plt.plot(df["t"], df["G"], label="G")
        plt.plot(df["t"], df["C"], label="C")
        plt.plot(df["t"], df["L"], label="L")
        plt.title("Adaptive parameters"); plt.xlabel("t"); plt.ylabel("value"); plt.legend(); plt.tight_layout()
        plt.savefig(os.path.join(out_dir, f"{name}_params.png")); plt.close()
    return csv_path
