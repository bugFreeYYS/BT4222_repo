import praw
import pandas as pd
import datetime as dt

my_client_id = 'mJ1I3LOoTVaNbw'
my_client_secret = '2FsS6tlzuzevUvsBzmUuRZcEDTgRVA'
my_user_agent = 'Bitcoin Scraping'

reddit = praw.Reddit(client_id=my_client_id, client_secret=my_client_secret, user_agent=my_user_agent)

# current utc time, supposed to be 7am sgt, an hour before the market open.
# 11pm utc time. 
now = dt.datetime.utcnow()
start = now - dt.timedelta(hours=24)

# Bitcoin subreddit
bitcoin_subreddit = reddit.subreddit('Bitcoin')

# Query keyword 
query = ['Bitcoin']

for item in query:
    post_dict = {
        'title': [],
        'score': [],
        'id': [],
        'url':[],
        'comms_num': [],
        'created': [],
        'body': []
    }

    comments_dict = {
        'comment_id': [],
        'comment_parent_id': [],
        'comment_body': [],
        'comment_link_id': [],
        'created': []
    }

    # top 100 hottest subreddit posts
    for submission in bitcoin_subreddit.hot(limit=50):
        post_dict["title"].append(submission.title)
        post_dict["score"].append(submission.score)
        post_dict["id"].append(submission.id)
        post_dict["url"].append(submission.url)
        post_dict["comms_num"].append(submission.num_comments)
        post_dict["created"].append(submission.created_utc)
        post_dict["body"].append(submission.selftext)
        
        ##### Acessing comments on the post
        submission.comments.replace_more(limit = 1)
        for comment in submission.comments.list():
            comments_dict["comment_id"].append(comment.id)
            comments_dict["comment_parent_id"].append(comment.parent_id)
            comments_dict["comment_body"].append(comment.body)
            comments_dict["comment_link_id"].append(comment.link_id)
            comments_dict["created"].append(comment.created_utc)
    
    # comments
    post_comments = pd.DataFrame(comments_dict)
    post_comments['created'] = post_comments['created'].apply(lambda x: dt.datetime.fromtimestamp(x))
    post_comments = post_comments[(post_comments['created'] > start) & (post_comments['created'] < now)]
    post_comments['date'] = post_comments['created'].apply(lambda x: x.date())
    post_comments.to_csv("./data/comments/{}.csv".format(now.date()))
    
    # posts
    post_data = pd.DataFrame(post_dict)
    post_data['created'] = post_data['created'].apply(lambda x: dt.datetime.fromtimestamp(x))
    post_data['date'] = post_data['created'].apply(lambda x: x.date())
    post_data.to_csv("./data/posts/{}.csv".format(now.date()))


