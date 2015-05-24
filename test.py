from datetime import date
from apscheduler.scheduler import Scheduler
import time
from bs4 import BeautifulSoup
import requests
import time


WEB_URL = 'http://www.baidu.com/s?wd=tsinghua&pn={0}'
NEWS_RUL = 'http://www.baidu.com/ns?word=%C6%F4%C3%F7%D0%C7%B3%BD&rn=10&clk=sortbytime&pn={0}'

# print 'Start!'
#
# for i in range(0,3):
#     page = str(i)+'0'
#     url = WEB_URL.format(page)
#     print url
#     r = requests.get(url)
#     print r.status_code
#     bsp = BeautifulSoup(r.text)
#     rs = bsp.find_all('div',class_='result c-container ')
#     for it in rs:
#         print type(it),it.name,it['id']
#
# print 'Done!'
#

print 'Start! for news'

i  = 0

while(i <= 3):
    time.sleep(3)
    page = str(i)+'0'
    url = NEWS_RUL.format(page)
    print url
    r = requests.get(url)
    #print r.status_code
    bsp = BeautifulSoup(r.text)
    rs = bsp.find_all('li',class_='result')
    print len(rs)
    if len(rs) == 0:
        print 'retring the url', url
        continue
    for it in rs:
        #print type(it),it.name,it['id']
        #print it.h3.a['href']
        print it.div.p.string.replace(u'\xa0',u' ').split(u' ')[0], it.div.p.string.replace(u'\xa0',u' ').split(u' ')[2]

    i= i+1

print 'Done!'















