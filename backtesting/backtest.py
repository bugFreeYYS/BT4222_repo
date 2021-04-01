from datetime import datetime, timedelta
import pandas as pd
import numpy as np


def backtest_classification_noSentiment(y_pre, # up --> 1, down --> -1
                                        date, 
                                        filename = str(int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()))): 
    # init a log file
    file = open(filename,'w')
    
    # read in data
    data = pd.read_csv("../data/bitcoin_price.csv")
    # convert to datetime
    data["Date"] = pd.to_datetime(data["Date"])
    # subset data set
    data = data[data["Date"].isin(date)]

    open_p, close_p = data["24h Open (USD)"].tolist(), data["Closing Price (USD)"].tolist()  
    
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
    
    return portfolio[1:]


def backtest_regression_noSentiment(y_pre, 
                                    date
                                    filename = str(int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()))):
    # init a log file
    file = open(filename,'w')
    
    # read in data
    data = pd.read_csv("../data/bitcoin_price.csv")
    # convert to datetime
    data["Date"] = pd.to_datetime(data["Date"])
    # subset data set
    data = data[data["Date"].isin(
        [date[0]- timedelta(days=1),] + date) # add in the previous day to obtain previous close information
                   ]
    # append predicted value to be na for the previous day
    data["predicted"] = [np.nan, ] + y_pre
    
    
    extended_date, predicted = data["Date"].tolist(), data["predicted"].tolist()
    open_p, close_p = data["24h Open (USD)"].tolist(), data["Closing Price (USD)"].tolist()
    high, low = data["24h High (USD)"].tolist(), data["24h Low (USD)"].tolist()
    
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
            
    return portfolio[1:]