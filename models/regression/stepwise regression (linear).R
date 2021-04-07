library(readr)
cleaned_trainingset <- read_csv("/Users/bolin/Desktop/NUS_Y4S2/BT4222/BT4222_repo/models/regression/clean_trainingset.csv")
attach(cleaned_trainingset)
ncol(cleaned_trainingset)
df = cleaned_trainingset[,2:ncol(cleaned_trainingset)]
View(df)

nothing = lm(`Adj_Close_BTC-USD` ~ 1)
fullmod = lm(`Adj_Close_BTC-USD`~.,df)

bothways = step(nothing, list(lower=formula(nothing), upper=formula(fullmod)), direction='both')

formula(bothways)
summary(bothways)

