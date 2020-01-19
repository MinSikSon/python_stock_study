import win32com.client

import datetime #https://datascienceschool.net/view-notebook/465066ac92ef4da3b0aba32f76d9750a/
import time

TRUE = 1
FALSE = 0

# 1. 초기화 및 크레온 접속 ?
# 2. 조회
# 3. 알고리즘 (todo)
# 4. 매매/매수
# 5. 결과 확인 (== 조회?)
# (6. 그래프)

class Connection:
    def __init__(self, logging=False):
        self.instCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
        self.logging = logging

    def check_connect(self):
        bConnect = self.instCpCybos.IsConnect
        if bConnect == 1:
            if self.logging == True:
                print("[check_connect] connect! (ret : %s)" % bConnect)
        else :
            print("[check_connect] fail.. (ret : %s)" % bConnect)
            
        return bConnect

class Utils:
    def __init__(self):
        self.종목_코드 = 0
        self.조회방법 = 1
        self.요청_개수 = 4
        self.요청할_데이터의_종류 = 5
        self.차트의_종류 = 6
        self.수정_주가_반영_여부 = 9

        self.instCpStockCode = win32com.client.Dispatch("CpUtil.CpStockCode")

        self.instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
    
    def get_code_from_name(self, name):
        return self.instCpStockCode.NameToCode(name)

    def get_name_from_code(self, code):
        return self.instCpStockCode.CodeToName(code)

    def set_stock_chart_info(self, 종목코드, 조회방법, 요청기간_또는_요청일수, 요청할_데이터_종류=(0, 1, 2, 3, 4, 5, 6, 8, 9, 10), 차트종류=ord('D'), 수정주가반영여부=ord('1')):
        self.instStockChart.SetInputValue(self.종목_코드, 종목코드)
        self.instStockChart.SetInputValue(self.조회방법, 조회방법) # 1: 조회 기간, 2: 조회 개수 
        self.instStockChart.SetInputValue(self.요청_개수, 요청기간_또는_요청일수)
        # self.instStockChart.SetInputValue(__dataType, 5) # 5: 종가
        self.instStockChart.SetInputValue(self.요청할_데이터의_종류, 요청할_데이터_종류) # 0: 날짜, 1: 시간, 2: 시가, 3: 고가, 4: 저가, 5: 종가, 6: 전일대비, 8: 거래량, 9: 거래대금, 10: 누적체결매도수량
        self.instStockChart.SetInputValue(self.차트의_종류, 차트종류) # D : day
        self.instStockChart.SetInputValue(self.수정_주가_반영_여부, 수정주가반영여부)

    def get_stock_value_n_days(self, stockCode, days, bPrint=False): # https://wikidocs.net/3684
        if bPrint == True:
            print('code : %s, name : %s' % (stockCode, self.get_name_from_code(stockCode)))

        #(dataType, InputData)
        __dataTypeList = (0, 1, 2, 3, 4, 5, 6, 8, 9, 10) # 0: 날짜, 1: 시간, 2: 시가, 3: 고가, 4: 저가, 5: 종가, 6: 전일대비, 8: 거래량, 9: 거래대금, 10: 누적체결매도수량
        self.set_stock_chart_info(stockCode, ord('2'), days, __dataTypeList, ord('D'), ord('1'))
        
        self.instStockChart.BlockRequest() # request data from the server

        __numData = self.instStockChart.GetHeaderValue(3) # response. receive data from the server
        if bPrint == True:
            print('numData : %s' % __numData)

        # __dateTime = datetime.datetime.now()
        # __weekday = __dateTime.weekday()
        for i in range(__numData):
            __stockValue = []
            for j in range(len(__dataTypeList)):
                __stockValue.append(self.instStockChart.GetDataValue(j, i))
            if bPrint == True:
                print('%s' % __stockValue)

            # print('%s/%s(%s) %s %s' % (__dateTime.month, __dateTime.day - i, __weekday - i, __stockValue, __stockValue_2))
        return __stockValue

class Trading:
    def __init__(self, logging=False):
        self.logging = logging

        self.stUtils = Utils()

        self.instCpTdUtil = win32com.client.Dispatch("CpTrade.CpTdUtil")
        self.instCpTd0311 = win32com.client.Dispatch("CpTrade.CpTd0311")

        # 매수/매도 확인
        # self.instCpConclusion = win32com.client.Disptch("CpConclusion")

        # 주식 잔고 조회
        self.instCpTd6033 = win32com.client.Dispatch("CpTrade.CpTd6033")

    # 거래 관련부 : init -> setinputvalue -> blockrequest
    def trade_init(self):
        ret = self.instCpTdUtil.TradeInit()
        if self.logging == True:
            if ret == 0:
                print('[tradeInit] 성공')
            elif ret == -1:
                print('[tradeInit] 오류')
            elif ret == 1:
                print('[tradeInit] OTP/보안카드 키 입력 잘못 됨')
            elif ret == 3:
                print('[tradeInit] 취소')
            else:
                print('[tradeInit] ??')
        return ret

    def 주식_주문(self, stockName):
        __필드__주문_종류_코드 = 0
        __매수 = 1
        __매도 = 2
        __필드__계좌_번호 = 1
        __내_계좌_번호 = self.instCpTdUtil.AccountNumber[0]
        __필드__종목_코드 = 2
        __필드__주문_수량 = 3
        __주문_수량 = 10
        __필드__주문_단가 = 5
        __주문_단가 = 55000
        self.instCpTd0311.SetInputValue(__필드__주문_종류_코드, __매수)
        self.instCpTd0311.SetInputValue(__필드__계좌_번호, __내_계좌_번호)

        stockCode = self.stUtils.get_code_from_name(stockName)
        self.instCpTd0311.SetInputValue(__필드__종목_코드, stockCode)

        self.instCpTd0311.SetInputValue(__필드__주문_수량, __주문_수량)

        self.instCpTd0311.SetInputValue(__필드__주문_단가, __주문_단가)

        # 요청
        self.instCpTd0311.BlockRequest()
        
    def 주식_잔고_조회(self, bPrint=False):
        if bPrint == True:
            print('> 주식_잔고_조회')

        __계좌번호 = self.instCpTdUtil.AccountNumber[0]
        __주식상품_구분 = self.instCpTdUtil.GoodsList(__계좌번호, 1) # ?
        if bPrint == True:
            print('계좌번호 : %s, 주식상품_구분 : %s' % (__계좌번호, __주식상품_구분))
        
        self.instCpTd6033.SetInputValue(0, __계좌번호)  # 계좌번호
        self.instCpTd6033.SetInputValue(1, __주식상품_구분[0])  # 상품구분 - 주식 상품 중 첫번째
        self.instCpTd6033.SetInputValue(2, 50)  # 요청 건수(최대 50)
        self.dicflag1 = {ord(' '): '현금',
                         ord('Y'): '융자',
                         ord('D'): '대주',
                         ord('B'): '담보',
                         ord('M'): '매입담보',
                         ord('P'): '플러스론',
                         ord('I'): '자기융자',
                         }

        return self.requestJango(bPrint)
    

    def requestJango(self, caller=0, bPrint=False):
        while True:
            self.instCpTd6033.BlockRequest()
            # 통신 및 통신 에러 처리
            rqStatus = self.instCpTd6033.GetDibStatus()
            rqRet = self.instCpTd6033.GetDibMsg1()
            if bPrint == True:
                print("통신상태", rqStatus, rqRet)
            if rqStatus != 0:
                print("통신상태", rqStatus, rqRet)
                return False
 
            cnt = self.instCpTd6033.GetHeaderValue(7)

            if bPrint == True:
                print(cnt)
 
            잔고 = 0
            ret_list = []
            for i in range(cnt):
                item = {}
                code = self.instCpTd6033.GetDataValue(12, i)  # 종목코드
                item['종목코드'] = code
                item['종목명'] = self.instCpTd6033.GetDataValue(0, i)  # 종목명
                item['잔고수량'] = self.instCpTd6033.GetDataValue(7, i)  # 체결잔고수량

                item['매도가능'] = self.instCpTd6033.GetDataValue(15, i)
                item['장부가'] = self.instCpTd6033.GetDataValue(17, i)  # 체결장부단가
                item['매입금액'] = item['장부가'] * item['잔고수량']
                __n_days_list = self.stUtils.get_stock_value_n_days(code, 1) # parameter 가 1이 아닐 경우, 아래 code 수정 필요
                item['현재가'] = __n_days_list[2] # 시가
                item['대비'] = 0
                item['거래량'] = 0
 
                합계 = item['잔고수량'] * item['현재가']
                if bPrint == True:
                    print('%s : 잔고수량(%s) * 현재가(%s) = (%s) (매도가능? %s)' % (item['종목명'], item['잔고수량'], item['현재가'], 합계, item['매도가능']))
                잔고 = 잔고 + 합계
                ret_list.append(item)

            if bPrint == True:
                print('잔고 : %s' % format(잔고, ','))
            if (self.instCpTd6033.Continue == False):
                break
        return ret_list

class StockInfo:
    종목코드_음식료품 = 5

    현재가 = 4 # MarketEye.
    매수호가 = 9 # MarketEye.
    VOLUME = 10 # MarketEye. 거래량
    거래대금 = 11 # MarketEye.
    총상장주식수 = 20 # MarketEye.
    PER = 67 # MarketEye. 주가/주당순이익
    BPS = 89 # MarketEye. 주당순자산

    def __init__(self):
        self.stUtils = Utils()

        self.instMarketEye = win32com.client.Dispatch("CpSysDib.MarketEye")

        self.instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")

    def GetInfo(self, stockName, requestType):
        필드_요청타입 = 0
        필드_주식코드 = 1
        # print('requestType : %s' % (requestType))
        self.instMarketEye.SetInputValue(필드_요청타입, requestType)
        주식코드 = self.stUtils.get_code_from_name(stockName)
        self.instMarketEye.SetInputValue(필드_주식코드, 주식코드)

        self.instMarketEye.BlockRequest() # 서버에 데이터 요청

        ret_value = []
        if type(requestType) == int:
            ret_value.append(self.instMarketEye.GetDataValue(0, 0))
        else :
            for i in range(len(requestType)):
                ret_value.append(self.instMarketEye.GetDataValue(i, 0))

        return ret_value

    def stockVolumeAnalysis(self, stockName, 몇배, days=60):
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
        __stockCode = self.stUtils.get_code_from_name(stockName)
        __거래량 = 8
        self.stUtils.set_stock_chart_info(__stockCode, ord('2'), days, __거래량,  ord('D'), ord('1'))

        # server 에 요청
        self.stUtils.instStockChart.BlockRequest()

        # server 에서 data 받아옴
        volumes = []
        numData = self.stUtils.instStockChart.GetHeaderValue(3)
        for i in range(numData):
            volume = self.stUtils.instStockChart.GetDataValue(0, i)
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
        CPC_MARKET_KOSP = 1
        codeList = self.instCpCodeMgr.getStockListByMarket(CPC_MARKET_KOSP)
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


class Algorithm:
    def __init__(self):
        pass
    