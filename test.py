# import inspect

# def dec(f):
#     def wrapper(a, b):
#         f(a*2, b)
#     return wrapper

# @dec
# def add(a, b):
#     print(a + b)

# print(add(1, 1))

class eg:
    def __init__(self, x):
        self.x = x
    
    @staticmethod
    def square(a):
        return a**2

    def print_sqr(self):
        print(self.square(self.x))

x = eg(69)

x.print_sqr()