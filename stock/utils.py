import win32com.client
import pythoncom
from time import sleep
import datetime

class Utils:
    # 0: 날짜, 1: 시간, 2: 시가, 3: 고가, 4: 저가, 5: 종가, 6: 전일대비, 8: 거래량, 9: 거래대금, 10: 누적체결매도수량

    InputValue_StockChart_Field_type = {
        '날짜':0,
        '시간':1,
        '시가':2,
        '고가':3,
        '저가':4,
        '종가':5,
        '전일대비':6,
        '거래량':8,
        '거래대금':9,
        '누적체결매도수량':10
    }

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

    def get_codeList_from_nameList(self, nameList):
        codeList = []
        for i in range(len(nameList)):
            codeList.append(self.get_code_from_name(nameList[i]))
        
        return codeList

    def get_name_from_code(self, code):
        return self.instCpStockCode.CodeToName(code)

    def get_nameList_from_codeList(self, codeList):
        nameList = []
        for i in range(len(codeList)):
            nameList.append(self.get_name_from_code(codeList[i]))
        
        return nameList

    def set_stock_chart_info_and_request(self, 종목코드, 조회방법, 요청기간_또는_요청일수, 요청할_데이터_종류=(0, 1, 2, 3, 4, 5, 6, 8, 9, 10), 차트종류=ord('D'), 수정주가반영여부=ord('1')):
        self.instStockChart.SetInputValue(self.종목_코드, 종목코드)
        self.instStockChart.SetInputValue(self.조회방법, 조회방법) # 1: 조회 기간, 2: 조회 개수 
        self.instStockChart.SetInputValue(self.요청_개수, 요청기간_또는_요청일수)
        # self.instStockChart.SetInputValue(__dataType, 5) # 5: 종가
        self.instStockChart.SetInputValue(self.요청할_데이터의_종류, 요청할_데이터_종류) # 0: 날짜, 1: 시간, 2: 시가, 3: 고가, 4: 저가, 5: 종가, 6: 전일대비, 8: 거래량, 9: 거래대금, 10: 누적체결매도수량
        self.instStockChart.SetInputValue(self.차트의_종류, 차트종류) # D : day
        self.instStockChart.SetInputValue(self.수정_주가_반영_여부, 수정주가반영여부)


        self.instStockChart.BlockRequest() # request data from the server

    def get_stock_value_n_days(self, stockCode, days, bPrint=False): # https://wikidocs.net/3684
        if bPrint == True:
            print('code : %s, name : %s' % (stockCode, self.get_name_from_code(stockCode)))

        #(dataType, InputData)
        __dataTypeList = (0, 1, 2, 3, 4, 5, 6, 8, 9, 10) # 0: 날짜, 1: 시간, 2: 시가, 3: 고가, 4: 저가, 5: 종가, 6: 전일대비, 8: 거래량, 9: 거래대금, 10: 누적체결매도수량
        self.set_stock_chart_info_and_request(stockCode, ord('2'), days, __dataTypeList, ord('D'), ord('1'))

        __numData = self.instStockChart.GetHeaderValue(3) # response. receive data from the server
        if bPrint == True:
            print('numData : %s' % __numData)

        # __dateTime = datetime.datetime.now()
        # __weekday = __dateTime.weekday()
        __stockValueList = []
        for i in range(__numData):
            __stockValue = []
            for j in range(len(__dataTypeList)):
                __stockValue.append(self.instStockChart.GetDataValue(j, i))
            if bPrint == True:
                print('%s' % __stockValue)
            __stockValueList.append(__stockValue)

        return __stockValueList

    def waiting(self, time, log='', bPrint=False):
        cnt = 0
        while True:
            # ret = pythoncom.PumpWaitingMessages() # [?] pythoncom 에 빨간줄 왜 생길까?
            cnt = cnt + 1
            sleep(1)
            if bPrint == True:
                print('waiting',log, '...(cnt: ', cnt, ')')
            if cnt > time:
                break


    def calculateTax(self, buying, selling):
        # 매도 금액 - 매수 금액 - 매수 수수료 - 매도 수수료 - 매도 세금 > 0
        __selling_fee =0.015
        __buying_fee =0.015
        __selling_tax =0.3
        __profit = selling - buying - (buying * __buying_fee) - (selling * __selling_fee) - (selling * __selling_tax)
        return __profit

    def 주식_장_시간_시간(self, bPrint=False):
        __start_time = datetime.datetime(year=2020, month=1, day=1, hour=9, minute=0, second=0)
        if bPrint == True:
            print('%s:%s ~' % (__start_time.hour, __start_time.minute))
        return __start_time

    def 주식_장_마감_시간(self, bPrint=False):
        # 09:00 ~ 15:30
        __end_time = datetime.datetime(year=2020, month=1, day=1, hour=15, minute=30, second=0)
        if bPrint == True:
            print('~ %s:%s' % (__end_time.hour, __end_time.minute))
        return __end_time

    def 현재_시간(self, bPrint=False):
        __cur_time = datetime.datetime.today()
        if bPrint == True:
            print('현재 시간 : %s' % (__cur_time))
        
        return __cur_time

    def 마감_까지_남은_시간_분_단위로_확인(self, bPrint=False):
        __start_time = self.주식_장_시간_시간()
        __end_time = self.주식_장_마감_시간()
        __cur_time = self.현재_시간()

        __diff_min = 0
        if (__start_time.hour <= __cur_time.hour) & (__cur_time.hour <= __end_time.hour) & (__start_time.minute <= __cur_time.minute) & (__cur_time.minute < __end_time.minute):
            print('in')
            __cur_minute = __cur_time.hour * 60 + __cur_time.minute
            __end_minute = __end_time.hour * 60 + __end_time.minute
            __diff_min = __end_minute - __cur_minute
        else:
            __cur_minute = __cur_time.hour * 60 + __cur_time.minute
            __start_minute = __start_time.hour * 60 + __start_time.minute
            if __cur_minute > __start_minute:
                __diff_min = __start_minute - __cur_minute + (24 * 60)
            else:
                __diff_min = -(__start_minute - __cur_minute)

        if bPrint == True:
            print('__diff : %s' % (__diff_min))

        return __diff_min

    def 마감_까지_남은_시간_초_단위로_확인(self, bPrint=False):
        __start_time = self.주식_장_시간_시간()
        __end_time = self.주식_장_마감_시간()
        __cur_time = self.현재_시간()

        __diff = 0
        if (__start_time.hour <= __cur_time.hour) & (__cur_time.hour <= __end_time.hour) & (__start_time.minute <= __cur_time.minute) & (__cur_time.minute < __end_time.minute):
            print('in')
            __cur = __cur_time.hour * 3600 + __cur_time.minute * 60 + __cur_time.second
            __end = __end_time.hour * 3600 + __end_time.minute * 60 + __end_time.second
            __diff = __end - __cur
        else:
            __cur = __cur_time.hour * 3600 + __cur_time.minute * 60 + __cur_time.second
            __start = __start_time.hour * 3600 + __start_time.minute * 60 + __start_time.second
            if __cur > __start:
                __diff = __start - __cur + (24 * 60 * 60)
            else:
                __diff = -(__start - __cur)

        if bPrint == True:
            print('__diff : %s' % (__diff))

        return __diff