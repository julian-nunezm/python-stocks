from typing import cast

from parameters import *
from handy_functions import *
from classes.Asset import Asset

start_date = '2020-01-01'
for group in TICKERS.keys():
    print(f'\n{group.upper()} TICKERS: {len(TICKERS[group])}\n')
    tickers = [Asset(ticker, start_date) for ticker in TICKERS[group]]
    # Organise stocks by sector
    tickers_by_sector = organise_tickers_by_sector(tickers)
    #print_as_json(tickers_by_sector)

    for sector in tickers_by_sector.keys():
        for industry in tickers_by_sector[sector].keys():
            print('------------------------------------------------------------')
            print(f'-> Sector: {sector}')
            print(f'   Industry: {industry}')
            print('------------------------------------------------------------')
            for ticker in tickers_by_sector[sector][industry]:
                ticker = cast(Asset,ticker)
                print(f'- Information for {ticker.ticker_name} ({ticker.short_name})')
                general_info = ticker.get_general_info()
                #print_as_json(general_info)
                if ticker.is_stock():
                    df = ticker.get_data()
                    #print(df)
                    debt_to_asset_ratio = ticker.get_debt_to_asset_ratio(latest=True)

    #print(tickers[0].__dict__)
    #print_as_json(tickers[0].ticker.info)
    #df = tickers[0].get_balance_sheet()
    #print(df)