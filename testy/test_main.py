__author__ = 'mcmushroom'

from testy.test_main2 import A

class B:
    def __init__(self):
        self.a = A()


if __name__ == '__main__':
    b = B()
    print(b.a.x)


