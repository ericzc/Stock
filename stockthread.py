# -*- coding = utf-8 -*-

__author__ = 'eric'

from threading import Thread
import random



class StockThreadPool():


    def __init__(self, num):
        self.max = num
        self.tid2thread = {}

    #def gettask(self,id):
    #    return None if id not in self.pool.values() else self.pool[id]

    def add_task(self, task, param ):
        trd = Thread(target = task, args=(param,))
        tid = self._generate_id()
        self.tid2thread[tid] = trd
        return tid

    def start_task(self,tid):
        print 'starting the thread : ' + self.tid2thread[tid].getName()
        self.tid2thread[tid].start()

    def start_all_task(self):
        for tid in self.tid2thread.keys():
            self.tid2thread[tid].start()


    def _generate_id(self):
        tid = random.randint(1,100000)
        while tid in self.tid2thread.keys():
            tid = random.randint(1,100000)
        return tid

    def is_all_dead(self):
        for tid in self.tid2thread.keys():
            if self.tid2thread[tid].isAlive():
                return False
        return True





