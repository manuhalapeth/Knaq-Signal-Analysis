# Take-Home Exercise — IOV Accelerometer Signal Analysis

This was a take-home exercise. The task was to analyze a raw 3-axis accelerometer log from an IoT device and extract meaningful signal from a pretty messy dataset.

The data was 800 Hz firmware output, 18 hours, 52 million samples, with no preprocessing. Before doing any analysis I had to actually trust the data, so I built a loading pipeline that auto-detects the header length, handles a pandas 2.x typing bug, and validates the sample rate against spec before touching anything else. About 4.5% of timestamps were either duplicated or out of order because the firmware was using a software polling loop instead of a hardware interrupt, which also caused 44.5% clock jitter. Those decisions all had to be documented and justified.

The signal characterization part is where it got interesting. I recovered the sensor orientation purely from the long term mean of each axis, with 0.146% error on the recovered gravity magnitude. The big finding there was that the Z axis carries basically zero gravity load, which means it is 100% dynamics and you can pipe it straight into an event detector with no compensation at all.

For anomaly detection I built a two scale detector: a fine 1 second window Z score for catching instantaneous spikes, and a coarse 60 second rolling MAD detector for sustained deviations. The reason for MAD instead of rolling standard deviation is that outliers inflate the std and mask adjacent anomalies, which is exactly the circular failure you want to avoid. The most interesting result was a 3g impact event that happened during the quietest hour of the entire 18 hour session. Any window based intensity metric would have missed it completely.

The report goes through every decision, what alternatives I considered, and what the tradeoffs were.

---

## File Structure

```
Knaq/
├── Notebook_Part_1.ipynb                     # Part 1: Data Loading & Cleaning
├── Notebook_Part_2.ipynb                     # Part 2: Exploratory Analysis
├── Notebook_Part_3.ipynb                     # Part 3: Anomaly Detection
├── explore.py                                # Standalone raw data exploration script
├── build_pdf_new.py                          # PDF generation script (reportlab) — run to reproduce the PDF
├── ManuHalapeth_Knaq_TakeHome.pdf            # Compiled write-up
├── Exploratory_Analysis_Key_Observations.md  # 13 documented findings from Part 2
│
├── Raw_Data/                                 # Source data (not included in submission)
│
├── fig_corrupt_row_types.png                 # Part 1 — corrupt row category breakdown
├── fig_signal_overview.png                   # Part 1 — first 30s of raw signal (3 axes)
├── fig_quality_summary.png                   # Part 1 — sampling intervals and per-axis box plots
├── fig_time_domain.png                       # Part 2 — full 18-hour waveform (X, Y, Z)
├── fig_frequency_domain.png                  # Part 2 — FFT power spectrum and Welch PSD
├── fig_distributions.png                     # Part 2 — per-axis histograms and CDFs
├── fig_orientation.png                       # Part 2 — gravity decomposition and mounting geometry
├── fig_magnitude.png                         # Part 2 — vector magnitude over 18 hours
├── fig_stationary.png                        # Part 2 — stationary segments and bin-std timeline
├── fig_trends_activity.png                   # Part 2 — per-hour intensity metrics
├── fig_trends_spectrogram.png                # Part 2 — Z-axis spectrogram (30-min clip)
├── fig_outliers.png                          # Part 3 — fine and coarse scale outlier annotations
├── fig_transients.png                        # Part 3 — energy timeline and 10-event gallery
├── fig_task3_comparison.png                  # Part 3 — cross-event similarity and anomaly scores
├── fig_event_anomalies.png                   # Part 3 — event anomaly visualization
└── fig_event_distributions.png               # Part 3 — event feature distributions
```

> All figures are saved at the root level alongside each notebook.

---

## Notebooks

### `Notebook_Part_1.ipynb` — Data Loading & Cleaning
- Load the raw log file (52.66M rows, 1.3 GB)
- Identify and categorize malformed/corrupt rows (6,479 rows, 0.012%)
- Handle corrupt rows with explicit justification
- Data quality summary: sample rate, timing jitter, timestamp anomalies, out-of-range samples

### `Notebook_Part_2.ipynb` — Exploratory Analysis
- Time and frequency domain plots across all three axes
- Per-axis descriptive statistics (mean, std, kurtosis, skewness)
- Sensor orientation via gravity decomposition
- Acceleration vector magnitude analysis over the full session
- Stationary period detection (15 segments identified)
- Trends and recurring spectral patterns
- Key observations documented in `Exploratory_Analysis_Key_Observations.md`

### `Notebook_Part_3.ipynb` — Anomaly Detection
- Local outlier detection: two-scale Z-score (fine 5σ per-sample, coarse 4σ MAD per bin)
- Transient event detection across 52.66M samples — 6,019 events found, 10 characterized with individual narratives
- Cross-event comparison: cosine similarity matrix, composite anomaly scoring, population percentile context

---

## Supporting Files

**`explore.py`** — Standalone script run prior to notebook development. Auto-detects header, counts lines, scans for corrupt rows, computes basic statistics and sample rate. No notebook kernel required.

**`build_pdf_new.py`** — Python script that generates `ManuHalapeth_Knaq_TakeHome.pdf` using the reportlab library. Run with `python3 build_pdf_new.py` to reproduce the PDF.

**`Exploratory_Analysis_Key_Observations.md`** — 13 findings from Part 2 covering sensor geometry, signal characteristics, firmware timing issues, stationary detection methodology, and operational insights.
