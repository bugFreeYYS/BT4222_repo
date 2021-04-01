import yfinance as yf
yf.pdr_override()
import pandas as pd
import datetime

def get_yahoo_finance_data(start_date, end_date, tickers=["BTC-USD", "SPY", "GLD", "CHFUSD=X", "EURUSD=X", "GBPUSD=X", "JPYUSD=X", "CNYUSD=X"]): 
    # downloading data 
    data_df = yf.download(tickers, start=start_date, end=end_date)

    df = data_df[[('Adj Close',  'BTC-USD'),
                  ('Open', 'BTC-USD'),
                  ('High', 'BTC-USD'),
                  ('Low', 'BTC-USD'),
                  ('Volume', 'BTC-USD'),
                  ('Adj Close', 'SPY'),
                ('Adj Close', "GLD"),
                ('Adj Close', 'CHFUSD=X'),
                ('Adj Close', 'CNYUSD=X'),
                ('Adj Close', 'EURUSD=X'),
                ('Adj Close', 'GBPUSD=X'),
                ('Adj Close', 'JPYUSD=X')
                 ]]

    df.columns = map(lambda x: x.replace(' ', '_'), map(lambda x: x[0] + ' ' + x[1], list(df.columns)))
    df['date'] = list(map(lambda x: str(x.date()), df.index))    
    df = df.fillna(method='ffill')
    return df