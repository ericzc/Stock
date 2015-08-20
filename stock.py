# -*- coding:utf-8 -*-





QQ_STOCK_URL_PREFIX = 'http://qt.gtimg.cn/q='


class Stock():
    '''
        code is the code of the stock
        name is the chinese name of the stock
        field 指的是某个股票所属的领域，例如太钢不锈属于钢铁炼制领域，属于煤炭相关领域等
        property 指某个股票所能涉及到的关键字，例如钢铁，太钢，太钢某个股东等
    '''
    def __init__(self,code='',name='',urlprefix=QQ_STOCK_URL_PREFIX):
        self.code = code
        self.name = name
        self.field = []
        self.propertys= []
        self.urlprefix = urlprefix

    def addField(self,field):
        self.field.append(field)

    def addProperty(self,property):
        self.propertys.append(property)

    def composeStockURL(self):
        url = self.urlprefix+self.code
        return url




