# -*- coding: utf-8 -*-

import sqlite3
import time

_REALTIME_TRADE_DB_NAME='RealTimeTrade.db'
_SUMMARY_STOCK_DB_NAME = 'Stock.db'


#define the cache class

def shortalert(fn):

    def wrapper(*args):
        #print 'in short alert ' +str(args)
        if isinstance(args[1],tuple):
            #print args[1]
            #process the trade
            if int(args[1][3])/100 >= 2000:
                if args[1][4] == 'S':
                    print args[2] +' short alert ! ! Active Sell ('+ str(int(args[1][3])/100)+')'
                elif args[1][4] == 'B':
                    print args[2] + ' short alert !! Active Buy (' +str(int(args[1][3])/100)+')'
            return fn(*args)


    return wrapper


def memcache(fn):
    cachedic = {}

    def wrapper(*args):
        #args[0] is the self pointer
        #args[1] is the str likt v_shxxxx+201550232+....
        #print args
        tmp_str = str(args[1])+args[2]
        #print 'in memcache cache str :'+ tmp_str
        stamp = int(time.time())
        if tmp_str not in cachedic:
            cachedic[tmp_str] = stamp
            for (ky, va) in cachedic.items():
                if stamp - va >= 300:
                    del cachedic[ky]
            return fn( *args )
        else:
            #print'found the same in cache!'
            for (ky, va) in cachedic.items():
                if stamp - va >= 300:
                    del cachedic[ky]
            pass
    return wrapper



DB_DESCRIBE_DIC={'DB_REALTIME':1,'DB_SUMMARY':2}

class stockdbtool:
    def __init__(self,typestring):
        #print 'init db for table %s' % table_name
        self.type = DB_DESCRIBE_DIC[typestring]
        self.conn = None
        self.cur = None
        self.cache = {}
        self.tables= []

    def priv_connect_realtime_trade_db(self,tn):
        self.conn = sqlite3.connect(_REALTIME_TRADE_DB_NAME)
        self.conn.text_factory = str

    def priv_connect_summary_stock_db(self,tn):
        self.conn = sqlite3.connect(_SUMMARY_STOCK_DB_NAME)
        self.conn.text_factory = str

        
    def ConnectDB(self):
        if self.type == DB_DESCRIBE_DIC['DB_REALTIME']:
            self.priv_connect_realtime_trade_db(_REALTIME_TRADE_DB_NAME)
        elif self.type == DB_DESCRIBE_DIC['DB_SUMMARY']:
            self.priv_connect_summary_stock_db(_SUMMARY_STOCK_DB_NAME)
            
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

    @memcache
    @shortalert
    def priv_insert_realtime_trade_db(self, value_tuple , tname ):
        #trade table
        #  time price volume type money
        #
        # for realtime we first check the cache to see if the value is already exist
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS %s(\
                                                        stock_date date,\
                                                        time text, \
                                                        price text, \
                                                        volume text, \
                                                        type text, \
                                                        money text)" % tname)

        sqlexe=format('INSERT INTO %s VALUES(?,?,?,?,?,?)' % tname )
        self.cur.execute(sqlexe, value_tuple)
        #print 'insert new data for '+self.table_name + ' : ' + str(value_tuple)



    @memcache
    def priv_summary_stock_db(self,value_tuple, tname):
        # summary table
        # stock_code stock_name current_price last_price today_open
        # deal_volume deal_money outside inside fluctuate fluctuate_percent
        # highest lowest exchange enterprise_ratio 
        #

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
                                                        )' % tname)

        sqlexe=format('INSERT INTO %s VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)' % tname)
        self.cur.execute(sqlexe, value_tuple)
        
        
    def InsertDB(self,table_name,value_tuple):
        if self.type == DB_DESCRIBE_DIC['DB_REALTIME']:
            self.priv_insert_realtime_trade_db(value_tuple, table_name)
        elif self.type == DB_DESCRIBE_DIC['DB_SUMMARY']:
            self.priv_summary_stock_db(value_tuple, table_name)

    def CommitDB(self):
        self.conn.commit()
     
    def CloseDB(self):
        self.cur.close()
        self.conn.close()   