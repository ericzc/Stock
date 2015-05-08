from datetime import date
from apscheduler.scheduler import Scheduler
import time








def Dector(fn):
    a = []
    def wrapper(*args):
        print args

        a.append(args[1])
        print a

        return fn(*args)
    return wrapper





class myfunc():
    def __init__(self):
        pass

    @Dector
    def calculate(self, num):
        print'num is ' +num

a = myfunc()
a.calculate('3')
a.calculate('4')
a.calculate('5')

b = myfunc()
b.calculate('7')
b.calculate('8')
b.calculate('9')






