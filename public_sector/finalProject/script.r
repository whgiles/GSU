library(haven)
library(tidyverse)
library(broom)
library(psych)
library(estimatr)
options(tibble.print_max = Inf)


data <- read_dta("/Users/williamgiles/gsu/public/finalProject/Marijuana/data/first_do_file_2001-2021_for_marijuana.dta") %>% rename(X_ageg5yr = `_ageg5yr`)
# sample_data <- data[sample(nrow(data),100000),]
# write.csv(sample_data, "/Users/williamgiles/gsu/public/finalProject/Marijuana/data/sample_data.csv", row.names = FALSE)

#data <- read.csv("/Users/williamgiles/gsu/public/finalProject/Marijuana/data/sample_data.csv") %>% select(-post) 

# _EDUCAG, IYEAR, _STATE

data <- data %>% 
  mutate(post = 0)
data <- data %>%
  mutate(post = ifelse(year > 2012,1,0))
data <- data %>% 
  mutate(post = ifelse(state == 8 & year < 2012, 0, post)) %>%
  mutate(post = ifelse(state == 53 & year < 2012, 0, post)) %>%
  mutate(post = ifelse(state == 2 & year < 2014, 0, post)) %>%
  mutate(post = ifelse(state == 4 & year < 2020, 0, post)) %>%
  mutate(post = ifelse(state == 6 & year < 2016, 0, post)) %>%
  mutate(post = ifelse(state == 9 & year < 2021, 0, post)) %>%
  mutate(post = ifelse(state == 17 & year < 2019, 0, post)) %>%
  mutate(post = ifelse(state == 23 & year < 2016, 0, post)) %>%
  mutate(post = ifelse(state == 24 & year < 2022, 0, post)) %>%
  mutate(post = ifelse(state == 25 & year < 2016, 0, post)) %>%
  mutate(post = ifelse(state == 26 & year < 2018, 0, post)) %>%
  mutate(post = ifelse(state == 29 & year < 2022, 0, post)) %>%
  mutate(post = ifelse(state == 30 & year < 2020, 0, post)) %>%
  mutate(post = ifelse(state == 32 & year < 2016, 0, post)) %>%
  mutate(post = ifelse(state == 34 & year < 2020, 0, post)) %>%
  mutate(post = ifelse(state == 35 & year < 2021, 0, post)) %>%
  mutate(post = ifelse(state == 36 & year < 2021, 0, post)) %>%
  mutate(post = ifelse(state == 41 & year < 2014, 0, post)) %>%
  mutate(post = ifelse(state == 44 & year < 2022, 0, post)) %>%
  mutate(post = ifelse(state == 50 & year < 2020, 0, post)) %>%
  mutate(post = ifelse(state == 51 & year < 2021, 0, post)) %>%
  mutate(post = as.factor(post))

data <- data %>%
  mutate(marijuana = state %in% c(8,53,2,4,6,9,17,23,24,25,26,29,30,32,34,35,36,41,44,50,51)) %>%
  mutate(marijuana = as.factor(marijuana))

data <- data %>% 
  mutate(hsgrad = ifelse(hsgrad == 1 | somecol == 1 | colgrad == 1, 1, 0))

data <- data %>% select(marijuana, hsgrad, post, hispanic, white, black, asian, hawaiinorpi, 
                        americanindianoral,  X_ageg5yr, married, inc_cat, 
                        hhsize, year, state) %>% na.omit()

# write_csv(data, "/Users/williamgiles/gsu/public/finalProject/Marijuana/data/scomplete_clean_.csv", row.names = FALSE)
#-------------------------------------------DD------------------------------->

model <- lm(hsgrad ~ marijuana*post + hispanic + white + black + asian + 
              hawaiinorpi + americanindianoral + X_ageg5yr +
              married + inc_cat + hhsize,
           data = filter(data,inc_cat < 5))
tidy(model)

#---------------------------------------------IPW------------------------------->
ipw.data <- filter(data, post == 1) %>% 
  mutate(marijuana = ifelse(marijuana == TRUE,1,0))
dim(data)
ipw.stage1 <- glm(marijuana ~ hispanic + white + black + asian + hawaiinorpi + 
                    americanindianoral +  X_ageg5yr + married + inc_cat + hhsize + factor(year) + factor(state),
                  data = ipw.data,
                  family = binomial("logit"))
ipw.data <- augment_columns(ipw.stage1,
                    ipw.data,
                    type.predict = "response") %>%
  mutate(weight = (marijuana / .fitted) + ((1-marijuana)/(1-.fitted)))

ipw.model <- lm(hsgrad ~ marijuana,
                data = ipw.data,
                weights = weight)
tidy(ipw.model)

#----------------------------Parallel Trends Graph------------------------------>
parellel_data <- data %>% 
  group_by(marijuana, year) %>%
  summarize(avg_hsgrad = mean(hsgrad))


ggplot(data = parellel_data) +
  geom_point(aes(year,avg_hsgrad, color = marijuana)) +
  geom_line(aes(year,avg_hsgrad, color = marijuana)) +
  geom_vline(xintercept = 2013) +
  labs(y = "HS Graduation Rate", x = "Year", title = "HS Graduation Rate (2001 - 2022)")
  

#------------------------Naive------------------------------------------------->

naive_model <- lm(hsgrad ~ marijuana,
                  data = ipw.data)
tidy(naive_model)


#------------------Model Summary----------------------------------------------->
modelsummary::modelsummary(list(
  "DD" = model,
  "Naive" = naive_model,
  "IPW" = ipw.model
), coef_rename = c("marijuanaTRUE" = "marijuana", "post1" = "Post", "marijuanaTRUE:post1" = "marijuana X post"),
coef_omit = c("hispanic|white|black|asain|hawaiinorpi|americanindianoral|X_ageg5yr|married|inc_cat|hhsize|asian"),
title = "Regression Output")


#----------------------Data Table---------------------------------------------->
library(psych)
library(htmlTable)
data$inc8 <- ifelse(data$inc_cat >= 8, 1, 0)
data$age8 <- ifelse(data$X_ageg5yr >= 8, 1, 0)
data.1 <- data %>% select(-state, hispanic, white, black, asian, hawaiinorpi, 
                            americanindianoral, X_ageg5yr, married, hhsize, post, marijuana, age1, age2, age3, age4, age5, age6, age7, age8, inc1, inc2, inc3, inc4, inc5, inc6, inc7, inc8)
#create summary table
before_co <- filter(data.1, post == 0, marijuana == FALSE)
before_tr <- filter(data.1, post == 0, marijuana == TRUE)
after_co <- filter(data.1, post == 1, marijuana == FALSE)
after_tr <- filter(data.1, post == 1, marijuana == TRUE)

summary_data <- cbind(describe(before_co) %>% select(mean),
                      describe(before_tr) %>%  select(mean),
                      describe(after_co) %>%  select(mean),
                      describe(after_tr) %>% select(mean)) 
summary_data <- summary_data[c(-1,-3),]
summary_data <- round(summary_data,4)
colnames(summary_data) <- c("pretreament non-legalization", "pretreatment legalization", "posttreatment non-legalization", "posttreatment legalization")
dim(before_co)
dim(before_tr)
dim(after_co)
dim(after_tr)
summary_data %>% htmlTable(caption = "Summary Data", tfoot = "N = {2,136,120 |  2,396,506  |  1,827,044 | 519,826}")




