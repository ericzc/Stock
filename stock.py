
# -*- coding: utf-8 -*-



import requests
import os
import sqlite3
from stockdb import stockdbtool
import time
from time import localtime,strftime
import datetime
from apscheduler.scheduler import Scheduler

sched = Scheduler()


STOCK_LIST = [
              
              'sz000725',
              'sh600307',
              'sh600010',
              'sz000825',
              'sh601390'
              ]

URL_ROOT = 'http://qt.gtimg.cn/q='

_CONN_DIC={}

def urlrequest(url):
    r = requests.get(url)    
    return r


def getrealtimedata(stock_list):
    if len(stock_list) == 0:
        return 
    
    url = URL_ROOT+stock_list[0]
    for stock in stock_list[1:]:
        url = url+','+stock
    
    r = requests.get(url)
    if r.status_code != 200:
        print 'wrong'
        raise ValueError('bad requests results!')
    s=r.content.decode('gbk')
    s=s.strip('\n')
    s=s.split('\n')    
    tm = str(datetime.date.today())
    for itm in s:
        itm = itm.strip(';')
        itm = itm.split('=')

        if itm[0] not in _CONN_DIC.keys():  
            dbtool = stockdbtool(itm[0],1)        
            dbtool.ConnectDB()
            _CONN_DIC[itm[0]] = dbtool
            print'add new dbtool!'
        dbtool = _CONN_DIC[itm[0]]
        des = eval(itm[1]).split('~')
        bs = des[29].split('|')
        for tmp in bs:
            tmp = tmp.split('/')          
            v_tuple=(tm,tmp[0],tmp[1],tmp[2],tmp[3],tmp[4])
            #print des[1]+'  recv data : '+str(v_dic_itm)
            dbtool.InsertDB(v_tuple)

        dbtool.CommitDB()
    #print 'all done!'  
        


def getsummarydata(stock_list):
    if len(stock_list) == 0 :
        return 
    
    for stock in stock_list:
        url = URL_ROOT+stock
        r = urlrequest(url)
        if r.status_code != 200:
            print 'wrong!'
            raise ValueError('bad requests result!')
        s = r.content.decode('gbk')
        s = s.strip(';\n')
        s = s.split('=')
        des = eval(s[1]).split('~')
        dbtool = stockdbtool(s[0],2)
        dbtool.ConnectDB()

        tm = str(datetime.date.today())
        v_tuple=(tm,des[2],des[1],des[3],des[4],des[5],des[36],des[37],des[7],
                    des[8],des[31],des[32],des[41],des[42],des[38],des[39])

        print 'inster data :' + v_tuple[1] +' '+ str(v_tuple).decode('gbk')
        dbtool.InsertDB(v_tuple)
        dbtool.CommitDB()
        dbtool.CloseDB()
    
    print 'all inserted!'
 

def jobA():
    dt = strftime('%b %d %Y %H:%M:%S ', localtime())
    print 'start jobA is running at time :' + dt
    while(True):
        getrealtimedata(STOCK_LIST)
        time.sleep(5)
        now_time = strftime('%H:%M:%S',localtime())
        if AmaxB(now_time,'11:32:00') and AmaxB('13:00:00',now_time):
            return None
        if AmaxB(now_time,'15:02:00') :
            return None
        
def jobB():
    dt = strftime('%b %d %Y %H:%M:%S ', localtime())
    print 'start jobB is running at time :' + dt
    getsummarydata(STOCK_LIST)


def AmaxB(A,B):
    a = time.strptime(A,'%H:%M:%S')
    b = time.strptime(B,'%H:%M:%S')

    if a >= b :
        return True
    else :
        return False

def main():
    #getsummarydata(STOCK_LIST)
    print'start!'
    sched.start()
    jobstartmorning = sched.add_cron_job(jobA,day_of_week='0,1,2,3,4',hour='9',minute='30')

    jobstartnoon = sched.add_cron_job(jobA,day_of_week='0,1,2,3,4',hour='13',minute='0')

    
    jobsummarystart = sched.add_cron_job(jobB,day_of_week='0,1,2,3,4',hour='20',minute='0')

    now_time = strftime('%H:%M:%S',localtime())
    if AmaxB(now_time,'9:30:00')  and AmaxB('11:32:00',now_time) :
        jobA()
    if AmaxB(now_time,'13:00:00')  and AmaxB('15:32:00',now_time) :
        jobA()


    while(True):
        #getrealtimedata(STOCK_LIST)
        print'waiting for the next trace!!'
        time.sleep(100)
    
if __name__ == "__main__":
    main()       
        
        
        
        