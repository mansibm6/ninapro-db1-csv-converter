"""Validate NinaPro DB1 arrays and export their original column layout."""

from pathlib import Path
import argparse
import numpy as np
import pandas as pd
from scipy.io import loadmat


def _matrix(data, key, rows=None, columns=None):
    if key not in data:
        raise ValueError(f"Missing MAT variable: {key}")
    value = np.asarray(data[key])
    if (
        value.ndim != 2
        or (rows is not None and len(value) != rows)
        or (columns is not None and value.shape[1] != columns)
    ):
        raise ValueError(f"Unexpected shape for {key}: {value.shape}")
    if not np.issubdtype(value.dtype, np.number) or not np.isfinite(value).all():
        raise ValueError(f"{key} must contain finite numeric values")
    return value


def _column(data, key, rows):
    value = _matrix(data, key).reshape(-1)
    if value.size == 1:
        return np.repeat(value, rows)
    if value.size != rows:
        raise ValueError(f"{key} must have one value or {rows} samples")
    return value


def to_frame(data, full=True):
    """Broadcast scalar metadata, retaining sample-aligned labels without truncation."""
    emg = _matrix(data, "emg", columns=10)
    rows = len(emg)
    if not rows:
        raise ValueError("EMG data is empty")
    frame = pd.DataFrame(emg, columns=[f"emg_{i}" for i in range(10)])
    if full:
        glove = _matrix(data, "glove", rows=rows, columns=22)
        for i in range(22):
            frame[f"glove_{i}"] = glove[:, i]
    keys = ["exercise", "stimulus"]
    if full:
        keys += ["restimulus", "repetition", "rerepetition", "subject"]
    for key in keys:
        frame[key] = _column(data, key, rows)
    return frame


def convert_directory(input_dir, output, full=True):
    """Convert sorted MAT files. Retain the legacy per-file CSV index column."""
    paths = sorted(Path(input_dir).glob("*.mat"))
    if not paths:
        raise FileNotFoundError(f"No .mat files in {input_dir}")
    frames = [to_frame(loadmat(path), full=full) for path in paths]
    result = pd.concat(frames)
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output, index=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("--output", type=Path, default=Path("Ninapro_DB1.csv"))
    args = parser.parse_args()
    frame = convert_directory(args.input_dir, args.output)
    print(f"Wrote {len(frame)} rows to {args.output}")


if __name__ == "__main__":
    main()
