from consumidor2 import check_bollinger
from collections import deque

def test_bollinger_within_bands():
    price_window = deque([10, 12, 15, 13, 11, 9, 8, 10, 12, 14, 16, 18, 20, 18, 16, 14, 12, 10, 8, 6])
    price = 12
    stock = "AAPL"
    assert check_bollinger(price_window, price, stock) == None