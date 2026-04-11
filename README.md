# SaaS Funnel Analysis

**Tools:** Python · Pandas · NumPy · Matplotlib · Seaborn  
**Dataset:** 10,000 simulated SaaS user events across 6 funnel stages  
**Focus:** Where do users drop off, and what does it cost the business?

---

## Business Summary

Analysed a 6-stage SaaS conversion funnel (Visit → Signup → Onboarding →
Activation → Trial → Paid) across 10,000 users. The pipeline covers data
generation, cleaning, segmentation analysis, and revenue impact quantification.

**Key finding:** Mobile users convert to paid at 0.6% versus 4.2%
on desktop — a 3.6 percentage-point gap that costs an estimated
**$8,828/month** in lost revenue.

---

## Key Metrics

| Metric | Value |
|---|---|
| Total users analysed | 9,995 |
| Overall conversion rate | 2.8% |
| Paying users | 277 |
| Monthly revenue | $19,563 |
| Revenue opportunity (mobile fix) | $8,828/mo |

---

## Funnel Overview

| Stage | Users | Step Conversion | Overall |
|---|---|---|---|
| Visited Site | 9,995 | 100.0% | 100.0% |
| Signed Up | 3,632 | 36.3% | 36.3% |
| Completed Onboarding | 1,984 | 54.6% | 19.8% |
| Activated Feature | 1,255 | 63.3% | 12.6% |
| Started Trial | 695 | 55.4% | 7.0% |
| Converted to Paid | 277 | 39.9% | 2.8% |

---

## Key Insights

### 1. Biggest drop-off: Visit → Signup (36.3%)
Only 1 in 3 visitors creates an account. This is a landing page and
value-proposition problem — the top of the funnel is leaking the most users.

**Recommendation:** A/B test the homepage headline and reduce the signup form
from 5 fields to 2 (email + password only).

### 2. Mobile onboarding is broken
Mobile users convert to paid at 0.6% versus 4.2% on desktop.
The onboarding step is the likely culprit — multi-step wizard forms are
notoriously painful on small screens.

**Recommendation:** Build a mobile-first onboarding flow with a single
action per screen and progress indicators. Estimated uplift: $8,828/month.

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
