# E-Commerce Conversion Funnel Analysis

[![CI](https://github.com/kavyanjali-karan/growth-funnel-performance-review/actions/workflows/ci.yml/badge.svg)](https://github.com/kavyanjali-karan/growth-funnel-performance-review/actions/workflows/ci.yml) [![tests: 18 passed](https://img.shields.io/badge/tests-18%20passed-2ea44f)](tests/) [![license: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

2,243,206 visitors landed in the store. 15,613 of them ever paid. That
0.70% visitor-to-paid conversion is the number this project exists to
explain: seven stages sit between those two figures, and before this
analysis nobody could say which one was leaking.

The repo turns 2.24M **simulated** visitor records into that 7-stage
funnel, from acquisition through signup, onboarding, profile completion,
feature activation, trial and payment. SQL and Python do the pipeline
work; a Power BI model does the reporting. The
[interactive dashboard](https://kavyanjali-karan.github.io/growth-funnel-performance-review/dashboard.html)
is rebuilt in CI from the committed data, so the live page always matches
the tables below.

## Where the funnel leaked

Money was going out to eight acquisition channels, but there was no
single view of where visitors fell away between landing and paying.
Signup-to-trial conversion swung hard from channel to channel, and the
product team had no evidence for which onboarding steps actually
correlated with paying. Every optimization debate started from opinion,
because nobody knew which stage leaked most.

## How the pipeline works

1. **Build the data** — 2.24M visitor records across 8 channels, with
   session-level detail (device, country, session duration) plus
   daily-channel aggregations
2. **Track every stage** — SQL and Python move each visitor from
   Acquisition → Signup → Onboarding → Profile Completion → Feature
   Activation → Trial → Paid Conversion
3. **Model it in Power BI** — a star schema with DAX measures for the
   three conversion stages (signup 6.05%, trial 43.86%, paid 26.25%),
   broken down by channel and device
4. **Write the definitions down** — metric definitions, SOPs and
   optimization recommendations for each funnel stage

## Key Findings

| Stage | Conversion Rate | Volume |
|-------|----------------|--------|
| Visitor → Signup | 6.05% | 135,611 signups from 2.24M visitors |
| Signup → Trial | 43.86% | 59,474 trials from 135,611 signups |
| Trial → Paid | 26.25% | 15,613 paid from 59,474 trials |
| **Visitor → Paid** | **0.70%** | **15,613 paid customers** |

The biggest drop-off is at the Visitor → Signup stage (93.95% attrition), suggesting acquisition targeting and landing page optimization are the highest-leverage improvement areas.

## Data

The dataset simulates an e-commerce platform with multi-channel visitor acquisition:

| Dataset | Records | Description |
|---------|---------|-------------|
| `visitors.csv` | 5,848 | Daily × channel aggregations (sum = 2,243,206 visitors) |
| `visitors_granular.csv` | 2,243,206 | Individual visitor records with device, country, session duration — ~97 MB, kept out of git and rebuilt with `data/generate_granular_visitors.py` (seeded, byte-identical) |
| `signups.csv` | 5,848 | Daily signups by channel |
| `trials.csv` | 5,848 | Daily trial initiations by channel |
| `paid_customers.csv` | 5,848 | Daily paid conversions by channel |
| `onboarded.csv` | 5,848 | Daily onboarding completions |
| `profile_completed.csv` | 5,848 | Daily profile completions |
| `activated_feature.csv` | 5,848 | Daily feature activations |
| `marketing_spend.csv` | 5,848 | Daily marketing spend by channel |

Rebuilding the data:
```bash
pip install pandas numpy
python data/generate_data.py           # aggregated CSVs
python data/generate_granular_visitors.py  # 2.24M-row granular file
```

## Dashboards

No chart below was made in a design tool. Two scripts render straight
from the pipeline output: [`python/generate_dashboard_pngs.py`](python/generate_dashboard_pngs.py)
for the images and [`python/generate_dashboards.py`](python/generate_dashboards.py)
for the interactive page, sharing one Power BI-style visual language.

### Funnel Analysis
![Funnel Analysis](assets/funnel_analysis.png)

### Channel Performance
![Channel Performance](assets/channel_performance.png)

### Cohort Analysis
![Cohort Analysis](assets/cohort_analysis.png)

### Retention Metrics
![Retention Metrics](assets/retention_metrics.png)

### Executive Overview
![Executive Overview](assets/executive_overview.png)

### Rebuilding the dashboards

```bash
python data/generate_data.py              # datasets (seeded, reproducible)
python python/generate_dashboard_pngs.py  # renders assets/*.png
python python/generate_dashboards.py      # builds assets/dashboard.html (Chart.js inlined, no CDN)
```

A push triggers a rebuild of both from the committed data before Pages
publishes, so a stale screenshot isn't something this repo can produce.

## Project Structure

```
├── data/
│   ├── raw/              # Generated CSVs (visitors, signups, trials, etc.)
│   ├── curated/          # Aggregated metrics by channel, cohort
│   └── warehouse/        # Target calendars, growth goals
├── sql/
│   ├── ddl/              # Table definitions
│   ├── staging/          # Staging views
│   ├── marts/            # Business marts
│   ├── metrics/          # Metric calculations
│   ├── monitoring/       # Data quality checks
│   └── reporting/        # Dashboard queries
├── python/
│   ├── extraction/       # Data loading
│   ├── transformation/   # Cleaning and enrichment
│   ├── validation/       # Quality checks
│   ├── monitoring/       # Pipeline health
│   ├── reporting/        # Business report scripts
│   ├── generate_dashboard_pngs.py   # Renders the dashboard PNGs in assets/
│   └── generate_dashboards.py       # Builds the interactive assets/dashboard.html
├── powerbi/
│   ├── dax/              # DAX measures (acquisition, conversion, retention, revenue, time intelligence)
│   └── model/            # Semantic model docs
├── docs/                 # Architecture, glossary, metric dictionary, business reviews, scorecards
├── outputs/              # Generated reports
├── tests/                # Data quality tests (pytest)
└── assets/               # Dashboard screenshots
```

## Running Tests

```bash
pip install pytest pandas numpy
pytest
```

18 tests covering data quality, funnel-stage math, and dashboard inputs. Fresh clones need no setup — the datasets regenerate on the first run of the suite.

## Tech Stack

SQL, Python (pandas, numpy), Power BI, DAX, Power Query, pytest, GitHub Actions, Git
