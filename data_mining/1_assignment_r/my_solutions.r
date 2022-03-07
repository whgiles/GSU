3 + 4
(-3 + 5 + 7 + 8)/4
-3 + 5 + 7 + 8/4
variable1 <- c(-3, 5, 7, 8)
mean(variable1)
sd(variable1)

library(readr)
library(mosaic)

# getwd()
hunterData <- read_csv("gsu/data_mining/1_assignment_r/Data/treadmill.csv")
head(hunterData)
tail(hunterData)

mean(hunterData$RunTime)
sd(hunterData$RunTime)

favstats(hunterData$RunTime)

hist(hunterData$RunTime)

hist(hunterData$RunTime, labels=TRUE)

IQR <- 11.37 - 9.78
11.27 + 1.5*IQR
boxplot(hunterData$RunTime)

boxplot(hunterData$RunTime, ylab = "1.5 Mile Run Time (minutes)",
        main = "Boxplot of the Run Times of n = 31 participants")
