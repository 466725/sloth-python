# https://www.bilibili.com/video/BV1wD4y1o7AS?spm_id_from=333.788.videopod.episodes&vd_source=a33df226c383c8e97ad19eb98bbbdc8b&p=125
# Define a circle class
class Circle:
    def __init__(self, radius, pie=3.14):
        self.radius = radius
        self.pie = pie

    def __str__(self):
        return f"Circle with radius {self.radius} and pie {self.pie}"

    def area(self):
        return round(pow(self.radius, 2) * self.pie, 2)

    def perimeter(self):
        return round(2 * self.radius * self.pie, 2)


# Test
c = Circle(5)
print(c)
# keep two decimal places for area and perimeter
print(f"Area: {c.area()}, Perimeter: {c.perimeter()}")

try:
    r = float(input("Enter radius: "))
    c = Circle(r, 3.14159265359)
    print(c)
    print(f"Area: {c.area():.2f}, Perimeter: {c.perimeter():.2f}")
except ValueError:
    print("Invalid input. Please enter a valid number for radius.")
else:
    print("Operation completed successfully.")
finally:
    print("Program execution completed.")
