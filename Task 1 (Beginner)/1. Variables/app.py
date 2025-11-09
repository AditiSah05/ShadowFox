#1. Create a variable named pi and store the value 22/7 in it. 
# # Now check the data type of this variable.

pi = 22/7
print(f"Value of pi: {pi}")
print(f"Data type of pi: {type(pi)}")
print(f"Data type name: {type(pi).__name__}")

#2. Create a variable called for and assign it a value 4. See what happens and
# find out the reason behind the behavior that you see.

# Attempting to create a variable named 'for':
# for = 4  # This line will cause a SyntaxError!

# What happens: SyntaxError: invalid syntax
# Reason: 'for' is a reserved keyword in Python

print("\nQuestion 2 Answer:")
print("Cannot create a variable named 'for' because:")
print("1. 'for' is a reserved keyword in Python")
print("2. Reserved keywords have special meanings in the language")
print("3. They are used for control structures (for loops, if statements, etc.)")
print("4. Python prevents using them as variable names to avoid confusion")

# List of some Python reserved keywords:
import keyword
print(f"\nPython has {len(keyword.kwlist)} reserved keywords:")
print(keyword.kwlist)

#3. Store the principal amount, rate of interest, and time in different variables and 
# then calculate the Simple Interest for 3 years. 
# Formula: Simple Interest = P x R x T / 100

print("\nQuestion 3 Answer:")

# Store values in different variables
principal = 10000  # Principal amount in rupees
rate = 8.5        # Rate of interest per annum (%)
time = 3          # Time period in years

# Calculate Simple Interest using the formula: SI = (P × R × T) / 100
simple_interest = (principal * rate * time) / 100

# Calculate total amount
total_amount = principal + simple_interest

# Display the calculation
print(f"Principal Amount (P): ₹{principal}")
print(f"Rate of Interest (R): {rate}% per annum")
print(f"Time Period (T): {time} years")
print(f"Simple Interest = (P × R × T) / 100")
print(f"Simple Interest = ({principal} × {rate} × {time}) / 100")
print(f"Simple Interest = ₹{simple_interest}")
print(f"Total Amount = Principal + Simple Interest")
print(f"Total Amount = ₹{principal} + ₹{simple_interest} = ₹{total_amount}")
