import pandas as pd
import numpy as np

# by default, log return transformation will be applied to all columns
# unless a list of custom columns are provided
def log_return_transformation(df, columns='all'):
    if columns == 'all':
        for column in list(df.columns):
            if column != 'date':
                # log rate of change
                df[column] = np.log(df[column]/df[column].shift(1))
    else:
        for column in columns:
                df[column] = np.log(df[column]/df[column].shift(1))

    df = df.dropna()
    return df