def validate(df):

    assert df.trial_id.duplicated().sum()==0