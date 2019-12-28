import win32com.client

import datetime #https://datascienceschool.net/view-notebook/465066ac92ef4da3b0aba32f76d9750a/
import time

TRUE = 1
FALSE = 0

class Creon:
    종목코드_음식료품 = 5

    def __init__(self):
        self.종목_코드 = 0
        self.조회_기간_또는_개수 = 1
        self.요청_개수 = 4
        self.요청할_데이터의_종류 = 5
        self.차트의_종류 = 6
        self.수정_주가_반영_여부 = 9


        self.instCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
        #print(self.instCpCybos)
        
        self.instCpStockCode = win32com.client.Dispatch("CpUtil.CpStockCode")
        #print(self.instCpStockCode)

        self.instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")

        self.instMarketEye = win32com.client.Dispatch("CpSysDib.MarketEye")

        self.instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")

    def check_connect(self):
        bConnect = self.instCpCybos.IsConnect
        if bConnect == 1:
            print("[check_connect] connect! %s" % bConnect)
        else :
            print("[check_connect] fail.. %s" % bConnect)
        return bConnect

    def get_code_from_name(self, name):
        return self.instCpStockCode.NameToCode(name)

    def get_name_from_code(self, code):
        return self.instCpStockCode.CodeToName(code)

    def get_stock_value_n_days(self, stockCode, days): # https://wikidocs.net/3684
        print('code : %s' % stockCode)
        print('name : %s' % self.get_name_from_code(stockCode))

        #(dataType, InputData)
        self.instStockChart.SetInputValue(self.종목_코드, stockCode)
        self.instStockChart.SetInputValue(self.조회_기간_또는_개수, ord('2')) # 1: 조회 기간, 2: 조회 개수 
        self.instStockChart.SetInputValue(self.요청_개수, days)
        # self.instStockChart.SetInputValue(__dataType, 5) # 5: 종가
        __dataTypeList = (0, 1, 2, 3, 4, 5, 6, 8, 9, 10)
        self.instStockChart.SetInputValue(self.요청할_데이터의_종류, __dataTypeList) # 0: 날짜, 1: 시간, 2: 시가, 3: 고가, 4: 저가, 5: 종가, 6: 전일대비, 8: 거래량, 9: 거래대금, 10: 누적체결매도수량
        self.instStockChart.SetInputValue(self.차트의_종류, ord('D')) # D : day
        self.instStockChart.SetInputValue(self.수정_주가_반영_여부, ord('1'))
        
        self.instStockChart.BlockRequest() # request data from the server

        __numData = self.instStockChart.GetHeaderValue(3) # response. receive data from the server
        print('numData : %s' % __numData)

        # __dateTime = datetime.datetime.now()
        # __weekday = __dateTime.weekday()
        for i in range(__numData):
            __stockValue = []
            for j in range(len(__dataTypeList)):
                __stockValue.append(self.instStockChart.GetDataValue(j, i))
            print('%s' % __stockValue)

            # print('%s/%s(%s) %s %s' % (__dateTime.month, __dateTime.day - i, __weekday - i, __stockValue, __stockValue_2))

    # 현재의 주가를 과거? 의 주당순이익(EPS) 로 나눈 값인 것에 유의하자.
    def GetPER(self, stockName): # PER : Price Earning Ratio, 주가를 주당 순이익(EPS) 으로 나눈 값. 주가의 수익성 지표로 자주 활용 된다.
        # 높은 PER : 기업이 영업활동으로 벌어들인 이익에 비해 주가가 고평가 되고 있음을 의미한다.
        # 낮은 PER : 주가가 상대적으로 저평가되고 있음을 의미한다.
        __requestValueField = 0
        # __requestValueList = (4, 67, 70, 111) # 현재가, PER, EPS, 최근분기년월 데이터
        __requestValueList = (67,) # PER
        __stockCodeField = 1
        __stockCode = self.get_code_from_name(stockName)
        
        self.instMarketEye.SetInputValue(__requestValueField, __requestValueList)
        self.instMarketEye.SetInputValue(__stockCodeField, __stockCode)

        self.instMarketEye.BlockRequest() # 서버에 데이터 요청

        __requestReturnValueList = []
        for i in range(len(__requestValueList)):
            __requestReturnValueList.append(self.instMarketEye.GetDataValue(i, 0))
        
        # print(len(__requestReturnValueList)) --> 1개만 리턴함.. 사실 list 아님
        for i in range(len(__requestValueList)):
            if __requestReturnValueList[i] == 0:
                print("%s is Zero" % (stockName))
            else:
                if __requestValueList[i] == 4:
                    print("%s  > 현재가: %s" % (stockName, __requestReturnValueList[i]))
                elif __requestValueList[i] == 67:
                    __returnValueRound = round(1/__requestReturnValueList[i]*100, 2)
                    print("%s  > PER: %s (1/PER * 100 = %s %%)" % (stockName, round(__requestReturnValueList[i], 4), __returnValueRound))
                elif __requestValueList[i] == 70:
                    print("%s  > EPS: %s" % (stockName, __requestReturnValueList[i]))
                elif __requestValueList[i] == 111:
                    print("%s  > 최근분기년월: %s" % (stockName, __requestReturnValueList[i]))
    
        return __requestReturnValueList

    def stockVolumeAnalysis(self, stockName, 몇배):
        # print('[stockVolumeAnalysis] 최근 거래량과 60일 평균 거래량 비교')
        # PSR : ?
        # PBR : Price Book-value Ratio(주가순자산비율) = 현재 주식 가격 / 주당 순자산
        #     : PBR 은 현재 주당 순자산의 몇배로 매매되고 있는지를 보여주는 지표이다.
        #     : PBR 을 간단히 설명하면, 얼마나 튼튼하고 안정적인 기업인지를 판단하는 지표라고 생각하면 된다.
        # BPS : Book-value Per Share(주당순자산) = 순자산 / 총 주식수
        #     : 
        
        # [조건]
        # 1) 대량 거래(거래량 1,000% 이상 급증) 종목
        # 2) 대량 거래 시점에 PBR 이 4보다 작아야 함
        __stockCode = self.get_code_from_name(stockName)
        __days = 60
        __거래량 = 8
        self.instStockChart.SetInputValue(self.종목_코드, __stockCode)
        self.instStockChart.SetInputValue(self.조회_기간_또는_개수, ord('2'))
        self.instStockChart.SetInputValue(self.요청_개수, __days)
        self.instStockChart.SetInputValue(self.요청할_데이터의_종류, __거래량)
        self.instStockChart.SetInputValue(self.차트의_종류, ord('D'))
        self.instStockChart.SetInputValue(self.수정_주가_반영_여부, ord('1'))

        # server 에 요청
        self.instStockChart.BlockRequest()

        # server 에서 data 받아옴
        volumes = []
        numData = self.instStockChart.GetHeaderValue(3)
        for i in range(numData):
            volume = self.instStockChart.GetDataValue(0, i)
            if volume == 0:
                #print('%s 은(는) 거래가 중지된 품목입니다.' % (stockName))
                return # 거래 중지된 경우
            volumes.append(volume)
            # print('volumes[%s] : %s' % (i, volumes[i]))
        # print(volumes)

        volumesLen = len(volumes)
        if volumesLen == 1:
            avgVolume = volumes[0]
        else :
            avgVolume = (sum(volumes) - volumes[0]) / (len(volumes) - 1)

        # print('  > volumes[0] : %s' % (volumes[0]))
        # print('  > avgVolume : %s' % (avgVolume))
        if volumes[0] > avgVolume * 몇배:
            print('(거래량 %s 배) %s 은(는) 대박 주! ' % (round((volumes[0] / avgVolume), 3), stockName))
            return 1
        else:
            return 0
            #print('(거래량 %s 배) %s 은(는) 일반 주.. ' % (round((volumes[0] / avgVolume), 3), stockName))

    def getStockListByMarket(self):
        codeList = self.instCpCodeMgr.getStockListByMarket(1)
        return codeList

    def 업종_별_코드_리스트(self):
        industryCodeList = self.instCpCodeMgr.GetIndustryList()
        
        # industry name 출력
        for industryCode in industryCodeList:
            print("%s - %s" % (industryCode, self.instCpCodeMgr.GetIndustryName(industryCode)))

        return industryCodeList

    def 업종_내_종목_코드_리스트(self, 업종코드):
        targetCodeList = self.instCpCodeMgr.GetGroupCodeList(업종코드)
        for stockCode in targetCodeList:
            stockName = self.get_name_from_code(stockCode)
            print(stockCode, stockName)

        return targetCodeList


if __name__ == '__main__':
    stCreon = Creon()
    bConnect = stCreon.check_connect()

    if bConnect == TRUE :
        # __target = '삼성전자'
        # code = stCreon.get_code_from_name(__target)
        # print("%s code : %s" % (__target, code))

        # name = stCreon.get_name_from_code(code)
        # print("%s name : %s" % (__target, name))

        # stCreon.get_stock_value_n_days(code, 15)

        # stCreon.GetPER(__target)

        

        # for i in range(len(__targetList)):
        #     print('[%s. %s]' % (i, __targetList[i]))
        #     stCreon.GetPER(__targetList[i])

        # print('이전 60일 대비 오늘 거래량 비율')
        bViewAll = 0
        if bViewAll == 1:
            codeList = stCreon.getStockListByMarket()
            codeListLen = len(codeList)
            print('codeListLen : %s' % (codeListLen))
            __targetList = []
            for i in range(codeListLen):
                name = stCreon.get_name_from_code(codeList[i])
                __targetList.append(name)

        else:
            __targetList = ('삼성전자',
                        'SK하이닉스',
                        'CJ',
                        '카카오',
                        'JYP Ent.',
                        '삼성바이오로직스',
                        '셀트리온',
                        'KCC',
                        '현대제철',
                        '엔씨소프트',
                        '신세계',
                        '고려제약',
                        '케이맥',
                        '제주반도체',
                        '에프엔씨엔터',
                        '와이지엔터테인먼트',
                        '메디톡스',
                        '현대차',
                        '큐브엔터',
                        '삼성물산',
                        '대한항공',
                        '아시아나항공',
                        '한국콜마',
                        '인터로조',
                        '폴루스바이오팜'
                        )
            codeListLen = len(__targetList)

        몇배 = 1.5
        buyList = []
        # for i in range(codeListLen):
        #     if stCreon.stockVolumeAnalysis(__targetList[i], 몇배) == 1:
        #         buyList.append(__targetList[i])
            # time.sleep(1)

        stCreon.업종_별_코드_리스트()

        음식료품_코드_리스트 = stCreon.업종_내_종목_코드_리스트(stCreon.종목코드_음식료품)

        sumPER = 0
        sumCount = 0
        for stockCode in 음식료품_코드_리스트:
            name = stCreon.get_name_from_code(stockCode)
            if stCreon.stockVolumeAnalysis(name, 몇배) == 1:
                buyList.append(name)
                
            PER = stCreon.GetPER(name)[0]
            if PER > 0:
                sumPER += PER
                sumCount += 1
            # time.sleep(1)
        
        print('sumPER %s' % (sumPER))
        print('sumCount %s' % (sumCount))
        print('avg PER = %s' % (round((sumPER/sumCount), 4)))



