import json

from parameters import *
from classes.Asset import Asset

start_date = '2020-01-01'
tickers = [Asset(ticker, start_date) for ticker in PORTFOLIO_TICKERS]

for ticker in tickers:
    print(f'Information for {ticker}')
    general_info = ticker.get_general_info()
    print(json.dumps(general_info, indent=4))
    print('---------------')