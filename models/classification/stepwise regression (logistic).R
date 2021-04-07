library(readr)
cleaned_trainingset <- read_csv("/Users/bolin/Desktop/NUS_Y4S2/BT4222/BT4222_repo/models/classification/clean_trainingset_no_sentiment.csv")
attach(cleaned_trainingset)
ncol(cleaned_trainingset)
df = cleaned_trainingset[,1:ncol(cleaned_trainingset)-1]
View(df)

nothing = glm(`Adj_Close_BTC-USD` ~ 1, family = binomial)
fullmod = glm(`Adj_Close_BTC-USD`~.,df, family=binomial)

bothways = step(nothing, list(lower=formula(nothing), upper=formula(fullmod)), direction='both')

formula(bothways)
summary(bothways)
