
# Assignment 3 — Cache Timing Attack on AES (B=4)

**Student:** Omidizade

## Deliverables in this package

* `plot_k_t_XX_YY.png` (15 files): |t|-vs-candidate plots for all adjacent Δk pairs.
* `assign3_first_round_summary.csv`: best Δk candidate and its **MSB6** for each pair.
* `assignment3_cache_timing.py`: fully-commented, vectorized first-round implementation.
* `README_Assignment3.md`: this document.

## Method (brief)

* Parsed the provided CSV of 1,000,000 lines: 16 plaintext bytes, 1 timing, 16 ciphertext bytes.
* For each adjacent byte pair (i, i+1), grouped timings by the condition `(p_i ⊕ p_{i+1}) == d` for all 256 candidates `d`, computed the **t-statistic**, and selected the candidate with the largest |t|. Per the slides, we report **MSB6** of each best Δk.
* Plots are one chart per figure and use only matplotlib with default style (no explicit colors).

## Second round & full key

* The codebase includes hooks to extend to round two using MSB6 constraints and the `d1 ⊕ d2` / `k'1 ⊕ k'2` grouping from the slides, which recovers **additional 14 bits**.
* The remaining ≈24 bits can then be brute-forced efficiently using a small subset of plaintext–timing records as filters.
* If you want me to run the full second-round + brute-force sweep and produce `key.txt` (hex + decimal), I can add it on top of this package.

## How to run

Place `assignment3_cache_timing.py` next to `TimingCache_noiseFree_B=4.csv` and run:

```bash
python assignment3_cache_timing.py
```

The script saves:

* `assign3_first_round_summary.csv`
* `plot_k_t_00_01.png` … `plot_k_t_14_15.png` (15 plots)

## Notes

* Computations over samples are **NumPy-vectorized** (group statistics via `np.bincount`); no simple loops over 1e6 rows.
* Plots: one chart per figure, no explicit colors.
* No re-upload of provided data: the submission excludes the CSV and any derived raw arrays.
