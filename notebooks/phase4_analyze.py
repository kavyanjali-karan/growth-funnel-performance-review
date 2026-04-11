# ============================================================
# PHASE 4 — Analyze the Funnel
# ============================================================

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

FUNNEL_STAGES = [
    'visited_site', 'signed_up', 'completed_onboard',
    'activated_feature', 'started_trial', 'converted_paid',
]

STAGE_LABELS = {
    'visited_site':      'Visited Site',
    'signed_up':         'Signed Up',
    'completed_onboard': 'Completed Onboarding',
    'activated_feature': 'Activated Feature',
    'started_trial':     'Started Trial',
    'converted_paid':    'Converted to Paid',
}

print("=" * 60)
print("PHASE 4 — FUNNEL ANALYSIS")
print("=" * 60)

# ----------------------------------------------------------
# STEP 1: Load clean data
# ----------------------------------------------------------
df = pd.read_csv('data/clean_funnel_data.csv', parse_dates=['signup_date'])
print(f"\nClean data loaded: {len(df)} rows")

# ----------------------------------------------------------
# STEP 2: Calculate users reaching each stage
# A user "reaches" a stage if their last_stage is that stage
# OR any stage that comes after it in the funnel
# ----------------------------------------------------------
stage_counts = {}
for stage in FUNNEL_STAGES:
    stage_idx = FUNNEL_STAGES.index(stage)
    count = (df['stage_order'] >= stage_idx + 1).sum()
    stage_counts[stage] = count

# Build funnel summary DataFrame
funnel_df = pd.DataFrame({
    'stage':     FUNNEL_STAGES,
    'label':     [STAGE_LABELS[s] for s in FUNNEL_STAGES],
    'users':     [stage_counts[s] for s in FUNNEL_STAGES],
})

# Overall conversion rate vs stage 1
funnel_df['overall_rate'] = (funnel_df['users'] / funnel_df['users'].iloc[0] * 100).round(1)

# Step-by-step conversion (how many from the previous stage made it)
funnel_df['step_rate'] = 100.0
for i in range(1, len(funnel_df)):
    prev = funnel_df.loc[i-1, 'users']
    curr = funnel_df.loc[i, 'users']
    funnel_df.loc[i, 'step_rate'] = round(curr / prev * 100, 1) if prev > 0 else 0.0

# Drop-off at each step
funnel_df['dropped'] = funnel_df['users'].shift(0) - funnel_df['users'].shift(-1)
funnel_df['dropped'] = funnel_df['dropped'].fillna(0).astype(int)

print("\n--- OVERALL FUNNEL ---")
print(f"{'Stage':<25} {'Users':>7} {'Step Rate':>10} {'Overall':>9} {'Dropped':>8}")
print("-" * 62)
for _, row in funnel_df.iterrows():
    print(f"{row['label']:<25} {row['users']:>7,} {row['step_rate']:>9.1f}% {row['overall_rate']:>8.1f}% {row['dropped']:>8,}")

# Save for later use in charts
funnel_df.to_csv('data/funnel_summary.csv', index=False)

# ----------------------------------------------------------
# STEP 3: Find the BIGGEST drop-off step
# ----------------------------------------------------------
worst_idx  = funnel_df['step_rate'][1:].idxmin()
worst_step = funnel_df.loc[worst_idx, 'label']
worst_rate = funnel_df.loc[worst_idx, 'step_rate']
prev_step  = funnel_df.loc[worst_idx - 1, 'label']

print(f"\n*** BIGGEST DROP-OFF: {prev_step} → {worst_step} ({worst_rate}% conversion) ***")

# ----------------------------------------------------------
# STEP 4: Segment by DEVICE — find mobile problem
# ----------------------------------------------------------
device_funnel = []
for device in df['device'].unique():
    sub = df[df['device'] == device]
    for stage in FUNNEL_STAGES:
        idx   = FUNNEL_STAGES.index(stage)
        count = (sub['stage_order'] >= idx + 1).sum()
        total = len(sub)
        device_funnel.append({
            'device': device,
            'stage':  STAGE_LABELS[stage],
            'users':  count,
            'rate':   round(count / total * 100, 1),
        })

device_df = pd.DataFrame(device_funnel)
device_df.to_csv('data/device_funnel.csv', index=False)

print("\n--- CONVERSION TO PAID BY DEVICE ---")
paid_by_device = device_df[device_df['stage'] == 'Converted to Paid'][['device','rate']].sort_values('rate', ascending=False)
for _, row in paid_by_device.iterrows():
    bar = '█' * int(row['rate'] / 1)
    print(f"  {row['device']:<10} {row['rate']:>5.1f}%  {bar}")

# ----------------------------------------------------------
# STEP 5: Segment by CHANNEL
# ----------------------------------------------------------
channel_funnel = []
for ch in df['channel'].unique():
    sub   = df[df['channel'] == ch]
    total = len(sub)
    for stage in FUNNEL_STAGES:
        idx   = FUNNEL_STAGES.index(stage)
        count = (sub['stage_order'] >= idx + 1).sum()
        channel_funnel.append({
            'channel': ch,
            'stage':   STAGE_LABELS[stage],
            'users':   count,
            'rate':    round(count / total * 100, 1),
        })

channel_df = pd.DataFrame(channel_funnel)
channel_df.to_csv('data/channel_funnel.csv', index=False)

print("\n--- CONVERSION TO PAID BY CHANNEL ---")
paid_by_ch = channel_df[channel_df['stage'] == 'Converted to Paid'][['channel','rate']].sort_values('rate', ascending=False)
for _, row in paid_by_ch.iterrows():
    bar = '█' * int(row['rate'] / 1)
    print(f"  {row['channel']:<20} {row['rate']:>5.1f}%  {bar}")

# ----------------------------------------------------------
# STEP 6: Revenue KPIs
# ----------------------------------------------------------
total_revenue = df['monthly_revenue'].sum()
paying_users  = df['converted_paid'].sum()
avg_revenue   = (total_revenue / paying_users) if paying_users > 0 else 0
overall_cvr   = paying_users / len(df) * 100

print("\n--- REVENUE KPIs ---")
print(f"  Total monthly revenue : ${total_revenue:,.0f}")
print(f"  Paying users          : {paying_users:,}")
print(f"  Avg revenue per user  : ${avg_revenue:.2f}")
print(f"  Overall conversion    : {overall_cvr:.1f}%")

# ----------------------------------------------------------
# STEP 7: Revenue impact — what if mobile onboarding improved?
# ----------------------------------------------------------
mobile_users = df[df['device'] == 'mobile']
mobile_total = len(mobile_users)
mobile_paid  = mobile_users['converted_paid'].sum()
mobile_cvr   = mobile_paid / mobile_total * 100

desktop_users = df[df['device'] == 'desktop']
desktop_cvr   = desktop_users['converted_paid'].sum() / len(desktop_users) * 100

# If mobile converted at desktop rate, how much extra revenue?
extra_conversions = int(mobile_total * (desktop_cvr - mobile_cvr) / 100)
avg_plan_rev      = avg_revenue
extra_revenue     = extra_conversions * avg_plan_rev

print(f"\n--- REVENUE OPPORTUNITY (Mobile Fix) ---")
print(f"  Mobile conversion rate   : {mobile_cvr:.1f}%")
print(f"  Desktop conversion rate  : {desktop_cvr:.1f}%")
print(f"  Gap                      : {desktop_cvr - mobile_cvr:.1f} percentage points")
print(f"  Extra conversions if fixed: {extra_conversions:,} users")
print(f"  Extra monthly revenue    : ${extra_revenue:,.0f}")

# Save revenue opportunity data
opportunity = {
    'mobile_cvr': round(mobile_cvr, 2),
    'desktop_cvr': round(desktop_cvr, 2),
    'gap_pct_pts': round(desktop_cvr - mobile_cvr, 2),
    'extra_conversions': extra_conversions,
    'extra_monthly_revenue': round(extra_revenue, 2),
}
pd.DataFrame([opportunity]).to_csv('data/revenue_opportunity.csv', index=False)

# ----------------------------------------------------------
# STEP 8: Monthly trend
# ----------------------------------------------------------
monthly = df.groupby('signup_month').agg(
    users=('user_id', 'count'),
    conversions=('converted_paid', 'sum'),
    revenue=('monthly_revenue', 'sum'),
).reset_index()
monthly['cvr'] = (monthly['conversions'] / monthly['users'] * 100).round(1)
monthly.to_csv('data/monthly_trend.csv', index=False)

print("\n--- MONTHLY CONVERSION TREND ---")
print(monthly[['signup_month','users','conversions','cvr','revenue']].to_string(index=False))

print("\n" + "=" * 60)
print("PHASE 4 COMPLETE — all analysis files saved to data/")
print("=" * 60)
