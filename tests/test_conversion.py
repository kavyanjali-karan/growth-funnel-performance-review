def test_paid_customers_exist(paid_customers):
    assert len(paid_customers) == 5848

def test_paid_positive(paid_customers):
    assert (paid_customers["paid_customers"] >= 0).all()

def test_mrr_positive(paid_customers):
    assert (paid_customers["mrr"] >= 0).all()