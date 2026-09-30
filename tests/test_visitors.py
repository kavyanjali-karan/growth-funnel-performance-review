def test_visitors_count(visitors):
    assert len(visitors) == 5848

def test_total_visitors_2point2m(visitors):
    assert visitors["visitors"].sum() == 2243206

def test_no_null_visitors(visitors):
    assert visitors["visitors"].isnull().sum() == 0

def test_valid_channels(visitors):
    valid = {"Organic", "Google", "LinkedIn", "Facebook", "Referral", "Email", "Direct", "Partner"}
    assert set(visitors["channel"].unique()).issubset(valid)