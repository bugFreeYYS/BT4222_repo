import datetime
from datetime import timedelta
import pandas as pd
import numpy as np


def backtest_classification_noSentiment(y_pre, # up --> 1, down --> -1
                                        date, 
                                        filename): 
    # init a log file
    file = open(filename,'w')
    
    # read in data
    data = pd.read_csv("./data/cooked_data/cooked_complete_dataset.csv")
    # convert to datetime
    data['date'] = data['date'].apply(lambda x: datetime.datetime.strptime(x, "%d/%m/%y"))
    data["date"] = pd.to_datetime(data["date"], format='%d/%m/%Y', infer_datetime_format=True)
    # subset data set
    data = data[data["date"].isin(date)]

    open_p, close_p = data["Open_BTC-USD"].tolist(), data["Adj_Close_BTC-USD"].tolist()
    
    # init portfolio at 1
    portfolio = [1,]
    
    # loop every day
    for i in range(len(date)):
        file.write("---------------------------------------------\n")
        file.write(str(date[i]) + "\n")
        pre, open_price, close_price = y_pre[i], open_p[i], close_p[i]
        # if predicted up
        if pre == 1: # strategy --> buy at open, sell at close
            file.write("Predicted price UP, LONG {} at open and SELL {} at close.\n".format("100%", "100%"))
            percentage = (close_price - open_price) / open_price
            new_portfolio = portfolio[-1] * (1 + percentage)
            portfolio.append(new_portfolio)
            file.write("Percentage return is {} and the new portfolio is {}.\n".format(
                round(percentage, 2), round(new_portfolio,2)))

        # if predicted down
        else: # strategy --> short at open, cover at close
            file.write("Predicted price DOWN, SHORT {} at open and COVER {} at close.\n".format("100%", "100%"))
            percentage = (open_price - close_price) / open_price
            new_portfolio = portfolio[-1] * (1 + percentage)
            portfolio.append(new_portfolio)
            file.write("Percentage return is {} and the new portfolio is {}.\n".format(
                round(percentage,2), round(new_portfolio,2)))
    
    return portfolio[:]


def backtest_regression_noSentiment(y_pre, 
                                    date,
                                    filename):
    # init a log file
    file = open(filename,'w')
    
    # read in data
    data = pd.read_csv("./data/cooked_data/cooked_complete_dataset.csv")
    # convert to datetime
    data['date'] = data['date'].apply(lambda x: datetime.datetime.strptime(x, "%d/%m/%y"))
    data["date"] = pd.to_datetime(data["date"], format='%d/%m/%Y', infer_datetime_format=True)
    # subset data set
    data = data[data["date"].isin(
        [date[0]- timedelta(days=1),] + date) # add in the previous day to obtain previous close information
                   ]
    # append predicted value to be na for the previous day
    data["predicted"] = [np.nan, ] + y_pre
    
    
    extended_date, predicted = data["date"].tolist(), data["predicted"].tolist()
    open_p, close_p = data["Open_BTC-USD"].tolist(), data["Adj_Close_BTC-USD"].tolist()
    high, low = data["High_BTC-USD"].tolist(), data["Low_BTC-USD"].tolist()
    
    # init portfolio at 1
    portfolio = [1,]
    
    # loop every day
    for i in range(len(extended_date)):
        if i == 0: # day 0 is added to obtain day 0 close price
            continue
        file.write("---------------------------------------------\n")
        file.write(str(extended_date[i]) + "\n")
        
        pre = predicted[i]
        open_price, close_price = open_p[i], close_p[i]
        high_price, low_price = high[i], low[i]

        # if the predicted price higher than the previous close --> long position
        if pre > close_p[i-1]:
            file.write("Predicted price {} is higher than the previous close {}, LONG {}.\n".format(
                round(pre,2), round(close_p[i-1],2), "100%"))
            
            # strategy --> buy at open, sell on hit or at close
            if pre <= high_price: # on hit
                file.write("Price movement hits the predicted price, SELL 100% on hit {}.\n".format(round(pre,2)))

                percentage = (pre - open_price) / open_price
                new_portfolio = portfolio[-1] * (1 + percentage)
                portfolio.append(new_portfolio)

                file.write("Percentage return is {} and the new portfolio is {}.\n".format(
                    round(percentage,2), round(new_portfolio,2)))
                
            else: # at close
                file.write("Price movement does not hit the predicted price, SELL 100% at close {}.\n".format(
                    round(close_price,2)))

                percentage = (close_price - open_price) / open_price
                new_portfolio = portfolio[-1] * (1 + percentage)
                portfolio.append(new_portfolio)
                
                file.write("Percentage return is {} and the new portfolio is {}.\n".format(
                    round(percentage,2), round(new_portfolio,2)))

        # if the predicted price lower than the previous close --> short position
        elif pre < close_p[i-1]:
            file.write("Predicted price {} is lower than the previous close {}, SHORT {}.\n".format(
                round(pre,2), close_p[i-1], "100%"))
            
            # strategy --> short at open, cover on hit or at close
            if pre >= low_price: # on hit
                file.write("Price movement hits the predicted price, COVER 100% on hit {}.\n".format(round(pre,2)))

                percentage = (open_price - pre) / open_price
                new_portfolio = portfolio[-1] * (1 + percentage)
                portfolio.append(new_portfolio)

                file.write("Percentage return is {} and the new portfolio is {}.\n".format(
                    round(percentage,2), round(new_portfolio,2)))
            else: # at close
                file.write("Price movement does not hit the predicted price, SELL 100% at close {}.\n".format(
                    round(close_price,2)))

                percentage = (open_price - close_price) / open_price
                new_portfolio = portfolio[-1] * (1 + percentage)
                portfolio.append(new_portfolio)

                file.write("Percentage return is {} and the new portfolio is {}.\n".format(
                    round(percentage,2), round(new_portfolio,2)))
        else:
            file.write("Predicted price {} is same as the previous close {}, NO ACTION.\n".format(
                round(pre,2), round(close_p[i-1],2)))
            
    return portfolio[:]



def backtest_regression_WithSentiment(y_pre, 
                                    date, sentiments,
                                    filename):
    
    # init a log file
    file = open(filename,'w')
    
    # read in data
    data = pd.read_csv("./data/cooked_data/cooked_complete_dataset.csv")
    # convert to datetime
    data['date'] = data['date'].apply(lambda x: datetime.datetime.strptime(x, "%d/%m/%y"))
    data["date"] = pd.to_datetime(data["date"], format='%d/%m/%Y', infer_datetime_format=True)
    # subset data set
    data = data[data["date"].isin(
        [date[0]- timedelta(days=1),] + date) # add in the previous day to obtain previous close information
                   ]
    # append predicted value to be na for the previous day
    data["predicted"] = [np.nan, ] + y_pre
    sentiments = [np.nan, ] + sentiments
    
    
    extended_date, predicted = data["date"].tolist(), data["predicted"].tolist()
    open_p, close_p = data["Open_BTC-USD"].tolist(), data["Adj_Close_BTC-USD"].tolist()
    high, low = data["High_BTC-USD"].tolist(), data["Low_BTC-USD"].tolist()
    
    # init portfolio at 1
    portfolio = [1,]
    
    # loop every day
    for i in range(len(extended_date)):
        if i == 0: # day 0 is added to obtain day 0 close price
            continue
        file.write("---------------------------------------------\n")
        file.write(str(extended_date[i]) + "\n")
        
        pre = predicted[i]
        open_price, close_price = open_p[i], close_p[i]
        high_price, low_price = high[i], low[i]
        sentiment = sentiments[i]

        # if the predicted price higher than the previous close --> long position
        if pre > close_p[i-1]:
            if sentiment == "positive":
                p = 0.8
            else:
                p = 0.4
                
            file.write("Predicted price {} is higher than the previous close {}, LONG {}.\n".format(
                round(pre,2), round(close_p[i-1],2), str(p*100) + "%"))
            
            # strategy --> buy at open, sell on hit or at close
            if pre <= high_price: # on hit
                file.write("Price movement hits the predicted price, SELL 100% on hit {}.\n".format(round(pre,2)))

                percentage = (pre - open_price) / open_price
                new_portfolio = portfolio[-1] * (1-p) + portfolio[-1] * p * (1+percentage)
                portfolio.append(new_portfolio)

                file.write("Percentage return is {} and the new portfolio is {}.\n".format(
                    round(percentage,2), round(new_portfolio,2)))
                
            else: # at close
                file.write("Price movement does not hit the predicted price, SELL 100% at close {}.\n".format(
                    round(close_price,2)))

                percentage = (close_price - open_price) / open_price
                new_portfolio = portfolio[-1] * (1-p) + portfolio[-1] * p * (1+percentage)
                portfolio.append(new_portfolio)
                
                file.write("Percentage return is {} and the new portfolio is {}.\n".format(
                    round(percentage,2), round(new_portfolio,2)))

        # if the predicted price lower than the previous close --> short position
        elif pre < close_p[i-1]:
            if sentiment == "positive":
                p = 0.3
            else:
                p = 0.6
            file.write("Predicted price {} is lower than the previous close {}, SHORT {}.\n".format(
                round(pre,2), close_p[i-1], str(p*100) + "%"))
            
            # strategy --> short at open, cover on hit or at close
            if pre >= low_price: # on hit
                file.write("Price movement hits the predicted price, COVER 100% on hit {}.\n".format(round(pre,2)))

                percentage = (open_price - pre) / open_price
                new_portfolio = new_portfolio = portfolio[-1] * (1-p) + portfolio[-1] * p * (1+percentage)
                portfolio.append(new_portfolio)
                file.write("Percentage return is {} and the new portfolio is {}.\n".format(
                    round(percentage,2), round(new_portfolio,2)))
            else: # at close
                file.write("Price movement does not hit the predicted price, SELL 100% at close {}.\n".format(
                    round(close_price,2)))

                percentage = (open_price - close_price) / open_price
                new_portfolio = new_portfolio = portfolio[-1] * (1-p) + portfolio[-1] * p * (1+percentage)
                portfolio.append(new_portfolio)

                file.write("Percentage return is {} and the new portfolio is {}.\n".format(
                    round(percentage,2), round(new_portfolio,2)))
        else:
            file.write("Predicted price {} is same as the previous close {}, NO ACTION.\n".format(
                round(pre,2), round(close_p[i-1],2)))
            
    return portfolio[:]

def backtest_classification_WithSentiment(y_pre, # up --> 1, down --> -1
                                        date, sentiments,
                                        filename): 
    # init a log file
    file = open(filename,'w')
    
    # read in data
    data = pd.read_csv("./data/cooked_data/cooked_complete_dataset.csv")
    # convert to datetime
    data['date'] = data['date'].apply(lambda x: datetime.datetime.strptime(x, "%d/%m/%y"))
    data["date"] = pd.to_datetime(data["date"], format='%d/%m/%Y', infer_datetime_format=True)
    # subset data set
    data = data[data["date"].isin(date)]

    open_p, close_p = data["Open_BTC-USD"].tolist(), data["Adj_Close_BTC-USD"].tolist()
    
    # init portfolio at 1
    portfolio = [1,]
    
    # loop every day
    for i in range(len(date)):
        file.write("---------------------------------------------\n")
        file.write(str(date[i]) + "\n")
        pre, open_price, close_price, sentiment = y_pre[i], open_p[i], close_p[i], sentiments[i]
        # if predicted up
        if pre == 1: # strategy --> buy at open, sell at close
            if sentiment == "positive":
                p = 0.8
            else:
                p = 0.4
            file.write("Predicted price UP, LONG {} at open and SELL {} at close.\n".format(str(p*100) + "%", str(p*100) + "%"))
            percentage = (close_price - open_price) / open_price
            new_portfolio = portfolio[-1] * (1-p) + portfolio[-1] * p * (1+percentage)
            portfolio.append(new_portfolio)
            file.write("Percentage return is {} and the new portfolio is {}.\n".format(
                round(percentage, 2), round(new_portfolio,2)))

        # if predicted down
        else: # strategy --> short at open, cover at close
            if sentiment == "positive":
                p = 0.3
            else:
                p = 0.6
            file.write("Predicted price DOWN, SHORT {} at open and COVER {} at close.\n".format(str(p*100) + "%", str(p*100) + "%"))
            percentage = (open_price - close_price) / open_price
            new_portfolio = portfolio[-1] * (1-p) + portfolio[-1] * p * (1+percentage)
            portfolio.append(new_portfolio)
            file.write("Percentage return is {} and the new portfolio is {}.\n".format(
                round(percentage,2), round(new_portfolio,2)))
    
    return portfolio[:]