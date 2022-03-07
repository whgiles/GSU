R Assignment 2
================
W Hunter Giles
2022-02-21

1.  Import the **Demographics** data file (csv format) into a data frame
    (table) and label it myData. Keep in mind that The R language is
    case sensitive.

``` r
# Replace Your with your name and " " with your file location. 

myData <- read.csv("./data/Demographics.csv")

# View(myData)
```

2.  Count the number of males and females in the data.

``` r
length(which(myData$Sex=='M'))
```

    ## [1] 508

``` r
length(which(myData$Sex=='F'))
```

    ## [1] 382

3.  What percentages of males and females are married?

``` r
length(which(myData$Sex=='M' & myData$Married=='Y'))/length(which(myData$Sex=='M'))
```

    ## [1] 0.6614173

``` r
length(which(myData$Sex=='F' & myData$Married=='Y'))/length(which(myData$Sex=='F'))
```

    ## [1] 0.6492147

4.  Of the 10 individuals with the highest income, how many are married
    males.

``` r
df2 <- myData[order(-myData$Income),]
df2 <- df2[1:10,]
length(which(df2$Married=='Y' & df2$Sex=='M'))
```

    ## [1] 7

5.  What are the highest and the lowest incomes of males and females?

``` r
library(dplyr)
# lowest and highest income for males:
min(filter(myData, myData$Sex=='M')$Income)
```

    ## [1] 35

``` r
max(filter(myData, myData$Sex=='M')$Income)
```

    ## [1] 147

``` r
# lowest and highest income for females
min(filter(myData, myData$Sex=='F')$Income)
```

    ## [1] 22

``` r
max(filter(myData, myData$Sex=='F')$Income)
```

    ## [1] 138

6.  What are the highest and lowest incomes of married and unmarried
    males?

``` r
# "lowest and highest income for Unmarried males:"
min(filter(myData, Sex=='M', Married=='N')$Income)
```

    ## [1] 39

``` r
max(filter(myData, Sex=='M', Married=='N')$Income)
```

    ## [1] 140

``` r
# lowest and highest income for married males:
min(filter(myData, Sex=='M', Married=='Y')$Income)
```

    ## [1] 35

``` r
max(filter(myData, Sex=='M', Married=='Y')$Income)
```

    ## [1] 147
