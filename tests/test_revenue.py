def test_revenue(df):

    assert (df.revenue>=0).all()