import win32com.client

import stock.utils as utils

class StocksByIndustry:
    MARKET = {
        '코스피':1,
        '코스닥':2,
    }
    def __init__(self):
        self.instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")

        self.stUtils = utils.Utils()
        
    def getStockListByMarket(self, market):
        __market = 0
        if 0 <= market | market <= 5:
            __market = market
        codeList = self.instCpCodeMgr.getStockListByMarket(__market)
        return codeList

    def 업종_별_코드_리스트(self, bPrint=False):
        industryCodeList = self.instCpCodeMgr.GetIndustryList()
        
        # industry name 출력
        if bPrint == True:
            for industryCode in industryCodeList:
                print("%s - %s" % (industryCode, self.instCpCodeMgr.GetIndustryName(industryCode)))

        return industryCodeList

    def 업종_내_종목_코드_리스트(self, 업종코드):
        targetCodeList = self.instCpCodeMgr.GetGroupCodeList(업종코드)
        for stockCode in targetCodeList:
            stockName = self.stUtils.get_name_from_code(stockCode)
            print(stockCode, stockName)

        return targetCodeList

