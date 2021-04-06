library(readr)
cleaned_trainingset <- read_csv("Desktop/NUS_Y4S2/BT4222/BT4222_repo/models/classification/cleaned_trainingset.csv")
attach(cleaned_trainingset)
ncol(cleaned_trainingset)
df = cleaned_trainingset[,3:ncol(cleaned_trainingset)]

nothing = glm(`Adj_Close_BTC-USD` ~ 1, family = binomial)
fullmod = glm(`Adj_Close_BTC-USD`~.,df, family=binomial)

bothways = step(nothing, list(lower=formula(nothing), upper=formula(fullmod)), direction='both')

formula(bothways)
summary(bothways)
