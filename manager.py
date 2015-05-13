
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
        self.thread2stocklist[tid] = stlist

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
            time.sleep(10)
            print 'Manager : wait for next check!'
        print 'Manager : all threads finished !'

    def get_day_summary(self):
        if self.stocklist is None:
            return

        for stock in self.stocklist:
            url = URL_ROOT+stock
            r = requests.get(url)
            if r.status_code != 200:
                print 'wrong!'
                raise ValueError('bad requests result!')
            s = r.content.decode('gbk')
            s = s.strip(';\n')
            s = s.split('=')
            des = eval(s[1]).split('~')
            dbtool = stockdbtool(s[0], 2)
            dbtool.ConnectDB()

            tm = str(datetime.date.today())
            v_tuple=(tm, des[2], des[1], des[3], des[4], des[5], des[36], des[37], des[7],
                         des[8], des[31], des[32], des[41], des[42], des[38], des[39])

            print 'inster data :' + v_tuple[1] +' '+str(v_tuple).decode('gbk')
            dbtool.InsertDB(v_tuple)
            dbtool.CommitDB()
            dbtool.CloseDB()




