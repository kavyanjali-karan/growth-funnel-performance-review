def test_retention(df):

    assert (df.retention_rate<=1).all()