def test_mrr_non_negative(paid_customers):
    assert (paid_customers["mrr"] >= 0).all()

def test_mrr_positive_sum(paid_customers):
    assert paid_customers["mrr"].sum() > 0

def test_trial_to_paid_rate(trials, paid_customers):
    total_trials = trials["trial_users"].sum()
    total_paid = paid_customers["paid_customers"].sum()
    rate = total_paid / total_trials * 100
    assert 20.0 < rate < 35.0  # Around 26.25%