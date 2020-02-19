####################################################
# CREON, subscribe/publish module

import win32com.client

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
            
            self.caller.test_result(self.client.GetHeaderValue(13))

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

            self.caller.complete = True # 체결

class CpPublish:
    def __init__(self, name, service_id):
        self.name = name
        # self.instCpConclusion = win32com.client.Dispatch("DsCbo1.CpConclusion")
        self.obj = win32com.client.Dispatch(service_id)
        self.bIsSubscribe = False
        self.local_value = 0
        self.complete = False

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

    def test_result(self, value): # for test
        if self.name == 'stockcur':
            self.local_value = value
        print('end!')

    def get_test_result(self):
        return self.local_value

    def get_conclusion(self):
        return self.complete

class CpPBStockCur(CpPublish):
    def __init__(self):
        super().__init__('stockcur', 'DsCbo1.StockCur')

    def getCurrentStockValue(self):
        return super().get_test_result()

class CpPBConclusion(CpPublish):
    def __init__(self):
        super().__init__('conclusion', 'DsCbo1.CpConclusion')
        
    def getConclusion(self):
        return super().get_conclusion()