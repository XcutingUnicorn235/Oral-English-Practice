#!/usr/bin/env python3
"""Plot speaking-progress trends from data.csv.

Usage:
    python trend.py <path-to-data.csv> [output_png]

Reads the CSV the oral-english-practice skill maintains and renders a trend
chart: the "native /100" distance-to-native line on top, and the seven 1-10
dimension scores below. Non-numeric cells (e.g. pronunciation=NA) are skipped
for that point.

If matplotlib isn't installed, exits with code 2 and prints a clear message so
the caller can fall back to a text/markdown summary instead of crashing.
"""
import csv
import os
import sys

DIMENSIONS = [
    "fluency", "lexis", "grammar", "pronunciation",
    "discourse", "interaction", "listening",
]


def load(csv_path):
    # utf-8-sig so a stray BOM on the header never corrupts the first column name
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        print("No sessions logged yet — data.csv is empty.")
        sys.exit(3)
    return rows


def to_float(val):
    try:
        return float(str(val).split("/")[0])
    except (ValueError, AttributeError):
        return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python trend.py <path-to-data.csv> [output_png]")
        sys.exit(1)
    csv_path = sys.argv[1]
    if not os.path.exists(csv_path):
        print(f"Not found: {csv_path}")
        sys.exit(1)

    rows = load(csv_path)

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed — fall back to a text/markdown trend "
              "summary instead. (pip install matplotlib to enable charts.)")
        sys.exit(2)

    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        os.path.dirname(os.path.abspath(csv_path)), "trend.png")

    # Prefer the explicit session column (schema v2); fall back to row order (v1).
    def session_of(i, r):
        s = to_float(r.get("session"))
        return int(s) if s is not None else i + 1
    x = [session_of(i, r) for i, r in enumerate(rows)]
    labels = [r.get("date", "") for r in rows]

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(10, 9), gridspec_kw={"height_ratios": [1, 2]})

    native = [to_float(r.get("native")) for r in rows]
    ax1.plot(x, native, marker="o", color="#1f77b4", linewidth=2)
    ax1.set_title("Distance to native (/100)")
    ax1.set_ylim(0, 100)
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(x)
    ax1.set_xticklabels([f"#{i}" for i in x])

    for dim in DIMENSIONS:
        ys = [to_float(r.get(dim)) for r in rows]
        xs = [xi for xi, y in zip(x, ys) if y is not None]
        yv = [y for y in ys if y is not None]
        if xs:
            ax2.plot(xs, yv, marker="o", linewidth=1.6, label=dim)
    ax2.set_title("Dimension scores (1-10)")
    ax2.set_ylim(0, 10)
    ax2.grid(True, alpha=0.3)
    ax2.set_xticks(x)
    ax2.set_xticklabels([f"#{i}\n{d}" for i, d in zip(x, labels)], fontsize=8)
    ax2.legend(loc="lower right", ncol=4, fontsize=8)

    fig.suptitle("Oral English Practice — progress", fontsize=14)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    fig.savefig(out, dpi=120)
    print(f"Chart written to: {out}  ({len(rows)} sessions)")


if __name__ == "__main__":
    main()
