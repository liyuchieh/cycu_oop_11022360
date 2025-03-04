def gcd(a: int, b: int) -> int:
    if b == 0:
        return a  #當餘數為0，返回a
    return gcd(b, a % b)  

num1 = int(input("number1: "))
num2 = int(input("number2: "))
result = gcd(num1, num2)
print(f"{num1} 和 {num2} 的最大公因數是 {result}")
