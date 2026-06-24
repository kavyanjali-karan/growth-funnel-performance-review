def test_conversion(df):

    assert (df.paid_conversion>=0).all()