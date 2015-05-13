# -*- coding: utf-8 -*-


'''
    This file implements the thread function
    There are two functions in threadimp:

        real_time_task( *args )

        day_summary_task( *args )


'''
import datetime
from tools import AmaxB
from time import strftime, localtime,time, sleep
from stockdb import stockdbtool
import requests



URL_ROOT = 'http://qt.gtimg.cn/q='

def real_time_task( *args ):
    '''
    :param args:  args[0] is a stocklist
    :return: None
    '''
    #check if the stock_list is None
    if not isinstance(args[0],list):
        return None

    conn_dic={}

    while(True):
        now_time = strftime('%H:%M:%S',localtime())
        if AmaxB(now_time,'11:32:00') and AmaxB('13:00:00',now_time):
            return None
        if AmaxB(now_time,'15:02:00') :
            return None
        retrive_realtime_data( args[0] , conn_dic )
        sleep(5)



def retrive_realtime_data( stklist, conn_dic ):

    _stock_list = stklist

    url = URL_ROOT+_stock_list[0]
    for stock in _stock_list[1:]:
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

        if itm[0] not in conn_dic.keys():
            dbtool = stockdbtool(itm[0], 1)
            dbtool.ConnectDB()
            conn_dic[itm[0]] = dbtool
            #print'add new dbtool!'
        dbtool = conn_dic[itm[0]]
        des = eval(itm[1]).split('~')
        bs = des[29].split('|')
        for tmp in bs:
            tmp = tmp.split('/')
            v_tuple=(tm,tmp[0],tmp[1],tmp[2],tmp[3],tmp[4])
            #print des[1]+'  recv data : '+str(v_dic_itm)
            dbtool.InsertDB(v_tuple)
        dbtool.CommitDB()
    #print 'all done!'

def day_summary_task( *args ):
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

