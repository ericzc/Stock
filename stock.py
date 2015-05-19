# -*- coding:utf-8 -*-


import requests
from threadimp import URL_ROOT

class Stock():
    def __init__(self,code='',name=''):
        self.code = code
        self.name = name


    def setStock(self,code,name):
        self.code = code
        self.name = name

    def getStockInfo(self):
        url = URL_ROOT+code
        r = requests.get(url)



