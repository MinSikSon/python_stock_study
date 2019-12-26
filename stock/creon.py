import win32com.client

import datetime #https://datascienceschool.net/view-notebook/465066ac92ef4da3b0aba32f76d9750a/

TRUE = 1
FALSE = 0

class Creon:
    def __init__(self):
        self.instCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
        #print(self.instCpCybos)
        
        self.instCpStockCode = win32com.client.Dispatch("CpUtil.CpStockCode")
        #print(self.instCpStockCode)

        self.instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")

        self.instMarketEye = win32com.client.Dispatch("CpSysDib.MarketEye")

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
        __stockCode = 0 #1) 종목 코드
        __viewDurationOrCount = 1 #2) 조회 기간 또는 개수
        __requestCount = 4 #3) 요청 개수
        __dataType = 5 #4 요청할 데이터의 종류
        __chartType = 6 #5 차트의 종류
        __modifiedStockValue = 9 #6 수정 주가 반영 여부


        #(dataType, InputData)
        self.instStockChart.SetInputValue(__stockCode, stockCode)
        self.instStockChart.SetInputValue(__viewDurationOrCount, ord('2')) # 1: 조회 기간, 2: 조회 개수 
        self.instStockChart.SetInputValue(__requestCount, days)
        # self.instStockChart.SetInputValue(__dataType, 5) # 5: 종가
        __dataTypeList = (0, 1, 2, 3, 4, 5, 6, 8, 9, 10)
        self.instStockChart.SetInputValue(__dataType, __dataTypeList) # 0: 날짜, 1: 시간, 2: 시가, 3: 고가, 4: 저가, 5: 종가, 6: 전일대비, 8: 거래량, 9: 거래대금, 10: 누적체결매도수량
        self.instStockChart.SetInputValue(__chartType, ord('D')) # D : day
        self.instStockChart.SetInputValue(__modifiedStockValue, ord('1'))
        
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
        
        for i in range(len(__requestValueList)):
            if __requestReturnValueList[i] == 0:
                print("__requestReturnValueList[i] is Zero")
            else:
                if __requestValueList[i] == 4:
                    print("  > 현재가: %s" % (__requestReturnValueList[i]))
                elif __requestValueList[i] == 67:
                    print("  > PER: %s" % (__requestReturnValueList[i]))
                    __returnValueRound = round(1/__requestReturnValueList[i]*100, 2)
                    print("  > 1/PER * 100 = %s %%" % (__returnValueRound))
                elif __requestValueList[i] == 70:
                    print("  > EPS: %s" % (__requestReturnValueList[i]))
                elif __requestValueList[i] == 111:
                    print("  > 최근분기년월: %s" % (__requestReturnValueList[i]))
    
    def stockVolumeAnalysis(self):
        # PSR : ?
        # PBR : Price Book-value Ratio(주가순자산비율) = 현재 주식 가격 / 주당 순자산
        #     : PBR 은 현재 주당 순자산의 몇배로 매매되고 있는지를 보여주는 지표이다.
        #     : PBR 을 간단히 설명하면, 얼마나 튼튼하고 안정적인 기업인지를 판단하는 지표라고 생각하면 된다.
        # BPS : Book-value Per Share(주당순자산) = 순자산 / 총 주식수
        #     : 
        pass
        

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

        for i in range(len(__targetList)):
            print('[%s. %s]' % (i, __targetList[i]))
            stCreon.GetPER(__targetList[i])

