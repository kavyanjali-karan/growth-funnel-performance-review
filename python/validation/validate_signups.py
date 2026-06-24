def validate(df):

    assert df.signup_id.duplicated().sum()==0