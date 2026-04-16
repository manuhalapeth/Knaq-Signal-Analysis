"""
explore.py  |  Raw exploration of the IOV accelerometer log.

Everything printed is computed directly from the file on each run.
No value is assumed, pre-filled, or carried over from prior inspection.

Usage:
    python3 explore.py
"""

import datetime
import statistics
from pathlib import Path

FILE_PATH = Path(__file__).parent / "Raw_Data" / "iov.log_2025_10_26"


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def detect_header_lines(filepath):
    """
    Scan from the top until the first line that parses as four floats.
    That line index is the number of header lines to skip.
    No line count is assumed in advance.
    """
    with open(filepath, "r") as fh:
        for i, line in enumerate(fh):
            parts = line.strip().split(",")
            if len(parts) == 4:
                try:
                    [float(p) for p in parts]
                    return i
                except ValueError:
                    pass
    return 0


def count_lines(filepath):
    """Binary read for fast total line count."""
    with open(filepath, "rb") as fh:
        return sum(
            buf.count(b"\n")
            for buf in iter(lambda: fh.read(1 << 20), b"")
        )


def scan_file(filepath, header_lines, sample_every=500):
    """
    Single pass over the file.  Returns:
      valid        total rows that parsed as four floats
      corrupt      total rows that did not
      first_ts     timestamp of the first valid row
      last_ts      timestamp of the last valid row
      first_dts    inter-sample intervals from the first 2000 valid rows
                   (used to derive the actual sample rate)
      xs, ys, zs   sampled axis values (every sample_every-th valid row)
    """
    valid      = 0
    corrupt    = 0
    first_ts   = None
    last_ts    = None
    first_dts  = []
    prev_ts    = None
    xs, ys, zs = [], [], []

    with open(filepath, "r", buffering=1 << 23) as fh:
        for i, line in enumerate(fh):
            if i < header_lines:
                continue

            stripped = line.strip()
            if not stripped:
                corrupt += 1
                continue

            parts = stripped.split(",")
            if len(parts) != 4:
                corrupt += 1
                continue

            try:
                x, y, z, ts = (float(p) for p in parts)
            except ValueError:
                corrupt += 1
                continue

            valid += 1

            if first_ts is None:
                first_ts = ts
            last_ts = ts

            if valid <= 2000 and prev_ts is not None:
                first_dts.append(ts - prev_ts)
            prev_ts = ts

            if valid % sample_every == 0:
                xs.append(x)
                ys.append(y)
                zs.append(z)

    return {
        "valid":     valid,
        "corrupt":   corrupt,
        "first_ts":  first_ts,
        "last_ts":   last_ts,
        "first_dts": first_dts,
        "xs":        xs,
        "ys":        ys,
        "zs":        zs,
    }


def to_utc(ts):
    return datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc)


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def main():
    print(f"File : {FILE_PATH}")
    print(f"Size : {FILE_PATH.stat().st_size / 1e9:.3f} GB")
    print()

    print("Detecting header ...")
    header_lines = detect_header_lines(FILE_PATH)

    print("Counting lines ...")
    total_lines      = count_lines(FILE_PATH)
    non_header_lines = total_lines - header_lines

    print(f"Scanning data (sampling every 500 valid rows) ...")
    r = scan_file(FILE_PATH, header_lines)
    print()

    duration  = r["last_ts"] - r["first_ts"]
    eff_hz    = r["valid"] / duration

    median_dt    = statistics.median(r["first_dts"])
    derived_hz   = round(1.0 / median_dt)

    def _axis_stats(vals):
        return min(vals), max(vals), statistics.mean(vals)

    bar = "=" * 56
    print(bar)
    print("  FILE")
    print(bar)
    print(f"  {'Name':<28}: {FILE_PATH.name}")
    print(f"  {'Size':<28}: {FILE_PATH.stat().st_size / 1e9:.3f} GB")
    print(f"  {'Total lines':<28}: {total_lines:,}")
    print(f"  {'Header lines (detected)':<28}: {header_lines:,}")
    print(f"  {'Non-header lines':<28}: {non_header_lines:,}")
    print()
    print(bar)
    print("  DATA ROWS")
    print(bar)
    print(f"  {'Valid rows':<28}: {r['valid']:,}")
    print(f"  {'Corrupt rows':<28}: {r['corrupt']:,}")
    print(f"  {'Corruption rate':<28}: {r['corrupt'] / non_header_lines * 100:.5f}%")
    print()
    print(bar)
    print("  RECORDING WINDOW")
    print(bar)
    print(f"  {'Start (UTC)':<28}: {to_utc(r['first_ts'])}")
    print(f"  {'End (UTC)':<28}: {to_utc(r['last_ts'])}")
    print(f"  {'Duration':<28}: {duration / 3600:.4f} h  ({duration:,.2f} s)")
    print()
    print(bar)
    print("  SAMPLE RATE")
    print(bar)
    print(f"  {'Effective rate':<28}: {eff_hz:.3f} Hz")
    print(f"  {'Derived rate (first 2k rows)':<28}: {derived_hz} Hz")
    print(f"  {'Median interval (first 2k)':<28}: {median_dt * 1000:.4f} ms")
    print()
    print(bar)
    print(f"  AXIS STATISTICS  (sampled every 500 valid rows, n={len(r['xs']):,})")
    print(bar)
    print(f"  {'Axis':<8} {'Min':>9} {'Max':>9} {'Mean':>9}  (m/s2)")
    print(f"  {'':{'_'}<38}")
    for name, vals in [("acc_x", r["xs"]), ("acc_y", r["ys"]), ("acc_z", r["zs"])]:
        mn, mx, avg = _axis_stats(vals)
        print(f"  {name:<8} {mn:>9.3f} {mx:>9.3f} {avg:>9.3f}")
    print(bar)


if __name__ == "__main__":
    main()
