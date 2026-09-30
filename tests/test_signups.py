def test_signups_exist(signups):
    assert len(signups) == 5848

def test_signups_positive(signups):
    assert (signups["signups"] >= 0).all()

def test_signup_rate_6pct(visitors, signups):
    total_visitors = visitors["visitors"].sum()
    total_signups = signups["signups"].sum()
    rate = total_signups / total_visitors * 100
    assert 5.0 < rate < 7.0  # Around 6.05%