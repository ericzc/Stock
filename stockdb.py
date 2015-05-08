# -*- coding: utf-8 -*-

import sqlite3
import time

_REALTIME_TRADE_DB_NAME='RealTimeTrade.db'
_SUMMARY_STOCK_DB_NAME = 'Stock.db'


#define the cache class
class memcache():
    def __init__(self,fn):
        self.fn = fn
        self.cachedic={}
        pass

    def refresh(self):
        stamp = int(time.time())
        for (ky,va) in self.cachedic.items():
            if stamp - va >= 300:
                del self.cache[ky]

    def __call__(self,*args):
            assert isinstance(args[0],tuple)
            tmp_str = str(args[0])
            if tmp_str not in self.cachedic:
                stamp = int(time.time())
                self.cachedic[tmp_str]=stamp
                self.refresh()
                return self.fn(self.obj,args[0])
            else:
                self.refresh()
                pass
        return wrapper



class stockdbtool:
    def __init__(self,table_name ,type):
        print 'init db for table %s' % table_name
        self.table_name = table_name
        self.type = type
        self.conn = None
        self.cur = None
        self.cache = {}

    def priv_connect_realtime_trade_db(self,tn):
        self.conn = sqlite3.connect(_REALTIME_TRADE_DB_NAME)
        self.conn.text_factory = str
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS %s(stock_date date, time text, price text, volume text, type text, money text)" % tn)
    def priv_connect_summary_stock_db(self,tn):
        self.conn = sqlite3.connect(_SUMMARY_STOCK_DB_NAME)
        self.conn.text_factory = str
        self.cur = self.conn.cursor()
        # summary table
        # stock_code stock_name current_price last_price today_open
        # deal_volume deal_money outside inside fluctuate fluctuate_percent
        # highest lowest exchange enterprise_ratio 
        self.cur.execute('CREATE TABLE IF NOT EXISTS %s(  \
                                                        stock_date date, \
                                                        stock_code text, \
                                                        stock_name text, \
                                                        current_price text, \
                                                        last_price text, \
                                                        today_open text,  \
                                                        deal_volume, \
                                                        deal_money, \
                                                        outside, \
                                                        inside, \
                                                        fluctuate, \
                                                        fluctuate_percent, \
                                                        highest, \
                                                        lowest, \
                                                        exchange, \
                                                        enterprise_ratio \
                                                        )' % tn)
        
    def ConnectDB(self):
        if self.type == 1:
            #RealTime trade db
            self.priv_connect_realtime_trade_db(self.table_name)
        else :
            self.priv_connect_summary_stock_db(self.table_name)
            
    # def priv_refreshcache(self):

                
                            
    # def priv_checkcache(self, value_dic):
    #     sv = str(value_dic)
    #     stamp = int(time.time())
    #     if sv not in self.cache :
    #         self.cache[sv] = stamp
    #         self.priv_refreshcache()
    #         return True
    #     else :
    #         print 'find the same ! escape!'
    #         self.priv_refreshcache()
    #         return False

    @staticmethod
    @memcache
    def priv_insert_realtime_trade_db(table_name,value_tuple):
        #trade table
        #  time price volume type money
        #
        # for realtime we first check the cache to see if the value is already exist
        sqlexe=format('INSERT INTO %s VALUES(?,?,?,?,?,?)' % table_name )
        self.cur.execute(sqlexe,value_tuple)
        print 'insert new data for '+table_name +' : '+ str(value_tuple)

    @memcache
    def priv_summary_stock_db(self,table_name,value_tuple):
        # summary table
        # stock_code stock_name current_price last_price today_open
        # deal_volume deal_money outside inside fluctuate fluctuate_percent
        # highest lowest exchange enterprise_ratio 
        #
        sqlexe=format('INSERT INTO %s VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)' %table_name)
        self.cur.execute(sqlexe,value_tuple)
        
        
    def InsertDB(self,value_tuple):
        if self.type == 1:
            #RealTime trade db
            self.priv_insert_realtime_trade_db(value_tuple)
        else:
            self.priv_summary_stock_db(value_tuple)

    def CommitDB(self):
        self.conn.commit()
     
    def CloseDB(self):
        self.cur.close()
        self.conn.close()   