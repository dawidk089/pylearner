__author__ = 'mcmushroom'

class SinglErr(BaseException):
    def __init__(self, mess=''):
        self.mess = mess
    def __str__(self):
        return 'self.mess'



class Singleton:
    def __init__(self):
        if Singleton.private:
            raise RuntimeError("ale jebło")

        self.x = 6

        print('wychodze z konstruktora')



print(Singleton.instance)
print(Singleton.get().x)
s = Singleton()
print(s.x)