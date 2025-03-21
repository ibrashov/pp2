from functools import reduce

def multiply(num):
    return reduce(lambda x, y: x * y, num)

list1 = input("Write numbers for list: ")

num = list1.split()

num = list(map(int, num))

print("Result: ", multiply(num))