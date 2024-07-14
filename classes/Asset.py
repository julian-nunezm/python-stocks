from datetime import datetime
import json

import yfinance as yf
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
#import plotly.io as pio
#pio.renderers.default = "browser"

class Asset:
    def __init__(self, ticker, start_date, end_date = datetime.today().strftime('%Y-%m-%d')):
        self.ticker_name = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.df = yf.download(self.ticker_name, start = self.start_date, end = self.end_date, progress=False)
        self.ticker = yf.Ticker(ticker)
        self.short_name = self.ticker.info.get('shortName')
        self.quote_type = self.ticker.info.get('quoteType')
        self.balance_sheet = self.ticker.balance_sheet
        self.dividends = self.ticker.dividends
        self.splits = self.ticker.splits
        
    def get_data(self):
        return self.df
    
    def get_raw_info(self):
        """Get Ticker Raw Info
        :Parameters: None
        """
        #print(type(self.ticker.info))
        print(json.dumps(self.ticker.info, indent=4))

    def get_general_info(self):
        """Get Ticker General Info
        :Parameters: None
        """
        #print(json.dumps(self.ticker.info, indent=4))
        properties = [
            'quoteType',
            'symbol',
            'shortName',
            'country',
            'sector',
            'industry',
            'fullTimeEmployees',
            'currency',
            'currentPrice',
            'totalCash',
            'totalDebt',
            'totalRevenue',
        ]
        self.general_info = {}
        
        for property in properties:
            #print(json.dumps(self.ticker.info, indent=4))
            value = self.ticker.info.get(property)
            if value:
                key = property[0].upper() + property[1:]
                self.general_info[key] = value

        return self.general_info
    
    def get_balance_sheet(self):
        #balance_sheet = self.ticker.financials
        return self.balance_sheet
    
    def get_debt_to_asset_ratio(self, latest=True):
        #print(f'Debt-to-Asset analysis:')
        # Defines how much debt a company carries compared to the value of the assets it owns.
        # Can compare one company's leverage with that of other companies in the same industry.
        # This information can reflect how financially stable a company is.
        # The higher the ratio, the higher the degree of leverage (DoL).
        # Depending on averages for the industry, there could be a higher risk of investing in that company compared to another.
        self.balance_sheet.loc['Debt-to-Asset'] = self.balance_sheet.loc['Total Debt'] / self.balance_sheet.loc['Total Assets']
        self.balance_sheet.loc['Good Debt-to-Asset'] = ((0.3 <= self.balance_sheet.loc['Debt-to-Asset']) & (self.balance_sheet.loc['Debt-to-Asset'] <= 0.6))
        df = self.balance_sheet.loc['Debt-to-Asset']
        if latest:
            currency = self.general_info.get('Currency')
            latest_debts = self.balance_sheet.loc['Total Debt'].iloc[0]
            latest_assets = self.balance_sheet.loc['Total Assets'].iloc[0]
            latest_date = df.index[0].date()
            latest_ratio = df.iloc[0]*100
            print(f"Latest Debt on {latest_date}: {latest_debts:,} {currency}")
            print(f"Latest Asset on {latest_date}: {latest_assets:,} {currency}")
            print(f"Latest Debt-to-Asset ratio on {latest_date}: {latest_ratio:,.5f}%")
            return latest_ratio
        return df
        
        #print(self.balance_sheet.loc['2023-12-31', 'Debt-to-Asset'])
        
        #print(balance_sheet.loc['Debt-to-Asset'])#, 'Total Debt', 'Total Assets'])  # To select a whole row
        #print(balance_sheet.loc['Good Debt-to-Asset'])#, 'Total Debt', 'Total Assets'])  # To select a whole row
    
    def is_stock(self):
        return self.quote_type == 'EQUITY'
    
    def is_etf(self):
        return self.quote_type == 'ETF'
