import statistics

# Data in question
infection_covid_data = [174, 335, 278, 214, 422, 513, 737, 672, 489, 412, 1301, 1105, 1123, 1376, 1502, 894, 665, 1704, 1656, 1342]

#calculations
minimum_value = min(infection_covid_data)
maximum_value = max(infection_covid_data)
range_infection = maximum_value - minimum_value
mean = statistics.mean(infection_covid_data)
median = statistics.median(infection_covid_data)
variance = statistics.variance(infection_covid_data)
std_deviation = statistics.stdev(infection_covid_data)

# Show the Result
print("COVID-19 Infection Statistics")
print(f"data: {infection_covid_data}")
print()
print("Result:")
print()
print(f"Minimum: {minimum_value}")
print(f"Maximum: {maximum_value}")
print(f"Range: {range_infection}")
print(f"Mean: {mean:.6f}")
print(f"Median: {median:.6f}")
print(f"Variance: {variance:.6f}")
print(f"Standard Deviation: {std_deviation:.6f}")
