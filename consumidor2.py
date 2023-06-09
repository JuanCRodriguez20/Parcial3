import json
import numpy as np
from collections import deque
import boto3

region_name = 'us-east-1'
stream_name = 'parcial3'
window_size = 20
num_std_dev = 1
kinesis = boto3.client('kinesis', region_name=region_name)
price_window = {}

def consume_bollinger():
    shard_iterator = kinesis.get_shard_iterator(
        StreamName=stream_name,
        ShardId='shardId-000000000001',
        ShardIteratorType='LATEST'
    )['ShardIterator']
    
    while True:
        response = kinesis.get_records(
            ShardIterator=shard_iterator,
            Limit=100
        )
        for record in response['Records']:
            action_data = json.loads(record['Data'])
            stock = action_data["stock"]
            price = action_data['price']

            if stock not in price_window.keys():
                price_window[stock] = deque(maxlen=window_size)
            
            price_window[stock].append(price)
            ans = check_bollinger(price_window[stock], price = price, stock = stock)
            print(ans) if ans != None else ans    
        shard_iterator = response['NextShardIterator']

def check_bollinger(price_window, price, stock):
    if len(price_window) == window_size:
        prices = np.array(price_window)
        sma = np.mean(prices)
        std = np.std(prices)
        bollinger_upper = sma + num_std_dev * std
        if price > bollinger_upper:
            return f'ALERTA: Precio de acción {stock} superó la franja superior de Bollinger (${round(bollinger_upper,2)} USD) con ${price}'
    return None

if __name__ == '__main__':
    consume_bollinger()
