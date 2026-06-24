def validate(df):

    assert df.customer_id.isnull().sum()==0