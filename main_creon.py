from stock import creon
from stock import creon_0_Init
from stock import creon_1_SB_PB
from stock import creon_98_stocks_by_industry
# from stock.creon import Trading
from time import sleep

from stock import utils

import pythoncom

from stock import creon_99_algorithm

from getpass import getpass

# global variables

if __name__ == '__main__':
    stInit = creon_0_Init.Connection(logging=False)
    stInit.kill_creon()
    print('########## CREON Login ##########')
    __id = input('id: ')
    __pwd = getpass('pwd: ')
    __pwdcert = getpass('pwdcert: ')
    print('########## ########### ##########')
    if stInit.run_creon(__id, __pwd, __pwdcert) == True :
############################################################################
# test
        stAlgorithm = creon_99_algorithm.Algorithm()

        # stAlgorithm.algorithm_2()
        stAlgorithm.algorithm_4()
        
        exit()
############################################################################

        stUtils = utils.Utils()

        stStockInfo = creon.StockInfo()

# 주식 잔고 및 거래 관련
        stTrading = creon.Trading(logging=True)
        잔고 = ''
        if stTrading.trade_init() == True:
            잔고 = stTrading.주식_잔고_조회(bPrint=True)

            for item in 잔고:
                # 거래량 증가폭
                __배수 = 0.1
                __비교기간 = 30
                __거래량_배수 = stStockInfo.stockVolumeAnalysis(item['종목명'], __배수, __비교기간)
                print(
                    '[[종목명:', item['종목명'], ']]',
                    '잔고수량:', item['잔고수량'], '|',
                    '(거래량 배수:',__거래량_배수,'배)',
                )
                stStockInfo.getInfoDetail(item['종목명'], bPrint=True)

# 매수 (실시간 거래 가능시간 '09:00 ~ 15:20' 에만 SB/PB 가 정상 동작한다)
            stCpStockCur = creon_1_SB_PB.CpPBStockCur()
            stCpPBConclusion = creon_1_SB_PB.CpPBConclusion()
            # for item in 잔고:
                # code = stUtils.get_code_from_name(item['종목명'])
                # stCpStockCur.subscribe(code, stCpStockCur)
            __stock_name = '삼성전자'
            code = stUtils.get_code_from_name(__stock_name)
            stCpStockCur.subscribe(code, stCpStockCur) # 실시간 거래 가능시간 이외에는, 현재가 고정이기 때문에 subscribe 해도 받는(receive)게 없다.

            code = stUtils.get_code_from_name(__stock_name)
            stCpStockCur.subscribe(code, stCpStockCur)
            stCpPBConclusion.subscribe('', stCpPBConclusion)

            # 매수
            # stTrading.주식_주문(__stock_name, 58800, 1) # 26000 원에 1주 매수

            # waiting
            cnt = 0
            expiration_time = 5 # sec
            while True:
                # ret = pythoncom.PumpWaitingMessages() # [?] pythoncom 에 빨간줄 왜 생길까?
                cnt = cnt + 1
                sleep(1)
                # test
                current_stock_value = stCpStockCur.get_test_result()
                print('current_stock_value:', current_stock_value)
                if True | current_stock_value != 0:
                    stTrading.주식_주문(creon.Trading.매매['매수'], __stock_name, current_stock_value - 500, 1, bTest=True) # 현재가 보다 500 원 낮은 가격에 1주 매수
                    
                    stCpStockCur.unsubscribe()
                    break
                # test end

                # if bPrint == True:
                # print('waiting', '...(cnt:', cnt, ')')
                if cnt > expiration_time:
                    break

            stUtils.waiting(5, log='Conclusion response',bPrint=True)

            stCpPBConclusion.unsubscribe()
