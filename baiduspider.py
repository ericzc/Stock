# -*- coding: utf-8 -*-


__author__ = 'eric'


from bs4 import BeautifulSoup
import requests
import re
from requests import ConnectionError

from threading import Thread
from datetime import *
import  time
NEWS_RUL = 'http://www.baidu.com/ns'

def baidunewspider(*args):

    kword = args[0]

    if not isinstance(args[1], list):
        return
    itmlist = args[1]

    param={}
    param['rn']=10
    param['clk']='sortbytime'
    param['word']=kword

    i  = 0

    while(i <= 3):
        time.sleep(3)
        page = str(i)+'0'
        param['pn']=page
        #url = NEWS_RUL.format(page)
        #print url
        r = requests.get(NEWS_RUL, params=param)
        print r.url
        #print r.status_code
        bsp = BeautifulSoup(r.text)
        rs = bsp.find_all('li',class_='result')
        print len(rs)
        if len(rs) == 0:
            print 'retring the url', r.url
            continue
        for it in rs:
            #print type(it),it.name,it['id']
            #print it.h3.a['href']
            itm = baidunewsitem()

            itm.seturl(it.h3.a['href'])
            itm.setsource(it.div.p.string.replace(u'\xa0',u' ').split(u' ')[0])
            itm.settime(it.div.p.string.replace(u'\xa0',u' ').split(u' ')[2])
            tmp_title = ''
            for s in  it.h3.a.strings:
                tmp_title = tmp_title+s
            itm.settitle(tmp_title)
            itmlist.append(itm)

            print it.div.p.string.replace(u'\xa0',u' ').split(u' ')[0],\
                  it.div.p.string.replace(u'\xa0',u' ').split(u' ')[2],\
                  it['id'], it.h3.a['href'],\
                  tmp_title

        i= i+1

    #process the item list

    for itm in itmlist:
        print itm.geturl()

    #index=0
    for itm in itmlist:
        u = itm.geturl()
        print u
        try:
            r = requests.get(u)
        except ConnectionError:
            print 'ConnectionError for '+u
            continue

        b = BeautifulSoup(r.content)
        s = ''
        for tmp in b.stripped_strings:
            s = s+tmp
        s = s.encode('utf-8',errors='ignore')
        s= re.sub(r'[\w\{\}(\)=\"\.;\[\]%\\/:\?\'\+`\-><|#,@\*\r\n\t&!\$]*','',s)
        itm.setcontent(s)
        #print str(index)+' : '+s
        #index+=1



class baidunewsitem():

    def __init__(self):
        self.title = ''
        self.source = ''
        self.source_time = ''
        self.url = ''
        self.score = 0
        self.content =''


    def settitle(self,title):
        self.title = title

    def setsource(self,source):
        self.source = source

    def settime(self,st):
        self.source_time = st

    def seturl(self,url):
        self.url=url

    def setcore(self,score):
        self.score = score

    def geturl(self):
        return self.url
    def setcontent(self,ct):
        self.content=ct

    def getsourcetime(self):
        return self.source_time

class mynewSpider():

    def __init__(self, kword):
        self.kword = kword
        self.itemlist = []
        self.spiderimp = baidunewspider
        self.trd = None

    def startspider(self):
        self.trd = Thread(target=self.spiderimp, args=(self.kword,self.itemlist))
        self.trd.start()

    def waitforspider(self):
        self.trd.join()

    def drawhotlineperday(self):
        if len(self.itemlist) == 0:
            print ' the item list is null '

        hotperday_dic={}

        for itm in self.itemlist:
            stime = itm.getsourcetime()

            b = re.search(ur'[\d]+[\u4e00-\u9fa5]+(\u524d)$', stime)
            if b is None:
                # possible the standard date time
                dt = datetime.strptime(stime.encode('utf-8'),'%Y年%m月%d日')
                s=dt.strftime('%Y-%m-%d')
                print 'history: '+s
                hotperday_dic[s] = (hotperday_dic[s]+1) if s in hotperday_dic else 1
            else:
                #today news
                s =datetime.now().strftime('%Y-%m-%d')
                print 'today : '+s
                hotperday_dic[s] = (hotperday_dic[s] + 1) if s in hotperday_dic else 1

        path = '/Users/eric/Desktop/'+self.kword+'.txt'

        fh=open(path,'a')
        list_hot = hotperday_dic.items()
        list_hot.sort(key=lambda x: datetime.strptime(x[0],'%Y-%m-%d'))
        for (k,v) in list_hot:
            fh.write(k)
            fh.write('\t')
            fh.write(str(v))
            fh.write('\n')





# b=re.search(ur'[\d]+[\u4e00-\u9fa5]+(\u524d)$',u'33分钟前时间')
th = mynewSpider('华联股份')
th.startspider()
th.waitforspider()
th.drawhotlineperday()
print len(th.itemlist)

