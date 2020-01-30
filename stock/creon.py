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
    def __init__(self, logging=False):
        self.logging = logging

        self.stUtils = utils.Utils()

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

class StockInfo:
    현재가_4 = 4 
    매수호가_9 = 9
    거래량_10 = 10          # **
    거래대금_11 = 11
    종목명_17 = 17
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
        self.stUtils = utils.Utils()

        self.instMarketEye = win32com.client.Dispatch("CpSysDib.MarketEye")

        self.instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")

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
            StockInfo.거래량_10,
            StockInfo.거래대금_11,
            StockInfo.총상장주식수_20,
            StockInfo.PER_67,
            StockInfo.BPS_89
        )
        return request_type_list

    def printRequestTypeListDetailed(self, result):
        print(
            '    >',
            '현재가:'  , format(result[0], ','), '원 |',
            '거래량:'  , format(result[1], ','), '회 |',
            '거래대금:', format(result[2], ','), '원 |',
            '총상장주식수', format(result[3], ','), '개 |',
            'PER:'    , format(round(result[4], 2), ','), '배 |',
            'BPS:'    , format(result[5], ','), '원',
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
        return 

    def stockVolumeAnalysis(self, stockName, 몇배수, 비교기간=60, bPrint=False):
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
        self.stUtils.set_stock_chart_info(__stockCode, ord('2'), 비교기간, __거래량,  ord('D'), ord('1'))

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
        if volumes[0] > avgVolume * 몇배수:
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

