# conduct data collection and sentiment extraction
# append raw rows to the respective datasets in the raw folder
# append combined rows to the cooked folder
from config import config
import datetime

# data collection
from data_collection_modules import get_coindesk_data
from data_collection_modules import get_yahoo_finance_data
from data_collection_modules import get_reddit_data

import sys
sys.path.insert(1, '/Users/bolin/Desktop/NUS_Y4S2/BT4222/project_submission')
from custom_utils import *

end = str(datetime.datetime.now().date())
start = str((datetime.datetime.now() - datetime.timedelta(days=1)).date())

# yahoo finance data
yahoo_finance_data = get_yahoo_finance_data(start, end)
try:
    append(config['raw_dir']+config['raw_yahoo_finance_file_name'], yahoo_finance_data)
except:
    yahoo_finance_data.to_csv(config['raw_dir']+config['raw_yahoo_finance_file_name'])


# coin desk data
coin_desk_data = get_coindesk_data()


# reddit posts and comments data
reddit_comments_data, reddit_posts_data = get_reddit_data()

# sentiment extraction



# joining datasets