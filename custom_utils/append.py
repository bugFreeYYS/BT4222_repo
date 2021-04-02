# Append newly collected data to an exisiting dataset
import pandas as pd

def append(file_name, new_rows, date, type_dataset='df'):
    if type_dataset == 'df':
        ## coindesk
        new_row = new_rows[new_rows['date'] == date]
        try: 
            pd.read_csv(file_name).append(new_row).drop_duplicates(subset=['header', 'title'], keep='last').to_csv(file_name, index=False)
        ## yahoo finance / daily data
        except:
            pd.read_csv(file_name).append(new_row).drop_duplicates(subset=['date']).to_csv(file_name, index=False)
    else:
        pass


