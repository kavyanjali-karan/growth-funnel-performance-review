def test_activated_exist(activated):
    assert len(activated) == 5848

def test_activated_positive(activated):
    assert (activated["activated"] >= 0).all()

def test_signup_to_trial_rate(signups, trials):
    total_signups = signups["signups"].sum()
    total_trials = trials["trial_users"].sum()
    rate = total_trials / total_signups * 100
    assert 35.0 < rate < 55.0  # Around 43.86%