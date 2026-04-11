# ============================================================
# PHASE 2 — Generate Realistic SaaS Funnel Dataset
# ============================================================

import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)  # Makes results reproducible every time you run it

# ----------------------------------------------------------
# STEP 1: Define our funnel stages
# ----------------------------------------------------------
FUNNEL_STAGES = [
    'visited_site',      # Stage 1: User lands on your website
    'signed_up',         # Stage 2: User creates a free account
    'completed_onboard', # Stage 3: User finishes the setup wizard
    'activated_feature', # Stage 4: User uses the core feature for first time
    'started_trial',     # Stage 5: User clicks "Start 14-day trial"
    'converted_paid',    # Stage 6: User pays — this is the money!
]

# ----------------------------------------------------------
# STEP 2: Define realistic drop-off rates between stages
# e.g. only 40% of visitors sign up
# ----------------------------------------------------------
CONVERSION_RATES = {
    'visited_site':      1.00,   # 100%  — starting point
    'signed_up':         0.40,   # 40%   of visitors sign up
    'completed_onboard': 0.55,   # 55%   of signups complete onboarding
    'activated_feature': 0.60,   # 60%   of onboarded users activate
    'started_trial':     0.50,   # 50%   of activated users start trial
    'converted_paid':    0.35,   # 35%   of trial users pay
}

# ----------------------------------------------------------
# STEP 3: Define segments we want to analyze later
# ----------------------------------------------------------
CHANNELS   = ['organic_search', 'paid_ads', 'referral', 'social_media', 'direct']
DEVICES    = ['desktop', 'mobile', 'tablet']
PLANS      = ['starter', 'professional', 'enterprise']
COUNTRIES  = ['India', 'USA', 'UK', 'Germany', 'Australia', 'Canada', 'Brazil']

# Different channels convert differently — this adds realism
CHANNEL_MULTIPLIERS = {
    'organic_search': 1.2,
    'paid_ads':       0.8,
    'referral':       1.4,
    'social_media':   0.7,
    'direct':         1.1,
}

# Mobile users drop off more on onboarding — a real insight we'll find later
DEVICE_MULTIPLIERS = {
    'desktop': 1.0,
    'mobile':  0.65,   # This is the "problem" in the analysis
    'tablet':  0.85,
}

# ----------------------------------------------------------
# STEP 4: Generate user records
# ----------------------------------------------------------
N_USERS = 10000
print(f"Generating {N_USERS} user records...")

records = []

for user_id in range(1, N_USERS + 1):
    # Assign random attributes to each user
    channel = np.random.choice(CHANNELS, p=[0.35, 0.25, 0.15, 0.15, 0.10])
    device  = np.random.choice(DEVICES,  p=[0.55, 0.35, 0.10])
    country = np.random.choice(COUNTRIES, p=[0.25, 0.25, 0.15, 0.10, 0.10, 0.10, 0.05])
    plan    = np.random.choice(PLANS,     p=[0.60, 0.30, 0.10])

    # Random signup date in the past 6 months
    days_ago = np.random.randint(0, 180)
    signup_date = pd.Timestamp('2024-07-01') + pd.Timedelta(days=int(days_ago))

    # Channel and device both affect how far a user progresses
    ch_mult  = CHANNEL_MULTIPLIERS[channel]
    dev_mult = DEVICE_MULTIPLIERS[device]
    combined = ch_mult * dev_mult

    # Simulate each stage: does this user make it through?
    last_stage_reached = 'visited_site'
    for stage in FUNNEL_STAGES[1:]:
        base_rate  = CONVERSION_RATES[stage]
        actual_rate = min(base_rate * combined, 0.97)  # Cap at 97% max
        if np.random.random() < actual_rate:
            last_stage_reached = stage
        else:
            break  # User dropped off — stop here

    records.append({
        'user_id':          user_id,
        'signup_date':      signup_date,
        'channel':          channel,
        'device':           device,
        'country':          country,
        'plan_type':        plan,
        'last_stage':       last_stage_reached,
        'stage_order':      FUNNEL_STAGES.index(last_stage_reached) + 1,
    })

# ----------------------------------------------------------
# STEP 5: Build DataFrame and add a "converted" column
# ----------------------------------------------------------
df = pd.DataFrame(records)
df['converted_paid'] = (df['last_stage'] == 'converted_paid').astype(int)

# Add a revenue column — only paying users generate revenue
PLAN_REVENUE = {'starter': 29, 'professional': 79, 'enterprise': 299}
df['monthly_revenue'] = df.apply(
    lambda row: PLAN_REVENUE[row['plan_type']] if row['converted_paid'] == 1 else 0,
    axis=1
)

# ----------------------------------------------------------
# STEP 6: Add intentional messiness so we can clean it in Phase 3
# ----------------------------------------------------------
# Add ~2% missing values in channel column
missing_mask = np.random.random(len(df)) < 0.02
df.loc[missing_mask, 'channel'] = np.nan

# Add ~1% duplicate rows (realistic in raw event logs)
duplicate_rows = df.sample(frac=0.01, random_state=42)
df = pd.concat([df, duplicate_rows], ignore_index=True)

# Add a few invalid stage orders
bad_idx = np.random.choice(df.index, size=5, replace=False)
df.loc[bad_idx, 'stage_order'] = -1

print(f"Raw dataset shape: {df.shape[0]} rows x {df.shape[1]} columns")

# ----------------------------------------------------------
# STEP 7: Save raw data (the messy version — we'll clean it next)
# ----------------------------------------------------------
os.makedirs('data', exist_ok=True)
df.to_csv('data/raw_funnel_data.csv', index=False)

print()
print("=" * 50)
print("PHASE 2 COMPLETE")
print("=" * 50)
print(f"  Total rows (with duplicates & nulls): {len(df)}")
print(f"  Columns: {list(df.columns)}")
print(f"  File saved: data/raw_funnel_data.csv")
print()
print("  Preview of first 5 rows:")
print(df.head().to_string(index=False))
print("=" * 50)
