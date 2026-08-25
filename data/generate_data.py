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

onboarded_rates = {
    "Organic":0.82,
    "Google":0.80,
    "LinkedIn":0.85,
    "Facebook":0.75,
    "Referral":0.83,
    "Email":0.80,
    "Direct":0.78,
    "Partner":0.86
}

profile_rates = {
    "Organic":0.80,
    "Google":0.78,
    "LinkedIn":0.82,
    "Facebook":0.73,
    "Referral":0.81,
    "Email":0.79,
    "Direct":0.76,
    "Partner":0.83
}

activated_rates = {
    "Organic":0.85,
    "Google":0.83,
    "LinkedIn":0.88,
    "Facebook":0.80,
    "Referral":0.86,
    "Email":0.84,
    "Direct":0.82,
    "Partner":0.89
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
onboarded_rows = []
profile_rows = []
activated_rows = []
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

        onboarded = int(
            signups *
            onboarded_rates[channel]
        )

        profile_completed = int(
            onboarded *
            profile_rates[channel]
        )

        activated = int(
            profile_completed *
            activated_rates[channel]
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

        onboarded_rows.append({
            "date":date,
            "channel":channel,
            "onboarded":onboarded
        })

        profile_rows.append({
            "date":date,
            "channel":channel,
            "profile_completed":profile_completed
        })

        activated_rows.append({
            "date":date,
            "channel":channel,
            "activated":activated
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
onboarded_df = pd.DataFrame(onboarded_rows)
profile_df = pd.DataFrame(profile_rows)
activated_df = pd.DataFrame(activated_rows)
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

onboarded_df.to_csv(
    RAW_DIR/"onboarded.csv",
    index=False
)

profile_df.to_csv(
    RAW_DIR/"profile_completed.csv",
    index=False
)

activated_df.to_csv(
    RAW_DIR/"activated_feature.csv",
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
    onboarded_df,
    on=["date","channel"]
).merge(
    profile_df,
    on=["date","channel"]
).merge(
    activated_df,
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

funnel["signup_to_onboarded"] = (
    funnel["onboarded"] /
    funnel["signups"]
)

funnel["onboarded_to_profile"] = (
    funnel["profile_completed"] /
    funnel["onboarded"]
)

funnel["profile_to_activated"] = (
    funnel["activated"] /
    funnel["profile_completed"]
)

funnel["activated_to_trial"] = (
    funnel["trial_users"] /
    funnel["activated"]
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
        "onboarded":"sum",
        "profile_completed":"sum",
        "activated":"sum",
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

# ==================================================
# FUNNEL SUMMARY (7 stages)
# ==================================================

total_visitors = funnel["visitors"].sum()
total_signups = funnel["signups"].sum()
total_onboarded = funnel["onboarded"].sum()
total_profile = funnel["profile_completed"].sum()
total_activated = funnel["activated"].sum()
total_trials = funnel["trial_users"].sum()
total_paid = funnel["paid_customers"].sum()

summary_rows = [
    {
        "stage": "visited_site",
        "label": "Visited Site",
        "users": int(total_visitors),
        "overall_rate": 100.0,
        "step_rate": 100.0,
        "dropped": int(total_visitors - total_signups)
    },
    {
        "stage": "signed_up",
        "label": "Signed Up",
        "users": int(total_signups),
        "overall_rate": round(total_signups / total_visitors * 100, 1),
        "step_rate": round(total_signups / total_visitors * 100, 1),
        "dropped": int(total_signups - total_onboarded)
    },
    {
        "stage": "completed_onboard",
        "label": "Completed Onboarding",
        "users": int(total_onboarded),
        "overall_rate": round(total_onboarded / total_visitors * 100, 1),
        "step_rate": round(total_onboarded / total_signups * 100, 1),
        "dropped": int(total_onboarded - total_profile)
    },
    {
        "stage": "completed_profile",
        "label": "Completed Profile",
        "users": int(total_profile),
        "overall_rate": round(total_profile / total_visitors * 100, 1),
        "step_rate": round(total_profile / total_onboarded * 100, 1),
        "dropped": int(total_profile - total_activated)
    },
    {
        "stage": "activated_feature",
        "label": "Activated Feature",
        "users": int(total_activated),
        "overall_rate": round(total_activated / total_visitors * 100, 1),
        "step_rate": round(total_activated / total_profile * 100, 1),
        "dropped": int(total_activated - total_trials)
    },
    {
        "stage": "started_trial",
        "label": "Started Trial",
        "users": int(total_trials),
        "overall_rate": round(total_trials / total_visitors * 100, 1),
        "step_rate": round(total_trials / total_activated * 100, 1),
        "dropped": int(total_trials - total_paid)
    },
    {
        "stage": "converted_paid",
        "label": "Converted to Paid",
        "users": int(total_paid),
        "overall_rate": round(total_paid / total_visitors * 100, 1),
        "step_rate": round(total_paid / total_trials * 100, 1),
        "dropped": 0
    },
]

summary_df = pd.DataFrame(summary_rows)
summary_df.to_csv(
    BASE_DIR/"funnel_summary.csv",
    index=False
)

# ==================================================
# RAW FUNNEL DATA (per-user, 7 stages)
# ==================================================

np.random.seed(42)

N_USERS = 10000

raw_channels = [
    "organic_search",
    "paid_ads",
    "social_media",
    "referral",
    "direct"
]
raw_channel_probs = [0.35, 0.25, 0.20, 0.12, 0.08]

raw_devices = ["desktop", "mobile", "tablet"]
raw_device_probs = [0.50, 0.40, 0.10]

raw_countries = [
    "USA", "India", "UK", "Germany",
    "Australia", "Canada", "Brazil"
]
raw_country_probs = [
    0.25, 0.20, 0.15, 0.12,
    0.10, 0.10, 0.08
]

raw_plans = ["starter", "professional", "enterprise"]
raw_plan_probs = [0.50, 0.35, 0.15]

raw_rows = []
for i in range(1, N_USERS + 1):
    channel = np.random.choice(raw_channels, p=raw_channel_probs)
    device = np.random.choice(raw_devices, p=raw_device_probs)
    country = np.random.choice(raw_countries, p=raw_country_probs)
    plan = np.random.choice(raw_plans, p=raw_plan_probs)

    # Every user visits
    stage = 1
    last_stage = "visited_site"

    # ~36% sign up
    if np.random.random() < 0.363:
        stage = 2
        last_stage = "signed_up"

        # ~54.6% complete onboarding
        if np.random.random() < 0.546:
            stage = 3
            last_stage = "completed_onboard"

            # ~63.3% complete profile
            if np.random.random() < 0.633:
                stage = 4
                last_stage = "completed_profile"

                # ~73.4% activate feature
                if np.random.random() < 0.734:
                    stage = 5
                    last_stage = "activated_feature"

                    # ~55.4% start trial
                    if np.random.random() < 0.554:
                        stage = 6
                        last_stage = "started_trial"

                        # ~39.9% convert to paid
                        if np.random.random() < 0.399:
                            stage = 7
                            last_stage = "converted_paid"

    signup_date = pd.Timestamp("2024-01-01") + pd.Timedelta(
        days=np.random.randint(0, 730)
    )

    converted_paid = 1 if last_stage == "converted_paid" else 0

    if converted_paid:
        if plan == "enterprise":
            monthly_revenue = np.random.randint(199, 499)
        elif plan == "professional":
            monthly_revenue = np.random.randint(49, 149)
        else:
            monthly_revenue = np.random.randint(9, 29)
    else:
        monthly_revenue = 0

    raw_rows.append({
        "user_id": i,
        "signup_date": signup_date.strftime("%Y-%m-%d"),
        "channel": channel,
        "device": device,
        "country": country,
        "plan_type": plan,
        "last_stage": last_stage,
        "stage_order": stage,
        "converted_paid": converted_paid,
        "monthly_revenue": monthly_revenue
    })

raw_df = pd.DataFrame(raw_rows)
raw_df.to_csv(
    BASE_DIR/"raw_funnel_data.csv",
    index=False
)

# ==================================================
# PRINT VERIFICATION
# ==================================================

print("=" * 60)
print("GROWTH FUNNEL DATASETS GENERATED (7-STAGE)")
print("=" * 60)

print(f"\nRaw funnel data: {len(raw_df):,} rows")
print(f"Stage distribution:")
for stage in sorted(raw_df["last_stage"].unique()):
    count = (raw_df["last_stage"] == stage).sum()
    print(f"  {stage}: {count:,}")

print(f"\nFunnel metrics: {len(funnel):,} rows")
print(f"Total visitors: {funnel['visitors'].sum():,}")
print(f"Total signups: {funnel['signups'].sum():,}")
print(f"Total onboarded: {funnel['onboarded'].sum():,}")
print(f"Total profile completed: {funnel['profile_completed'].sum():,}")
print(f"Total activated: {funnel['activated'].sum():,}")
print(f"Total trials: {funnel['trial_users'].sum():,}")
print(f"Total paid: {funnel['paid_customers'].sum():,}")

tv = funnel['visitors'].sum()
ts = funnel['signups'].sum()
to = funnel['onboarded'].sum()
tp = funnel['profile_completed'].sum()
ta = funnel['activated'].sum()
tt = funnel['trial_users'].sum()
tpa = funnel['paid_customers'].sum()

print(f"\nResume-aligned rates:")
print(f"  Signup rate (signups/visitors): {ts/tv*100:.2f}% (resume: 6.05%)")
print(f"  Trial rate (trials/signups): {tt/ts*100:.2f}% (resume: 43.86%)")
print(f"  Paid rate (paid/trials): {tpa/tt*100:.2f}% (resume: 26.25%)")
print(f"  Visitor-to-paid: {tpa/tv*100:.2f}% (resume: 0.7%)")

print(f"\nFunnel summary (7 stages):")
print(summary_df.to_string(index=False))
