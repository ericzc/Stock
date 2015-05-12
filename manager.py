
# -*- coding: utf-8 -*-

from stockthread import StockThreadPool
from threadimp import real_time_task
import time

class Manager():

    def __init__(self):
        self.threadpool = StockThreadPool(20)
        self.stocklist = []
        self.thread2stocklist = {}

    def add_stock(self, stock):
        self.stocklist.append(stock)

    def del_stock(self, stock):
        pass

    def add_stocklist(self, stlst):
        self.stocklist = self.stocklist+stlst

    def _dispatch_stocklist_realtime(self , stlist):
        tid = self.threadpool.add_task( real_time_task , stlist )
        self.thread2stock[tid] = stlist

    def start_realtime(self):
        if len(self.stocklist) > 10:
            i = len(self.stocklist)/10
            for k in range(1,i):
                tmp = self.stocklist[(k-1)*10:k*10]
                self._dispatch_stocklist_realtime(tmp)
        else :
            tmp = self._dispatch_stocklist_realtime(self.stocklist)

        for tid in self.thread2stocklist.keys():
            self.threadpool.start_task(tid)

        while not self.threadpool.is_all_dead():
            time.sleep(1000)
            print 'Manager : wait for next check!'



        print 'Manager : all threads started !'




