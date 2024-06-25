#function
def calculate_miles_per_gallon():
    # Set up variables to record the overall number of miles and gallons.
    total_miles = 0
    total_gallons = 0
    
    while True:
        gallons = float(input("Enter the gallons used (-1 to end): "))
        if gallons == -1:
            break
        miles = float(input("Enter the miles driven: "))
        
        mpg = miles / gallons
        print(f"The miles/gallon for this tank was {mpg:.6f}")
        
        # Compute the total number of miles and gallons.
        total_miles += miles
        total_gallons += gallons
        
    # After exiting the loop, calculate the overall average miles per gallon
    if total_gallons != 0:
        overall_mpg = total_miles / total_gallons
        print(f"The overall average miles/gallon was {overall_mpg:.6f}")
    else:
        print("No data to calculate overall average miles/gallon.")

# Run The calculate_miles_per_gallon
calculate_miles_per_gallon()
