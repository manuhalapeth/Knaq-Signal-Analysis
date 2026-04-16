# Take Home Exercise: IOT Device Signal Analysis

This was a take-home exercise. The task was to analyze a raw 3-axis accelerometer log from an IoT device and extract meaningful signal from a pretty messy dataset: 52.66 million samples, 18 hours, 800 Hz, and no preprocessing. 

The write-up is in [`ManuHalapeth_Knaq_TakeHome.pdf`](./ManuHalapeth_Knaq_TakeHome.pdf). The report goes through every decision, what alternatives I considered, and what the tradeoffs were.

---

## Key Findings

**Data Quality**
- 6,479 corrupt rows identified and categorized (0.012% of dataset) — handled with explicit justification, not silently dropped
- 4.5% of timestamps were duplicated or out-of-order — root cause traced to firmware using a software polling loop instead of a hardware interrupt
- 44.5% clock jitter as a result; documented and accounted for throughout the analysis

**Signal Characterization**
- Recovered sensor orientation purely from the long-run axis means — no ground truth required
- Recovered gravity magnitude with **0.146% error**
- Z axis carries essentially zero gravity load → it is 100% dynamics, so it can feed an event detector directly with no compensation

**Anomaly Detection**
- Built a two-scale detector: fine-grained 1-second Z-score (5σ threshold) + coarse 60-second rolling MAD (4σ threshold)
- Used MAD instead of rolling std because outliers inflate std and mask adjacent anomalies — exactly the circular failure you want to avoid
- Detected **6,019 transient events** across the full 18-hour session; top 10 characterized with individual narratives
- Most interesting result: a **3g impact** occurred during the quietest hour of the session — any window-based intensity metric would have missed it entirely

---

## How to Run

### 1. Clone the repo

```bash
git clone https://github.com/manuhalapeth/Knaq.git
cd Knaq
```

### 2. Install dependencies

Python 3.9+ is required. Install everything with:

```bash
pip install numpy pandas scipy matplotlib reportlab
```

> **Note:** The notebooks use `pandas 2.x`. If you're on an older version some dtype handling may differ — upgrading is recommended.

### 3. Add the raw data

The raw data file is not included in the repo (1.3 GB). Place it inside:

```
Knaq/Raw_Data/
```

The loading pipeline auto-detects the header length, so the exact filename does not need to match — just point the path variable at the top of `Notebook_Part_1.ipynb` to your file.

### 4. Run the notebooks in order

Each notebook is self-contained but builds on the cleaned dataset produced by Part 1. Run them in sequence:

```bash
jupyter notebook Notebook_Part_1.ipynb   # Data loading & cleaning
jupyter notebook Notebook_Part_2.ipynb   # Exploratory analysis
jupyter notebook Notebook_Part_3.ipynb   # Anomaly detection
```

Or open all three at once:

```bash
jupyter notebook
```

All figures are saved automatically to the repo root as `.png` files when you run each notebook.

### 5. Reproduce the PDF (optional)

```bash
python3 build_pdf_new.py
```

This regenerates `ManuHalapeth_Knaq_TakeHome.pdf` using `reportlab`. All figures must exist in the root directory first (i.e. run the notebooks before this step).

### 6. Run the standalone exploration script (optional)

```bash
python3 explore.py
```

This was the first script written before any notebook work. It auto-detects the header, counts lines, scans for corrupt rows, and computes basic statistics and sample rate — no Jupyter kernel required. Useful for a quick sanity check on any new data file.

---

## Notebooks

### `Notebook_Part_1.ipynb` — Data Loading & Cleaning
- Load the raw log file (52.66M rows, 1.3 GB)
- Auto-detect header length and validate sample rate against spec
- Identify and categorize corrupt rows with explicit handling decisions
- Data quality summary: timing jitter, timestamp anomalies, out-of-range samples, per-axis box plots

### `Notebook_Part_2.ipynb` — Exploratory Analysis
- Time and frequency domain plots across all three axes
- Per-axis descriptive statistics (mean, std, kurtosis, skewness)
- Sensor orientation recovery via gravity decomposition
- Acceleration vector magnitude over the full session
- Stationary period detection (15 segments identified)
- Per-hour intensity trends and Z-axis spectrogram
- Findings documented in [`Exploratory_Analysis_Key_Observations.md`](./Exploratory_Analysis_Key_Observations.md)

### `Notebook_Part_3.ipynb` — Anomaly Detection
- Local outlier detection: two-scale Z-score (fine 5σ per-sample, coarse 4σ MAD per 60-second bin)
- Transient event detection across 52.66M samples — 6,019 events found
- Top 10 events characterized individually with narrative descriptions
- Cross-event comparison: cosine similarity matrix, composite anomaly scoring, population percentile context

---

## File Structure

```
Knaq/
├── Notebook_Part_1.ipynb                     # Data loading & cleaning
├── Notebook_Part_2.ipynb                     # Exploratory analysis
├── Notebook_Part_3.ipynb                     # Anomaly detection
├── explore.py                                # Standalone exploration script (pre-notebook)
├── build_pdf_new.py                          # Generates the PDF report via reportlab
├── ManuHalapeth_Knaq_TakeHome.pdf            # Compiled write-up
├── Exploratory_Analysis_Key_Observations.md  # 13 findings from Part 2
│
├── Raw_Data/                                 # Source data (not included — see How to Run)
│
└── figures/                                  # All output figures (saved to repo root)
    ├── fig_corrupt_row_types.png             # Part 1 — corrupt row category breakdown
    ├── fig_signal_overview.png               # Part 1 — first 30s of raw signal
    ├── fig_quality_summary.png               # Part 1 — sampling intervals and box plots
    ├── fig_time_domain.png                   # Part 2 — full 18-hour waveform
    ├── fig_frequency_domain.png              # Part 2 — FFT and Welch PSD
    ├── fig_distributions.png                 # Part 2 — per-axis histograms and CDFs
    ├── fig_orientation.png                   # Part 2 — gravity decomposition
    ├── fig_magnitude.png                     # Part 2 — vector magnitude over 18 hours
    ├── fig_stationary.png                    # Part 2 — stationary segments
    ├── fig_trends_activity.png               # Part 2 — per-hour intensity metrics
    ├── fig_trends_spectrogram.png            # Part 2 — Z-axis spectrogram (30-min clip)
    ├── fig_outliers.png                      # Part 3 — fine and coarse outlier annotations
    ├── fig_transients.png                    # Part 3 — energy timeline and event gallery
    ├── fig_task3_comparison.png              # Part 3 — cross-event similarity and anomaly scores
    ├── fig_event_anomalies.png               # Part 3 — event anomaly visualization
    └── fig_event_distributions.png           # Part 3 — event feature distributions
```

> Figures are saved at the repo root (not in a subfolder) — the structure above is for readability.

---

## Learnings

**On data trust before analysis.** The instinct is to jump straight into modeling, but the most important work here happened before a single plot was made: validating the sample rate, understanding *why* timestamps were duplicated (firmware polling loop, not data corruption), and making deliberate decisions about how to handle each corrupt row category. Skipping that step would have poisoned every downstream result.

**On detector design.** The two-scale approach (fine Z-score + coarse MAD) was driven by a specific failure mode: rolling standard deviation inflates when there are outliers, which then masks the anomalies right next to them. Choosing MAD wasn't a stylistic preference — it was the only choice that didn't have that circular failure. Designing a detector means thinking about how it fails, not just how it works.

**On the value of quiet periods.** The 3g impact event during the quietest hour was the result that surprised me most. Intensity-based windowing would have ranked that hour as low-priority and potentially skipped it. The lesson is that anomaly score and signal amplitude are different things, and conflating them is a real production risk in any monitoring system.

**On communication.** Every algorithmic decision in the notebooks has a written justification: what I considered, what I ruled out, and why. That discipline made the PDF write-up straightforward to produce because the reasoning was already captured inline. It also means anyone reading the notebooks can audit the choices and not just reproduce the outputs.

