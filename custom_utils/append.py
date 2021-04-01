# Append newly collected data to an exisiting dataset
import pandas as pd

def append(file_name, new_rows, type_dataset='df'):
    if type_dataset == 'df':
        pd.read_csv(file_name).append(new_rows).drop_duplicates().to_csv(file_name, index=False)
    else:
        pass


