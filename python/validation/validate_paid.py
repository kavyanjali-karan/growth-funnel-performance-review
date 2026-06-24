def validate(df):

    assert (df.subscription_amount>=0).all()