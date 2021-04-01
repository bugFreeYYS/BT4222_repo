import json
import pandas as pd
import re
import spacy
nlp = spacy.load("en_core_web_sm")
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def extract_coindesk_sentiments(df):
    df['complete_article'] = df['complete_article'].apply(lambda x: re.sub(r'^\W*\w+\W*\W*\w+\W*\W*\w+\W*', '', x))
    df['complete_article'] = df['complete_article'].apply(lambda x: re.sub(r"([A-Z])", r" \1", x))

    analyser = SentimentIntensityAnalyzer()

    def sentiment_analyzer_scores_title(title):
        result = analyser.polarity_scores(title)
        score = result['compound']
        return score

    def sentiment_analyzer_scores_body(body):
        doc = nlp(body)
        scores = []
        
        for sent in doc.sents:
            compound_sentiment = analyser.polarity_scores(str(sent))['compound']
            if abs(compound_sentiment) > 0.3:
                scores.append(compound_sentiment)
        return sum(scores)/len(scores)

    df['coindesk_body_sentiment'] = df['complete_article'].apply(lambda x: sentiment_analyzer_scores_body(x))
    df['coindesk_header_sentiment'] = df['header'].apply(lambda x: sentiment_analyzer_scores_title(x))

    body_weight = 0.7
    header_weight = 1-body_weight

    df['overall_sentiment'] = df['coindesk_body_sentiment']*body_weight + df['coindesk_header_sentiment']*header_weight
    df['num_of_coindesk_posts'] = 1

    cols = ['coindesk_sentiment', 'num_of_coindesk_posts']

    grouped_df = df.groupby('date').agg({'overall_sentiment': 'mean', 'num_of_coindesk_posts': 'sum'})
    grouped_df.columns = cols
    grouped_df = grouped_df.reset_index()
    grouped_df = grouped_df.sort_values('date')

    return grouped_df