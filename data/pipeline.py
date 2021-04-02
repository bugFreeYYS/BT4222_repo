# conduct data collection and sentiment extraction
# append raw rows to the respective datasets in the raw folder
# append combined rows to the cooked folder
from config import config
import datetime

#######################
### data collection ###
#######################

from data_collection_modules import get_coindesk_data
from data_collection_modules import get_yahoo_finance_data
from data_collection_modules import get_reddit_data

from sentiment_extraction_modules import *

import sys
sys.path.insert(1, '/Users/bolin/Desktop/NUS_Y4S2/BT4222/BT4222_repo')
from custom_utils import *

end = str(datetime.datetime.now().date())
start = str((datetime.datetime.now() - datetime.timedelta(days=1)).date())

# yahoo finance data
yahoo_finance_data = get_yahoo_finance_data(start, end)
try:
    append(config['raw_dir']+config['raw_yahoo_finance_file_name'], yahoo_finance_data, start)
except:
    yahoo_finance_data.to_csv(config['raw_dir']+config['raw_yahoo_finance_file_name'])


# coin desk data
coin_desk_data = get_coindesk_data()
try:
    append(config['raw_dir']+config['raw_coindesk_file_name'], coin_desk_data, start)
except:
    coin_desk_data.to_csv(config['raw_dir']+config['raw_coindesk_file_name'])

# reddit posts and comments data
reddit_comments_data, reddit_posts_data = get_reddit_data()
date_version = str((datetime.datetime.now() - datetime.timedelta(days=1)).date())
reddit_comments_data.to_csv("/Users/bolin/Desktop/NUS_Y4S2/BT4222/BT4222_repo/data/raw_data/raw_reddit_df/Comments/{}.csv".format(date_version))
reddit_posts_data.to_csv("/Users/bolin/Desktop/NUS_Y4S2/BT4222/BT4222_repo/data/raw_data/raw_reddit_df/Posts/{}.csv".format(date_version))


##########################
## sentiment extraction ##
##########################

coindesk_sentiments = extract_coindesk_sentiments(coin_desk_data)
reddit_comments_sentiments = extract_reddit_comments_sentiments(reddit_comments_data, str(start))
reddit_posts_sentiments = extract_reddit_posts_sentiments(reddit_posts_data, str(start))


###########################
#### joining datasets #####
###########################
cleaned_df = merge([yahoo_finance_data, coindesk_sentiments, reddit_comments_sentiments, reddit_posts_sentiments])
try:
    append(config['cooked_dir']+config['cooked_data_file_name'], cleaned_df, start)
except:
    cleaned_df.to_csv(config['cooked_dir']+config['cooked_data_file_name'])
