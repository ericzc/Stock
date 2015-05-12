# -*- coding = utf-8 -*-

__author__ = 'eric'

import threading
import random

class stockworker(threading.Thread):

    def __init__(self, task, param=()):
        super(stockworker,self).__init__()
        self.task = task
        self.param = param

    def run(self):

        try:
            self.task(self.param)
        except Exception:
            print ' ooh exception in thread :'+self.getName()




class stockthreadpool():


    def __init__(self):
        self.pool = {}

    def gettask(self,id):
        return None if id not in self.pool.values() else self.pool[id]

    def addtask(self, task, param = ()):
        worker = stockworker(task,param)
        id = self.generateid()
        self.pool[id] = worker
        return id

    def runtask(self,id):
        self.pool[id].start()

    def runalltask(self):
        for id in self.pool.keys():
            self.pool[id].start()


    def generateid(self):
        id = random.randint(1,100000)
        while( id in self.pool.values()):
            id = random.randint(1,100000)
        return id




