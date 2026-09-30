def test_all_datasets_exist():
    from pathlib import Path
    data_dir = Path(__file__).resolve().parents[1] / "data" / "raw"
    required = ["visitors.csv", "signups.csv", "trials.csv", "paid_customers.csv"]
    for f in required:
        assert (data_dir / f).exists(), f"Missing {f}"

def test_funnel_completeness(visitors, signups, trials, paid_customers):
    v = visitors["visitors"].sum()
    s = signups["signups"].sum()
    t = trials["trial_users"].sum()
    p = paid_customers["paid_customers"].sum()
    assert v > s > t > p  # Funnel should decrease at each stage