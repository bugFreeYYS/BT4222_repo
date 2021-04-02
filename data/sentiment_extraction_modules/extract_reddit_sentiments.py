import json
import pandas as pd
import re
import spacy
nlp = spacy.load("en_core_web_sm")
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def extract_reddit_posts_sentiments(df, date):
    analyser = SentimentIntensityAnalyzer()
    df = df.dropna()

    output = dict()

    title_counter = 0
    title_sentiment = 0

    for index, row in df.iterrows():
        title_counter = title_counter + row['comms_num']
        try:
            title_sentiment = title_sentiment + analyser.polarity_scores(row['title'])['compound'] * row['comms_num']
        except:
            continue

    body_counter = 0
    body_sentiment = 0

    for index, row in df.iterrows():
        body_counter = body_counter + row['comms_num']
        try:
            body_sentiment = body_sentiment + analyser.polarity_scores(row['body'])['compound'] * row['comms_num']
        except:
            continue

    output[date] = {
        'top_50_reddit_posts_sentiments': (0.3)*(title_sentiment/title_counter) + (0.7)*(body_sentiment/body_counter)
    }

    output = pd.DataFrame.from_dict(output).transpose()
    output['date'] = output.index
    return output


def extract_reddit_comments_sentiments(df, date):
    analyser = SentimentIntensityAnalyzer()
    df = df.dropna()

    output = dict()

    counter = 0
    sentiment = 0

    for index, row in df.iterrows():
        counter = counter + 1
        try:
            sentiment = sentiment + analyser.polarity_scores(row['comment_body'])['compound']
        except:
            continue



    output[date] = {
        'reddit_comments_sentiments': sentiment/counter
    }

    output = pd.DataFrame.from_dict(output).transpose()
    output['date'] = output.index
    return output
