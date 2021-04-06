import pandas as pd

# by default will lag independent variable by one period
# more lags can be created by specifying in the lag_dict
# eg.
# lags = {
#     'Adj_Close_BTC-USD': 6,
#     'Open_BTC-USD': 6,
#     'Low_BTC-USD': 6,
#     'Volume_BTC-USD': 6,
#     'Adj_Close_SPY': 6,
#     'Adj_Close_GLD': 6,
# }

def get_num_lags(df, lag_dict):
    for column in list(df.columns):
        if column != 'date' and column != 'Adj_Close_BTC-USD':
            if column not in lag_dict:
                # lag by 1 period 
                df[column + '_lag_1'] = df[column].shift(1)
            else:
                for i in range(1, lag_dict[column]):
                    df[column + '_lag_' + str(i)] = df[column].shift(i)
            df = df.drop([column], axis=1)
    df = df.dropna()
    return df

def lag(data, dic):
    cols = []
    for key, value in dic.items():
        for i in range(1, value+1):
            cols.append(data[key].shift(i).rename('{}_lag{}'.format(data[key].name, i)))
    return pd.concat([data["date"],data["Adj_Close_BTC-USD"]] + cols, axis = 1)


## example
feature_lags = {"Adj_Close_BTC-USD" : 2, 
                "Volume_BTC-USD" : 1, 
                "Adj_Close_SPY" : 1,
                "Adj_Close_GLD" : 1,
                "Adj_Close_CHFUSD=X" : 1,
                "Adj_Close_CNYUSD=X" : 1,
                "Adj_Close_EURUSD=X" : 1,
                "Adj_Close_GBPUSD=X" : 1,
                "Adj_Close_JPYUSD=X" : 1,
                "blockchain_transactions_per_block" : 1,
                "blockchain_hash_rates" : 1}
                
# data = lag(data, feature_lags)
