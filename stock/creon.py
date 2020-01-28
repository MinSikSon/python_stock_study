import ctypes
import win32com.client
import pythoncom

import datetime #https://datascienceschool.net/view-notebook/465066ac92ef4da3b0aba32f76d9750a/
import time
from time import sleep


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
        if ctypes.windll.shell32.IsUserAnAdmin():
            if self.logging == True:
                print("[check_connect] 정상: 관리자 권한으로 실행된 프로세스")
        else:
            print("[check_connect] 오류: 관리자 권한으로 실행하세요")
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

    def waiting(self, time, bPrint=False):
        cnt = 0
        while True:
            ret = pythoncom.PumpWaitingMessages() # ?
            cnt = cnt + 1
            sleep(1)
            if bPrint == True:
                print(cnt, ret)
            if cnt > time:
                break


class Trading:
    def __init__(self, logging=False):
        self.logging = logging

        self.stUtils = Utils()

        self.instCpTdUtil = win32com.client.Dispatch("CpTrade.CpTdUtil")
        self.instCpTd0311 = win32com.client.Dispatch("CpTrade.CpTd0311")

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

    def 주식_주문(self, stockName, 주문단가, 주문수량):
        SetInputValue_param = {
            '주문종류코드':0,
            '계좌번호':1,
            '상품관리구분코드':2,
            '종목코드':3,
            '주문수량':4,
            '주문단가':5,
            # 이하 생량
        }
        __매도 = 1
        __매수 = 2
        __내_계좌_번호 = self.instCpTdUtil.AccountNumber[0]
        print('__내_계좌_번호:', __내_계좌_번호)
        self.instCpTd0311.SetInputValue(SetInputValue_param['주문종류코드'], __매수)
        self.instCpTd0311.SetInputValue(SetInputValue_param['계좌번호'], __내_계좌_번호)
        stockCode = self.stUtils.get_code_from_name(stockName)
        self.instCpTd0311.SetInputValue(SetInputValue_param['종목코드'], stockCode)
        self.instCpTd0311.SetInputValue(SetInputValue_param['주문수량'], 주문수량)
        self.instCpTd0311.SetInputValue(SetInputValue_param['주문단가'], 주문단가)

        # 요청
        BlockRequest_result = self.instCpTd0311.BlockRequest()
        print('result:', BlockRequest_result)

        # 결과 조회 -> Subscribe 방식으로 확인 해야함
        
    def 주식_잔고_조회(self, bPrint=False):
        if bPrint == True:
            print('> 주식_잔고_조회')

        __계좌번호 = self.instCpTdUtil.AccountNumber[0]
        __주식상품_구분 = self.instCpTdUtil.GoodsList(__계좌번호, 1) # ?
        if bPrint == True:
            print('계좌번호 : %s, 주식상품_구분 : %s' % (__계좌번호, __주식상품_구분))
        
        input_value_field = {
            '계좌번호': 0,
            '상품관리구분코드': 1,
            '요청건수': 2
        }
        self.instCpTd6033.SetInputValue(input_value_field['계좌번호'], __계좌번호)  # 계좌번호
        self.instCpTd6033.SetInputValue(input_value_field['상품관리구분코드'], __주식상품_구분[0])  # 상품구분 - 주식 상품 중 첫번째
        self.instCpTd6033.SetInputValue(input_value_field['요청건수'], 50)  # 요청 건수(최대 50)
        # self.dicflag1 = {ord(' '): '현금',
        #                  ord('Y'): '융자',
        #                  ord('D'): '대주',
        #                  ord('B'): '담보',
        #                  ord('M'): '매입담보',
        #                  ord('P'): '플러스론',
        #                  ord('I'): '자기융자',
        #                  }

        return self.requestJango(bPrint)
    

    def requestJango(self, bPrint=False):
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
 
            header_value_field = {
                '수신개수': 7
            }
            cnt = self.instCpTd6033.GetHeaderValue(header_value_field['수신개수'])

            if bPrint == True:
                print(cnt)
 
            잔고 = 0
            ret_item_list = []
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
                ret_item_list.append(item)

            if bPrint == True:
                print('잔고 : %s' % format(잔고, ','))
            if self.instCpTd6033.Continue == False:
                break
        return ret_item_list


######################################################################
class CpEvent:
    def set_params(self, client, name, caller):
        self.client = client
        self.name = name
        self.caller = caller

    def OnReceived(self):
        if self.name == 'stockcur':
            print('stock_code:', self.client.GetHeaderValue(0),
            'stock_name:', self.client.GetHeaderValue(1),
            '매도호가:', self.client.GetHeaderValue(7),
            '매수호가:', self.client.GetHeaderValue(8),
            '누적거래량:', self.client.GetHeaderValue(9),
            '현재가:', self.client.GetHeaderValue(13),
            )
            
            # self.caller.test_result()

        elif self.name == 'conclusion':
            GetHeaderValue_param = {
                '계좌명':1,
                '종목명':2,
                '체결수량':3,
                '체결가격':4,
                '주문번호':5,
                '원주문번호':6,
                '계좌번호':7,
                '상품관리구분코드':8,
                '종목코드':9,
                '매매구분코드':12,
                '체결구분코드':14,
                '신용대출구분코드':15,
                # 이하 생략
            }
            
            print(
                '계좌명:', self.client.GetHeaderValue(GetHeaderValue_param['계좌명']),
                '종목명:', self.client.GetHeaderValue(GetHeaderValue_param['종목명']),
                '체결수량:', self.client.GetHeaderValue(GetHeaderValue_param['체결수량']),
                '체결가격:', self.client.GetHeaderValue(GetHeaderValue_param['체결가격']),
            )


class CpPublish:
    def __init__(self, name, service_id):
        self.name = name
        # self.instCpConclusion = win32com.client.Dispatch("DsCbo1.CpConclusion")
        self.obj = win32com.client.Dispatch(service_id)
        self.bIsSubscribe = False

    def subscribe(self, var, caller):
        if self.bIsSubscribe == True:
            self.unsubscribe()
            
        if len(var) > 0:
            self.obj.SetInputValue(0, var)
        
        __handler = win32com.client.WithEvents(self.obj, CpEvent)
        __handler.set_params(self.obj, self.name, caller)
        self.obj.Subscribe()
        self.bIsSubscribe = True

    def unsubscribe(self):
        if self.bIsSubscribe == True:
            self.obj.Unsubscribe()
            print(self.name, 'is unsubscribed')
        self.bIsSubscribe = False

    def test_result(self):
        print('end!')

class CpPBStockCur(CpPublish):
    def __init__(self):
        super().__init__('stockcur', 'DsCbo1.StockCur')

class CpPBConclusion(CpPublish):
    def __init__(self):
        super().__init__('conclusion', 'DsCbo1.CpConclusion')

######################################################################

class StockInfo:
    종목코드_음식료품 = 5

# MarketEye.
    # CreonMarketEye = {
    #     4  : '현재가',
    #     9  : '매수호가',
    #     '거래량' : 10,
    #     11 : '거래대금',
    #     20 : '총상장주식수',
    #     22 : '전일거래량',
    #     67 : 'PER',
    #     72 : '액면가',
    #     75 : '부채비율',
    #     77 : '자기자본이익률',
    #     78 : '매출액증가율',
    #     80 : '순이익증가율',
    #     89 : 'BPS'
    # }

    현재가_4 = 4 
    매수호가_9 = 9
    거래량_10 = 10          # **
    거래대금_11 = 11
    총상장주식수_20 = 20
    전일거래량_22 = 22      # **
    PER_67 = 67             # ** 주가/주당순이익
    액면가_72 = 72
    부채비율_75 = 75        # ** 대차대조표의 부채 총액을 자기자본으로 나눈 비율
    자기자본이익률_77 = 77  # **
    매출액증가율_78 = 78    # **
    순이익증가율_80 = 80    # **
    BPS_89 = 89            # **s 주당순자산

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

    def stockVolumeAnalysis(self, stockName, 몇배, days=60, bPrint=False):
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
            __거래량_배수 = round((volumes[0] / avgVolume), 3)
            if bPrint == True:
                print('(거래량 %s 배) %s 은(는) 대박 주! ' % (__거래량_배수, stockName))
            return __거래량_배수
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
    

