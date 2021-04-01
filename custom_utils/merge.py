# inner join multiple datasets on specified columns
import pandas as pd

def merge(list_of_dfs, list_of_column=['date']):
    output = list_of_dfs[0]

    for index in range(1, len(list_of_dfs)):
        output = pd.merge(output, list_of_dfs[index], how='inner', on=list_of_column)
    
    return output.sort_values('date')