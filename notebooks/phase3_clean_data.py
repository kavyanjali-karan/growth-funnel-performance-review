# ============================================================
# PHASE 3 — Clean & Validate the Data
# ============================================================

import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

FUNNEL_STAGES = [
    'visited_site', 'signed_up', 'completed_onboard',
    'activated_feature', 'started_trial', 'converted_paid',
]

print("=" * 55)
print("PHASE 3 — DATA CLEANING & VALIDATION")
print("=" * 55)

# ----------------------------------------------------------
# STEP 1: Load raw data
# ----------------------------------------------------------
df = pd.read_csv('data/raw_funnel_data.csv', parse_dates=['signup_date'])
raw_row_count = len(df)
print(f"\nRaw data loaded: {raw_row_count} rows, {df.shape[1]} columns")

# ----------------------------------------------------------
# STEP 2: Initial audit — understand what's broken
# ----------------------------------------------------------
print("\n--- DATA QUALITY AUDIT ---")
print(f"Duplicate rows        : {df.duplicated().sum()}")
print(f"Missing values:")
for col in df.columns:
    nulls = df[col].isnull().sum()
    if nulls > 0:
        print(f"  {col:<22}: {nulls} ({nulls/len(df)*100:.1f}%)")
print(f"Invalid stage_order   : {(df['stage_order'] == -1).sum()} rows")
print(f"Unrecognised stages   : {(~df['last_stage'].isin(FUNNEL_STAGES)).sum()} rows")

# ----------------------------------------------------------
# STEP 3: Remove exact duplicates
# ----------------------------------------------------------
before = len(df)
df = df.drop_duplicates()
print(f"\nRemoved duplicates    : {before - len(df)} rows dropped")

# ----------------------------------------------------------
# STEP 4: Fix missing channel — fill with 'unknown'
# ----------------------------------------------------------
missing_channel = df['channel'].isnull().sum()
df['channel'] = df['channel'].fillna('unknown')
print(f"Filled missing channel: {missing_channel} rows filled with 'unknown'")

# ----------------------------------------------------------
# STEP 5: Drop rows with invalid stage_order
# ----------------------------------------------------------
before = len(df)
df = df[df['stage_order'] > 0]
print(f"Dropped invalid stages: {before - len(df)} rows removed")

# ----------------------------------------------------------
# STEP 6: Fix data types
# ----------------------------------------------------------
df['signup_date']      = pd.to_datetime(df['signup_date'])
df['user_id']          = df['user_id'].astype(int)
df['stage_order']      = df['stage_order'].astype(int)
df['converted_paid']   = df['converted_paid'].astype(int)
df['monthly_revenue']  = df['monthly_revenue'].astype(float)
print("Data types fixed      : dates, ints, floats all correct")

# ----------------------------------------------------------
# STEP 7: Add derived columns useful for analysis
# ----------------------------------------------------------
# Month of signup — useful for time-series charts
df['signup_month'] = df['signup_date'].dt.to_period('M').astype(str)

# Week number — useful for cohort analysis
df['signup_week'] = df['signup_date'].dt.isocalendar().week.astype(int)

# Reached trial or beyond? (binary flag for quick filtering)
df['reached_trial'] = (df['stage_order'] >= 5).astype(int)

print("Derived columns added : signup_month, signup_week, reached_trial")

# ----------------------------------------------------------
# STEP 8: Final validation checks
# ----------------------------------------------------------
print("\n--- POST-CLEANING VALIDATION ---")
assert df.duplicated().sum() == 0,            "FAIL: Duplicates still present"
assert df['channel'].isnull().sum() == 0,     "FAIL: Nulls in channel"
assert (df['stage_order'] < 1).sum() == 0,   "FAIL: Invalid stage_order values"
assert df['converted_paid'].isin([0,1]).all(),"FAIL: converted_paid not binary"
print("All assertions passed: data is clean!")

# ----------------------------------------------------------
# STEP 9: Print cleaning summary
# ----------------------------------------------------------
clean_row_count = len(df)
print(f"\nRows before cleaning  : {raw_row_count}")
print(f"Rows after cleaning   : {clean_row_count}")
print(f"Rows removed total    : {raw_row_count - clean_row_count}")
print(f"Columns now           : {list(df.columns)}")

# ----------------------------------------------------------
# STEP 10: Save clean data
# ----------------------------------------------------------
os.makedirs('data', exist_ok=True)
df.to_csv('data/clean_funnel_data.csv', index=False)
print(f"\nClean file saved: data/clean_funnel_data.csv")
print("=" * 55)
print("PHASE 3 COMPLETE — ready for analysis")
print("=" * 55)
