import math

radius = 5
area = (4/3) * math.pi * radius**3
print("part1 =", area)

x = 42  
result = (math.cos(x))**2 + (math.sin(x))**2  
print("part2 =", result)

result1 = math.e ** 2
result2 = math.pow(math.e, 2)
result3 = math.exp(2)
print("part3 = Using exponentiation operator (**):", result1)
print("part3 = Using math.pow:", result2)
print("part3 = Using math.exp:", result3)