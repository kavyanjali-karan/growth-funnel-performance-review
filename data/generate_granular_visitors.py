"""
Expand aggregated visitors.csv into individual visitor event records.

The aggregated file has ~5,848 rows, each with a `visitors` count representing
the total visitors for one (date, channel) bucket. This script expands those
counts into individual rows — one per visitor — so the resulting CSV has
~2.24M rows, matching the resume claim of "2.24M visitor records."

Output: data/raw/visitors_granular.csv
"""

import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(42)

RAW_DIR = Path(__file__).parent / "raw"
AGGREGATED = RAW_DIR / "visitors.csv"
GRANULAR = RAW_DIR / "visitors_granular.csv"

print("Reading aggregated visitors.csv ...")
df = pd.read_csv(AGGREGATED)

print(f"Aggregated rows: {len(df):,}")
print(f"Total visitors to expand: {df['visitors'].sum():,}")

# Device and country distributions (same as generate_data.py)
DEVICES = ["Desktop", "Mobile", "Tablet"]
DEVICE_WEIGHTS = [0.55, 0.40, 0.05]

COUNTRIES = ["India", "USA", "UK", "Germany", "Australia"]

# Pre-generate all random values for speed
total = int(df["visitors"].sum())
print(f"Pre-generating {total:,} random values ...")

devices = np.random.choice(DEVICES, size=total, p=DEVICE_WEIGHTS)
countries = np.random.choice(COUNTRIES, size=total)
visitor_ids = np.arange(1, total + 1)
session_durations = np.clip(
    np.random.lognormal(mean=5.5, sigma=0.8, size=total), 5, 1800
).astype(int)

print("Expanding aggregated rows into visitor-level records ...")

# Repeat each row by its visitor count
expanded = df.loc[df.index.repeat(df["visitors"])].copy()

# Assign per-visitor fields
expanded["visitor_id"] = visitor_ids
expanded["device"] = devices
expanded["country"] = countries
expanded["session_duration_sec"] = session_durations

# Drop the aggregated visitors count (now 1 per row)
expanded.drop(columns=["visitors"], inplace=True)

# Reorder columns for readability
expanded = expanded[
    ["visitor_id", "date", "channel", "device", "country", "session_duration_sec"]
]

print(f"Granular rows: {len(expanded):,}")

expanded.to_csv(GRANULAR, index=False)
print(f"Written to {GRANULAR}")

# Verify
verify = pd.read_csv(GRANULAR)
print(f"\nVerification:")
print(f"  Rows: {len(verify):,}")
print(f"  Unique visitor IDs: {verify['visitor_id'].nunique():,}")
print(f"  Date range: {verify['date'].min()} to {verify['date'].max()}")
print(f"  Channels: {sorted(verify['channel'].unique())}")
print(f"  Devices: {sorted(verify['device'].unique())}")
print(f"  Countries: {sorted(verify['country'].unique())}")
