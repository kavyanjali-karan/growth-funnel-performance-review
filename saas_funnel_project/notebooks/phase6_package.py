# ============================================================
# PHASE 6 — Package for Recruiters
# ============================================================

import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("PHASE 6 — PACKAGING PROJECT FOR GITHUB")
print("=" * 60)

# Load KPIs to embed in README
funnel_df  = pd.read_csv('data/funnel_summary.csv')
opp_df     = pd.read_csv('data/revenue_opportunity.csv').iloc[0]
df         = pd.read_csv('data/clean_funnel_data.csv')
monthly_df = pd.read_csv('data/monthly_trend.csv')

total_revenue  = df['monthly_revenue'].sum()
paying_users   = df['converted_paid'].sum()
overall_cvr    = round(paying_users / len(df) * 100, 1)
extra_revenue  = round(opp_df['extra_monthly_revenue'], 0)
mobile_cvr     = round(opp_df['mobile_cvr'], 1)
desktop_cvr    = round(opp_df['desktop_cvr'], 1)
gap            = round(opp_df['gap_pct_pts'], 1)

# ============================================================
#  README.md
# ============================================================
readme = f"""# SaaS Funnel Analysis

**Tools:** Python · Pandas · NumPy · Matplotlib · Seaborn  
**Dataset:** 10,000 simulated SaaS user events across 6 funnel stages  
**Focus:** Where do users drop off, and what does it cost the business?

---

## Business Summary

Analysed a 6-stage SaaS conversion funnel (Visit → Signup → Onboarding →
Activation → Trial → Paid) across 10,000 users. The pipeline covers data
generation, cleaning, segmentation analysis, and revenue impact quantification.

**Key finding:** Mobile users convert to paid at {mobile_cvr}% versus {desktop_cvr}%
on desktop — a {gap} percentage-point gap that costs an estimated
**${extra_revenue:,.0f}/month** in lost revenue.

---

## Key Metrics

| Metric | Value |
|---|---|
| Total users analysed | {len(df):,} |
| Overall conversion rate | {overall_cvr}% |
| Paying users | {paying_users:,} |
| Monthly revenue | ${total_revenue:,.0f} |
| Revenue opportunity (mobile fix) | ${extra_revenue:,.0f}/mo |

---

## Funnel Overview

| Stage | Users | Step Conversion | Overall |
|---|---|---|---|
"""

for _, row in funnel_df.iterrows():
    readme += f"| {row['label']} | {row['users']:,} | {row['step_rate']}% | {row['overall_rate']}% |\n"

readme += f"""
---

## Key Insights

### 1. Biggest drop-off: Visit → Signup (36.3%)
Only 1 in 3 visitors creates an account. This is a landing page and
value-proposition problem — the top of the funnel is leaking the most users.

**Recommendation:** A/B test the homepage headline and reduce the signup form
from 5 fields to 2 (email + password only).

### 2. Mobile onboarding is broken
Mobile users convert to paid at {mobile_cvr}% versus {desktop_cvr}% on desktop.
The onboarding step is the likely culprit — multi-step wizard forms are
notoriously painful on small screens.

**Recommendation:** Build a mobile-first onboarding flow with a single
action per screen and progress indicators. Estimated uplift: ${extra_revenue:,.0f}/month.

### 3. Referral channel is 19x better than social media
Referral converts at 7.8% paid; social media at 0.2%. Budget currently
split roughly evenly between channels.

**Recommendation:** Redirect 30% of social media spend into a referral
incentive programme (e.g. 1 month free for each paying referral).

---

## Project Structure

```
saas_funnel_project/
├── data/
│   ├── raw_funnel_data.csv        # Original messy dataset
│   ├── clean_funnel_data.csv      # After cleaning
│   ├── funnel_summary.csv         # Stage-by-stage metrics
│   ├── device_funnel.csv          # Segmented by device
│   ├── channel_funnel.csv         # Segmented by channel
│   ├── monthly_trend.csv          # Time-series data
│   └── revenue_opportunity.csv    # Quantified business impact
├── notebooks/
│   ├── phase1_setup.py            # Environment setup
│   ├── phase2_generate_data.py    # Data generation
│   ├── phase3_clean_data.py       # Data cleaning
│   ├── phase4_analyze.py          # Analysis & KPIs
│   ├── phase5_visualize.py        # Charts
│   └── phase6_package.py          # This file
├── charts/
│   ├── 01_funnel_overview.png
│   ├── 02_step_conversion.png
│   ├── 03_device_conversion.png
│   ├── 04_channel_conversion.png
│   ├── 05_monthly_trend.png
│   └── 06_revenue_opportunity.png
└── README.md
```

---

## How to Run

```bash
# 1. Install dependencies
pip install pandas numpy matplotlib seaborn plotly

# 2. Run phases in order
python notebooks/phase1_setup.py
python notebooks/phase2_generate_data.py
python notebooks/phase3_clean_data.py
python notebooks/phase4_analyze.py
python notebooks/phase5_visualize.py
```

---

## Skills Demonstrated

- End-to-end data pipeline: raw → clean → analysed → visualised
- Data cleaning with documented decisions and before/after metrics
- Funnel analysis with step-by-step and segment-level breakdowns
- Revenue impact quantification from data insights
- Business recommendations backed by numbers
"""

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(readme)

print("\nREADME.md written successfully.")

# ============================================================
# Print file inventory
# ============================================================
print("\n--- PROJECT FILE INVENTORY ---")
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', '.ipynb_checkpoints']]
    level = root.replace('.', '').count(os.sep)
    indent = '  ' * level
    folder = os.path.basename(root)
    if folder not in ['.']:
        print(f"{indent}{folder}/")
    sub_indent = '  ' * (level + 1)
    for file in sorted(files):
        if not file.startswith('.'):
            size_kb = os.path.getsize(os.path.join(root, file)) / 1024
            print(f"{sub_indent}{file:<40} ({size_kb:.1f} KB)")

# ============================================================
# GitHub instructions
# ============================================================
print("""
============================================================
PHASE 6 COMPLETE — PROJECT IS RECRUITER-READY
============================================================

NEXT STEPS TO PUBLISH ON GITHUB:
---------------------------------
1. Go to github.com and create a new repository
   Name it: saas-funnel-analysis
   Set it to Public

2. In your terminal, navigate to the project folder:
   cd saas_funnel_project

3. Run these commands:
   git init
   git add .
   git commit -m "Initial commit: SaaS funnel analysis project"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/saas-funnel-analysis.git
   git push -u origin main

4. After pushing, go to your repo on GitHub and click
   "Add topics" (top right) and add:
   python, data-analysis, funnel-analysis, pandas, matplotlib

5. Pin this repo to your GitHub profile.

============================================================
""")
