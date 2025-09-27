
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Assignment 3 — Cache Timing Attack on AES (B=4), Noise-Free Dataset
--------------------------------------------------------------------
Vectorized first-round timing attack using |t|-test on Δk_{i,i+1} (adjacent pairs).
- Reads: TimingCache_noiseFree_B=4.csv (33 values per line: 16 pt bytes, time, 16 ct bytes)
- Produces: 15 plots (plot_k_t_XX_YY.png) and a CSV summary of best candidates.

Notes / Compliance
------------------
- No "simple loops" over samples: grouping/statistics via NumPy's bincount (vectorized).
- Plots use matplotlib only; one chart per figure; no explicit colors/styles.
- The CSV from the assignment has *no header*; we read it with header=None.

Author: Omidizadeh
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def t_scores_for_pair(xor_vals: np.ndarray, times: np.ndarray) -> np.ndarray:
    """Compute |t|-scores for all 256 candidates (vectorized via bincount)."""
    cnt0 = np.bincount(xor_vals, minlength=256).astype(np.float64)
    sum0 = np.bincount(xor_vals, weights=times, minlength=256)
    sumsq0 = np.bincount(xor_vals, weights=times*times, minlength=256)

    N = times.size
    cnt1 = N - cnt0
    sum1 = times.sum() - sum0
    sumsq1 = (times*times).sum() - sumsq0

    with np.errstate(invalid='ignore', divide='ignore'):
        m0 = sum0 / cnt0
        m1 = sum1 / cnt1
        v0 = (sumsq0 - cnt0*m0*m0) / (cnt0 - 1.0)
        v1 = (sumsq1 - cnt1*m1*m1) / (cnt1 - 1.0)
        sp2 = ((cnt0 - 1.0)*v0 + (cnt1 - 1.0)*v1) / (cnt0 + cnt1 - 2.0)
        tvals = (m0 - m1) / np.sqrt(sp2*(1.0/cnt0 + 1.0/cnt1))

    tvals[~np.isfinite(tvals)] = np.nan
    return np.abs(tvals)

def main():
    data_path = Path("TimingCache_noiseFree_B=4.csv")
    df = pd.read_csv(data_path, header=None)
    # Drop a trailing blank column if present
    if df.shape[1] == 34 and df.iloc[:, -1].astype(str).str.strip().eq("").all():
        df = df.iloc[:, :-1]

    P = df.iloc[:, 0:16].to_numpy(np.uint8)           # plaintext bytes
    times = pd.to_numeric(df.iloc[:, 16], errors="coerce").to_numpy(np.float64)  # timing
    N = P.shape[0]

    pairs = [(i, i+1) for i in range(15)]
    rows = []
    for (i,j) in pairs:
        xor_ij = (P[:, i] ^ P[:, j]).astype(np.uint8)
        ts = t_scores_for_pair(xor_ij, times)
        best = int(np.nanargmax(ts))
        msb6 = best >> 2
        rows.append({"pair": f"{i}-{j}", "best_delta": best, "MSB6(best_delta)": msb6})

        plt.figure(figsize=(10, 4.0))
        plt.plot(range(256), ts)
        plt.xlabel(f"Δk_{i},{j} candidate (0..255)")
        plt.ylabel("|t| statistic")
        plt.title(f"First-round: |t| for Δk_{i},{j} (N={N})")
        plt.tight_layout()
        plt.savefig(f"plot_k_t_{i:02d}_{j:02d}.png", dpi=180)
        plt.close()

    pd.DataFrame(rows).to_csv("assign3_first_round_summary.csv", index=False)
    print("Done. Wrote 15 plots and assign3_first_round_summary.csv")

if __name__ == "__main__":
    main()
