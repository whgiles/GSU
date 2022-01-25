x <- "Hello World"
print(x)
print(R.version.string)

# Define the cars vector with 5 values
cars <- list(1, 3, 6, 4, 10)

# Graph the cars vector with all defaults
hist(cars)

my_func <- function(x) {
    y <- 2 * x + 1
    print("my function has been completed")
    return(y)
}
print(my_func(1))