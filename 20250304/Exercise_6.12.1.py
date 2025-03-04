import math

def absolute_value_wrong(x1):
    if x1 < 0:
        return -x1
    if x1 > 0:
        return x1   

def absolute_value_extra_return(x2):
    if x2 < 0:
        return -x2
    else:
        return x2
    
    return 'This is dead code.'

def is_divisible(x, y):
    if x % y == 0:
        return True
    else:
        return False

x1 = int(input("x1: "))
x2 = int(input("x2: "))
x = int(input("x: "))
y = int(input("y: "))
print(absolute_value_wrong(x1))
print(absolute_value_extra_return(x2))
print(is_divisible(x, y))
