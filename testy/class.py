__author__ = 'mcmushroom'


class A:

    instance = None

    def __init__(self):
        self.x = 'x'
        self.y = 'y'

    @staticmethod
    def get():
        if not A.instance:
            A.instance = A()
        return A.instance



a = A()
print(a.x)
print(a.y)
print(A.get().x)
a.x = 'z'
b = A()
print(A.get().x)
