Assignment 4 solution
================
Hunter GIles
3/21/2022

### setup

``` r
library(readxl)
library(jtools)
# using the "readxl" package to load the .xlsx data file
data <- read_excel("./TV.xlsx")
#View(data)
```

### Question 1

A. Estimate a quadratic regression model where the GPA of middle school
children is regressed on hours and hours-squared.

``` r
ols1 <- lm(GPA~Hours+I(Hours^2), data=data)
summary(ols1)
```

    ## 
    ## Call:
    ## lm(formula = GPA ~ Hours + I(Hours^2), data = data)
    ## 
    ## Residuals:
    ##      Min       1Q   Median       3Q      Max 
    ## -0.48261 -0.11259  0.06073  0.14251  0.43845 
    ## 
    ## Coefficients:
    ##               Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept)  3.0944928  0.2023129  15.296 7.09e-14 ***
    ## Hours        0.0409976  0.0227527   1.802 0.084141 .  
    ## I(Hours^2)  -0.0021909  0.0005725  -3.827 0.000814 ***
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 0.2323 on 24 degrees of freedom
    ## Multiple R-squared:  0.7912, Adjusted R-squared:  0.7737 
    ## F-statistic: 45.46 on 2 and 24 DF,  p-value: 6.886e-09

### Question 3

B. Find the optimal number of weekly hours of TV for middle school
children.

``` r
# retrieving the coefs from the last ols to use as numerics
beta1 <- coef(ols1)[2]
beta2 <- coef(ols1)[3]

# Formula to maximize GPA
max_hours <- beta1/(beta2*2) * -1
max_hours
```

    ##    Hours 
    ## 9.356458
