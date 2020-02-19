import win32com.client
import pythoncom

import datetime #https://datascienceschool.net/view-notebook/465066ac92ef4da3b0aba32f76d9750a/
import time

import stock.utils as utils

TRUE = 1
FALSE = 0

# 1. 초기화 및 크레온 접속 ?
# 2. 조회
# 3. 알고리즘 (todo)
# 4. 매매/매수
# 5. 결과 확인 (== 조회?)
# (6. 그래프)

class Trading:
    
    BlockRequest_ReturnValue = {
        '정상요청':0,
        '통신요청실패':1,
        '그외의내부오류':3
    }

    def __init__(self, logging=False):
        self.logging = logging

        self.stUtils = utils.Utils()

        self.instCpTdUtil = win32com.client.Dispatch("CpTrade.CpTdUtil")
        self.instCpTd0311 = win32com.client.Dispatch("CpTrade.CpTd0311")

        # 주식 잔고 조회
        self.instCpTd6033 = win32com.client.Dispatch("CpTrade.CpTd6033")

    # 거래 관련부 : init -> setinputvalue -> blockrequest
    def trade_init(self):
        bInitResult = self.instCpTdUtil.TradeInit()
        bReturn = False
        if bInitResult == 0:
            if self.logging == True:
                print('[tradeInit] 성공')
            bReturn = True
        elif bInitResult == -1:
            print('[tradeInit] 오류')
        elif bInitResult == 1:
            print('[tradeInit] OTP/보안카드 키 입력 잘못 됨')
        elif bInitResult == 3:
            print('[tradeInit] 취소')
        else:
            print('[tradeInit] ??')
        return bReturn


    def 주식_주문(self, 매매, stockName, 주문단가, 주문수량, bPrint=False, bTest=False):
        SetInputValue_param = {
            '주문종류코드':0,
            '계좌번호':1,
            '상품관리구분코드':2,
            '종목코드':3,
            '주문수량':4,
            '주문단가':5,
            '주문조건구분코드':7,
            '주문호가구분코드':8,

            # 이하 생략
        }

        if ((매매 == 1) | (매매 == 2)) == False:
            print('[param] 매매 를 1(매도) 또는 2(매수)로 지정하세요')
            return
        __내_계좌_번호 = self.instCpTdUtil.AccountNumber[0]
        if bPrint == True:
            print('__내_계좌_번호:', __내_계좌_번호)
        __상품관리구분코드 = {
            '주식':1,
            '선물/옵션':2,
            'EUREX':16,
            '해외선물':64,
        } # __상품관리구분코드['주식'] + __상품관리구분코드['선물/옵션'] 요런 식으로 사용 가능함
        __상품_목록 = self.instCpTdUtil.GoodsList(__내_계좌_번호, __상품관리구분코드['주식']) # __상품_목록은 배열임..!
        if bPrint == True:
            print(__상품_목록)
        self.instCpTd0311.SetInputValue(SetInputValue_param['주문종류코드'], 매매) # 1: 매도, 2: 매수
        self.instCpTd0311.SetInputValue(SetInputValue_param['계좌번호'], __내_계좌_번호)
        self.instCpTd0311.SetInputValue(SetInputValue_param['상품관리구분코드'], __상품_목록[0]) # 
        stockCode = self.stUtils.get_code_from_name(stockName)
        self.instCpTd0311.SetInputValue(SetInputValue_param['종목코드'], stockCode)
        self.instCpTd0311.SetInputValue(SetInputValue_param['주문수량'], 주문수량)
        self.instCpTd0311.SetInputValue(SetInputValue_param['주문단가'], 주문단가)
        self.instCpTd0311.SetInputValue(SetInputValue_param['주문조건구분코드'], '0') # '0' : 없음 [default]
        self.instCpTd0311.SetInputValue(SetInputValue_param['주문호가구분코드'], '01') # '01' : 보통 [default]

        # 요청
        if bTest == False:
            BlockRequest_result = self.instCpTd0311.BlockRequest()
            if BlockRequest_result == self.BlockRequest_ReturnValue['정상요청']:
                if 매매 == 1: # 매도
                    print('[주식_주문] result: 정상 요청 (%s 매도)' % (stockName))
                elif 매매 == 2: # 매수
                    print('[주식_주문] result: 정상 요청 (%s 매수)' % (stockName))
            else:
                print('[주식_주문] result: 문제 발생')

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
                item['현재가'] = __n_days_list[0][2] # 시가
                item['대비'] = 0
                item['거래량'] = 0

                # 추가한 정보
                item['손익단가'] = self.instCpTd6033.GetDataValue(18, i)
                item['평가손익'] = self.instCpTd6033.GetDataValue(10, i)
                item['수익률'] = self.instCpTd6033.GetDataValue(11, i)
                item['평가금액'] = self.instCpTd6033.GetDataValue(9, i)

 
                합계 = item['잔고수량'] * item['현재가']
                if bPrint == True:
                    print('%s : 잔고수량(%s) * 현재가(%s) = (%s) (매도가능? %s)' % (item['종목명'], item['잔고수량'], item['현재가'], 합계, item['매도가능']))
                잔고 = 잔고 + 합계
                ret_item_list.append(item)

            if bPrint == True:
                print('잔고 : %s' % format(잔고, ','))
            if self.instCpTd6033.Continue == False: # README.md 의 '3. RQ/RP 의 연속 data 통신' 참고
                break
        return ret_item_list

class StockInfo:
    현재가_4 = 4 
    고가_6 = 6
    매수호가_9 = 9
    거래량_10 = 10          # **
    거래대금_11 = 11
    종목명_17 = 17
    총상장주식수_20 = 20
    전일거래량_22 = 22      # **
    전일종가_23 = 23
    PER_67 = 67             # ** 주가/주당순이익
    액면가_72 = 72
    부채비율_75 = 75        # ** 대차대조표의 부채 총액을 자기자본으로 나눈 비율
    자기자본이익률_77 = 77  # **
    매출액증가율_78 = 78    # **
    순이익증가율_80 = 80    # **
    BPS_89 = 89            # **s 주당순자산

    def __init__(self):
        self.stUtils = utils.Utils()

        self.instMarketEye = win32com.client.Dispatch("CpSysDib.MarketEye")

    def getRequestTypeListBrief(self):
        request_type_list = (
            StockInfo.현재가_4,
            StockInfo.거래량_10,
            StockInfo.PER_67,
            StockInfo.BPS_89
        )
        return request_type_list

    def printRequestTypeListBrief(self, result):
        print(
            '    >',
            '현재가:'  , format(result[0], ','), '원 |',
            '거래량:'  , format(result[1], ','), '회 |',
            'PER:'    , format(round(result[2], 2), ','), '배 |',
            'BPS:'    , format(result[3], ','), '원',
        )

    def getRequestTypeListDetailed(self):
        request_type_list = (
            StockInfo.현재가_4,
            StockInfo.고가_6,
            StockInfo.거래량_10,
            StockInfo.거래대금_11,
            StockInfo.총상장주식수_20,
            StockInfo.전일종가_23,
            StockInfo.PER_67,
            StockInfo.BPS_89
        )
        return request_type_list

    def printRequestTypeListDetailed(self, result):
        print(
            '    >',
            '현재가:'  , format(result[0], ','), '원 |',
            '고가:'    , format(result[1], ','), '원 |',
            '거래량:'  , format(result[2], ','), '회 |',
            '거래대금:', format(result[3], ','), '원 |',
            '총상장주식수', format(result[4], ','), '개 |',
            '전일종가', format(result[5], ','), '원 |',
            'PER:'    , format(round(result[6], 2), ','), '배 |',
            'BPS:'    , format(result[7], ','), '원',
        )

    

    def getInfo(self, stockName, requestType):
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

    def getInfoSimple(self, stockName, bPrint=False):
        request_result_list = self.getInfo(stockName, self.getRequestTypeListBrief())
        if bPrint == True:
            self.printRequestTypeListBrief(request_result_list)
        return request_result_list

    def getInfoDetail(self, stockName, bPrint=False):
        request_result_list = self.getInfo(stockName, self.getRequestTypeListDetailed())
        if bPrint == True:
            self.printRequestTypeListDetailed(request_result_list)
        return request_result_list

    def stockVolumeAnalysis(self, stockName, 몇배수, 비교기간=60, bPrint=False):
        __stockCode = self.stUtils.get_code_from_name(stockName)
        __거래량 = 8
        self.stUtils.set_stock_chart_info_and_request(__stockCode, ord('2'), 비교기간, __거래량,  ord('D'), ord('1'))

        # server 에서 data 받아옴
        volumes = []
        __수신개수 = 3
        __numData = self.stUtils.instStockChart.GetHeaderValue(__수신개수) # 비교기간 이랑 같을 듯.

        __종목코드 = 0
        for i in range(__numData):
            volume = self.stUtils.instStockChart.GetDataValue(__종목코드, i)
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
        if volumes[0] > avgVolume * 몇배수:
            __거래량_배수 = round((volumes[0] / avgVolume), 3)
            if bPrint == True:
                print('(거래량 %s 배) %s 은(는) 대박 주! ' % (__거래량_배수, stockName))
            return __거래량_배수
        else:
            return 0
            #print('(거래량 %s 배) %s 은(는) 일반 주.. ' % (round((volumes[0] / avgVolume), 3), stockName))

