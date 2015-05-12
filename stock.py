
# -*- coding: utf-8 -*-



import requests
import os
import sqlite3
from stockdb import stockdbtool
import time
from time import localtime,strftime
import datetime
from apscheduler.scheduler import Scheduler
from tools import AmaxB
import stockthread

sched = Scheduler()


STOCK_LIST = [
              
              'sz000725',
              'sh600307',
              'sh600010',
              'sz000825',
              'sh601390'
              ]

URL_ROOT = 'http://qt.gtimg.cn/q='

class Stock():

    def __init__(self, stock_list=None):
        self._stock_list = stock_list
        self._stock_conn_dic = {}
        self.threadspool = stockthread.stockthreadpool()
        self._stock_cache ={}


    def getrtmdata(self ):
        #check if the stock_list is None
        if self._stock_list is None:
            return

        url = URL_ROOT+self._stock_list[0]
        for stock in self._stock_list[1:]:
            url = url+','+stock

        r = requests.get(url)
        if r.status_code != 200:
            print 'wrong'
            raise ValueError('bad requests results!')

        s = r.content.decode('gbk')
        s = s.strip('\n')
        s = s.split('\n')
        tm = str(datetime.date.today())
        for itm in s:
            itm = itm.strip(';')
            itm = itm.split('=')

            if itm[0] not in self._stock_conn_dic.keys():
                dbtool = stockdbtool(itm[0], 1)
                dbtool.ConnectDB()
                self._stock_conn_dic[itm[0]] = dbtool
                self._stock_cache[itm[0]] =[]
                #self.threadspool.addtask()
                print'add new dbtool!'
            dbtool = self._stock_conn_dic[itm[0]]
            des = eval(itm[1]).split('~')
            bs = des[29].split('|')
            for tmp in bs:
                tmp = tmp.split('/')
                v_tuple=(tm,tmp[0],tmp[1],tmp[2],tmp[3],tmp[4])
                self._stock_cache[itm[0]].append(v_tuple)
                #print des[1]+'  recv data : '+str(v_dic_itm)
                dbtool.InsertDB(v_tuple)

            dbtool.CommitDB()
        #print 'all done!'


    def getsummarydata(self):
        if self._stock_list is None:
            return

        for stock in self._stock_list:
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



    def jobrt(self):
        while(True):
            self.getrtmdata()
            time.sleep(5)
            now_time = strftime('%H:%M:%S',localtime())
            if AmaxB(now_time,'11:32:00') and AmaxB('13:00:00',now_time):
                return None
            if AmaxB(now_time,'15:02:00') :
                return None

    def schedulertjob(self):
        self.threadspool.addtask(self.jobrt)
        self.threadspool.runalltask()

    def jobsm(self):
        self.getsummarydata()

    def schedulejob(self):
        sched.start()
        jobstartmorning = sched.add_cron_job(self.jobrt,day_of_week='0,1,2,3,4',hour='9',minute='30')
        jobstartnoon = sched.add_cron_job(self.jobrt,day_of_week='0,1,2,3,4',hour='13',minute='0')
        jobsummarystart = sched.add_cron_job(self.jobsm,day_of_week='0,1,2,3,4',hour='20',minute='0')

def main():

    print 'ok in main'

    st = Stock(STOCK_LIST)
    st.schedulertjob()


    now_time = strftime('%H:%M:%S',localtime())
    if AmaxB(now_time,'9:30:00')  and AmaxB('11:32:00',now_time) :
        jobA()
    if AmaxB(now_time,'13:00:00')  and AmaxB('15:32:00',now_time) :
        jobA()


    while(True):
        print'waiting for the next trace!!'
        time.sleep(100)
    
if __name__ == "__main__":
    main()       
        
        
        
        