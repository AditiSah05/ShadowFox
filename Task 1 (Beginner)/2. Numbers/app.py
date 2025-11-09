"""1. Write a function that takes two arguments, 145 and 'o', and uses the `format`
function to return a formatted string. Print the result. 
Try to identify the representation used."""


def format_number(number, format_type):
    return format(number, format_type)

result = format_number(145, 'o')
print(f"format(145, 'o') = {result}")
print("\nExplanation:")
print(f"The number 145 in decimal is converted to '{result}' in octal")
print("Representation used: Octal (base-8) number system")
print("'o' format specifier converts decimal to octal representation")
print(f"\nVerification: 2×8² + 2×8¹ + 1×8⁰ = 2×64 + 2×8 + 1 = 128 + 16 + 1 = 145")


"""2. In a village, there is a circular pond with a radius of 84 meters.
Calculate the area of the pond using the formula: Circle Area = π
r^2. (Use the value 3.14 for π) Bonus Question: If there is exactly
1.4 liters of water in a square meter, what is the total amount of
water in the pond? Print the answer without any decimal point in
it. Hint: Circle Area = π r^2 Water in the pond = Pond Area
Water per Square Meter"""

pi = 3.14
radius = 84
pond_area = pi * radius ** 2
water_per_sqm = 1.4
total_water = pond_area * water_per_sqm

print(f"\nPond radius: {radius} meters")
print(f"Pond area: {pond_area} square meters")
print(f"Total water in pond: {int(total_water)} liters")


"""3. If you cross a 490meterlong street in 7 minutes, calculate your
speed in meters per second. Print the answer without any decimal
point in it. Hint: Speed = Distance / Time"""

distance = 490
time_minutes = 7
time_seconds = time_minutes * 60
speed = distance / time_seconds

print(f"\nDistance: {distance} meters")
print(f"Time: {time_minutes} minutes = {time_seconds} seconds")
print(f"Speed: {int(speed)} meters per second")
