# -*- coding: utf-8 -*-


'''
    This file implements the thread function
    There are two functions in threadimp:

        real_time_task( *args )

        day_summary_task( *args )


'''
import datetime
from tools import AmaxB
from time import strftime, localtime,time
from stockdb import stockdbtool



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
        time.sleep(5)



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
            print'add new dbtool!'
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

