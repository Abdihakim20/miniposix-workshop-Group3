#!/usr/bin/env python3
"""Summarize local pipe benchmark CSV results and save a throughput plot."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


REQUIRED_COLUMNS = {
    "variant",
    "buffer_bytes",
    "total_bytes",
    "seconds",
    "throughput_mib_s",
    "repeat",
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path, help="CSV produced by bench_pipe")
    parser.add_argument(
        "--plot",
        type=Path,
        default=Path("bench-results/throughput.png"),
        help="output PNG (default: bench-results/throughput.png)",
    )
    args = parser.parse_args()

    data = pd.read_csv(args.csv)
    missing = REQUIRED_COLUMNS.difference(data.columns)
    if missing:
        parser.error(f"missing CSV columns: {', '.join(sorted(missing))}")
    if data.empty:
        parser.error("CSV has no measurements")

    numeric = ["buffer_bytes", "total_bytes", "seconds", "throughput_mib_s", "repeat"]
    for column in numeric:
        data[column] = pd.to_numeric(data[column], errors="raise")
    if data[numeric].isna().any().any():
        parser.error("CSV contains missing numeric values")
    if (data[["buffer_bytes", "total_bytes", "seconds", "throughput_mib_s"]] <= 0).any().any():
        parser.error("buffer size, total bytes, elapsed time, and throughput must be positive")

    summary = (
        data.groupby(["variant", "buffer_bytes"], sort=True)["throughput_mib_s"]
        .agg(samples="count", mean="mean", median="median", minimum="min", maximum="max", std="std")
        .reset_index()
    )
    summary["std"] = summary["std"].fillna(0)
    print(summary.to_string(index=False, float_format=lambda value: f"{value:.2f}"))

    fig, ax = plt.subplots(figsize=(8, 5))
    for variant, group in summary.groupby("variant", sort=True):
        ax.errorbar(
            group["buffer_bytes"],
            group["mean"],
            yerr=group["std"],
            marker="o",
            capsize=3,
            label=str(variant),
        )
    ticks = np.sort(data["buffer_bytes"].unique())
    ax.set_xscale("log", base=2)
    ax.set_xticks(ticks, [str(value) for value in ticks])
    ax.set_xlabel("Buffer size (bytes)")
    ax.set_ylabel("Throughput (MiB/s)")
    ax.set_title("Local pipe transfer: mean ± sample standard deviation")
    ax.grid(axis="y", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    args.plot.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.plot, dpi=150)
    print(f"Saved plot: {args.plot}")


if __name__ == "__main__":
    main()
