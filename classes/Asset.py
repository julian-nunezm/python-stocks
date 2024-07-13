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
        self.ticker = yf.Ticker(ticker)
        self.start_date = start_date
        self.end_date = end_date
        self.df = self.get_data()
        
    def get_data(self):
        print(self.ticker)
        df = yf.download(self.ticker_name, start = self.start_date, end = self.end_date)
        return df
    
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
            'shortName',
            'country',
            'sector',
            'fullTimeEmployees',
            'currency',
            'currentPrice',
            'totalCash',
            'totalDebt',
            'totalRevenue',
        ]
        self.general_info = {}
        
        for property in properties:
            value = self.ticker.info.get(property)
            if value:
                self.general_info[property.title()] = value

        #self.general_info = {
        #    'ShortName': self.ticker.info.get('shortName'),
        #    'Country': self.ticker.info.get('country'),
        #    'Sector': self.ticker.info.get('sector'),
        #    'FullTimeEmployees': f"{self.ticker.info.get('fullTimeEmployees'):,}",
        #    'Currency': self.ticker.info.get('currency'),
        #    'CurrentPrice': self.ticker.info.get('currentPrice'),
        #    'TotalCash': f"{self.ticker.info.get('totalCash'):,}",
        #    'TotalDebt': f"{self.ticker.info.get('totalDebt'):,}",
        #    'TotalRevenue': f"{self.ticker.info.get('totalRevenue'):,}",
        #}
        return self.general_info
    
    def get_balance_sheet(self):
        #balance_sheet = self.ticker.financials
        balance_sheet = self.ticker.balancesheet
        return balance_sheet
    
    