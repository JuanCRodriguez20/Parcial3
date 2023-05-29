from productor1 import get_data

def test_get_data_edge_case():
    data = get_data()
    assert 'event_time' in data
    assert 'stock' in data
    assert 'price' in data
    assert data['stock'] in ['AAPL', 'AMZN', 'MSFT', 'INTC', 'TBV']
    assert type(data['price']) == float
