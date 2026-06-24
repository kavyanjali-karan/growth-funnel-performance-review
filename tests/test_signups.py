def test_signups(df):

    assert df.signup_id.duplicated().sum()==0