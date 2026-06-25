import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(42)

BASE_DIR = Path(__file__).parent

RAW_DIR = BASE_DIR / "raw"
CURATED_DIR = BASE_DIR / "curated"
WAREHOUSE_DIR = BASE_DIR / "warehouse"

for d in [RAW_DIR, CURATED_DIR, WAREHOUSE_DIR]:
    d.mkdir(parents=True, exist_ok=True)

START_DATE = "2024-01-01"
END_DATE = "2025-12-31"

dates = pd.date_range(
    START_DATE,
    END_DATE,
    freq="D"
)

channels = [
    "Organic",
    "Google",
    "LinkedIn",
    "Facebook",
    "Referral",
    "Email",
    "Direct",
    "Partner"
]

channel_weights = {
    "Organic":0.30,
    "Google":0.22,
    "LinkedIn":0.08,
    "Facebook":0.15,
    "Referral":0.08,
    "Email":0.05,
    "Direct":0.08,
    "Partner":0.04
}

signup_rates = {
    "Organic":0.06,
    "Google":0.055,
    "LinkedIn":0.09,
    "Facebook":0.04,
    "Referral":0.08,
    "Email":0.07,
    "Direct":0.05,
    "Partner":0.10
}

trial_rates = {
    "Organic":0.45,
    "Google":0.40,
    "LinkedIn":0.55,
    "Facebook":0.35,
    "Referral":0.50,
    "Email":0.45,
    "Direct":0.40,
    "Partner":0.60
}

paid_rates = {
    "Organic":0.28,
    "Google":0.25,
    "LinkedIn":0.35,
    "Facebook":0.20,
    "Referral":0.38,
    "Email":0.30,
    "Direct":0.25,
    "Partner":0.40
}

mrr_per_customer = {
    "Organic":220,
    "Google":220,
    "LinkedIn":350,
    "Facebook":180,
    "Referral":300,
    "Email":240,
    "Direct":250,
    "Partner":400
}

visitor_rows = []
signup_rows = []
trial_rows = []
paid_rows = []
spend_rows = []

for date in dates:

    for channel in channels:

        base = int(
            np.random.normal(
                3000 * channel_weights[channel],
                150
            )
        )

        visitors = max(base,50)

        signups = int(
            visitors *
            signup_rates[channel]
        )

        trials = int(
            signups *
            trial_rates[channel]
        )

        paid = int(
            trials *
            paid_rates[channel]
        )

        mrr = paid * mrr_per_customer[channel]

        spend = round(
            visitors *
            np.random.uniform(0.15,1.50),
            2
        )

        visitor_rows.append({
            "date":date,
            "channel":channel,
            "device":
                np.random.choice([
                    "Desktop",
                    "Mobile",
                    "Tablet"
                ],
                p=[0.55,0.40,0.05]),
            "country":
                np.random.choice([
                    "India",
                    "USA",
                    "UK",
                    "Germany",
                    "Australia"
                ]),
            "visitors":visitors
        })

        signup_rows.append({
            "date":date,
            "channel":channel,
            "signups":signups
        })

        trial_rows.append({
            "date":date,
            "channel":channel,
            "trial_users":trials
        })

        paid_rows.append({
            "date":date,
            "channel":channel,
            "paid_customers":paid,
            "mrr":mrr
        })

        spend_rows.append({
            "date":date,
            "channel":channel,
            "spend":spend
        })

visitors_df = pd.DataFrame(visitor_rows)
signups_df = pd.DataFrame(signup_rows)
trials_df = pd.DataFrame(trial_rows)
paid_df = pd.DataFrame(paid_rows)
spend_df = pd.DataFrame(spend_rows)

visitors_df.to_csv(
    RAW_DIR/"visitors.csv",
    index=False
)

signups_df.to_csv(
    RAW_DIR/"signups.csv",
    index=False
)

trials_df.to_csv(
    RAW_DIR/"trials.csv",
    index=False
)

paid_df.to_csv(
    RAW_DIR/"paid_customers.csv",
    index=False
)

spend_df.to_csv(
    RAW_DIR/"marketing_spend.csv",
    index=False
)

funnel = visitors_df.merge(
    signups_df,
    on=["date","channel"]
).merge(
    trials_df,
    on=["date","channel"]
).merge(
    paid_df,
    on=["date","channel"]
)

funnel["visit_to_signup"] = (
    funnel["signups"] /
    funnel["visitors"]
)

funnel["signup_to_trial"] = (
    funnel["trial_users"] /
    funnel["signups"]
)

funnel["trial_to_paid"] = (
    funnel["paid_customers"] /
    funnel["trial_users"]
)

funnel.to_csv(
    CURATED_DIR/"funnel_metrics.csv",
    index=False
)

channel_metrics = (
    funnel
    .groupby("channel")
    .agg({
        "visitors":"sum",
        "signups":"sum",
        "trial_users":"sum",
        "paid_customers":"sum",
        "mrr":"sum"
    })
    .reset_index()
)

channel_metrics.to_csv(
    CURATED_DIR/"channel_metrics.csv",
    index=False
)

cohort_rows = []

months = pd.date_range(
    START_DATE,
    END_DATE,
    freq="MS"
)

for month in months:

    base = 100

    for n in range(13):

        retention = max(
            100 - (n*6) + np.random.randint(-2,3),
            25
        )

        cohort_rows.append({
            "cohort_month":
                month.strftime("%Y-%m"),
            "month_number":n,
            "retention_rate":retention
        })

cohort_df = pd.DataFrame(cohort_rows)

cohort_df.to_csv(
    CURATED_DIR/"retention_cohorts.csv",
    index=False
)

cohort_df.to_csv(
    CURATED_DIR/"cohort_metrics.csv",
    index=False
)

growth_targets = pd.DataFrame({
    "month":
        months.strftime("%Y-%m"),
    "visitor_target":
        np.random.randint(
            50000,
            120000,
            len(months)
        ),
    "signup_target":
        np.random.randint(
            2500,
            9000,
            len(months)
        ),
    "mrr_target":
        np.random.randint(
            100000,
            500000,
            len(months)
        )
})

growth_targets.to_csv(
    WAREHOUSE_DIR/
    "growth_targets.csv",
    index=False
)

channel_targets = pd.DataFrame({
    "channel":channels,
    "cac_target":[
        40,
        50,
        70,
        45,
        35,
        25,
        30,
        80
    ]
})

channel_targets.to_csv(
    WAREHOUSE_DIR/
    "channel_targets.csv",
    index=False
)

calendar = pd.DataFrame({
    "event_date":[
        "2024-01-01",
        "2024-04-01",
        "2024-07-01",
        "2024-10-01",
        "2025-01-01",
        "2025-04-01",
        "2025-07-01",
        "2025-10-01"
    ],
    "event_name":[
        "Q1 Planning",
        "Q2 Planning",
        "Q3 Planning",
        "Q4 Planning",
        "Q1 Planning",
        "Q2 Planning",
        "Q3 Planning",
        "Q4 Planning"
    ]
})

calendar.to_csv(
    WAREHOUSE_DIR/
    "growth_calendar.csv",
    index=False
)

print("Growth Funnel datasets generated.")