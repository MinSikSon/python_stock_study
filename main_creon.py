from stock import creon
from stock import creon_0_Init
from stock import creon_1_SB_PB
# from stock.creon import Trading
from time import sleep

from stock import utils

import pythoncom

TRUE = 1
FALSE = 0

# global variables

if __name__ == '__main__':
    bViewAll = FALSE

    if creon_0_Init.Connection(logging=False).check_connect() == TRUE :
        stUtils = utils.Utils()

        stStockInfo = creon.StockInfo()

        if bViewAll == 1:
            codeList = stStockInfo.getStockListByMarket()
            codeListLen = len(codeList)
            print('codeListLen : %s' % (codeListLen))
            종목리스트 = []
            for i in range(codeListLen):
                name = stUtils.get_name_from_code(codeList[i])
                종목리스트.append(name)

        else:
            종목리스트 = ('삼성전자',
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
            codeListLen = len(종목리스트)

# 주식 잔고 및 거래 관련
        stTrading = creon.Trading(logging=True)
        잔고 = ''
        if stTrading.trade_init() == 0: # 0 : 성공
            잔고 = stTrading.주식_잔고_조회(bPrint=False)

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

# 매수 (실시간 거래 가능시간 09:00 ~ 15:20)
            # stCpConclusion = creon.CpPBConclusion()
            stCpStockCur = creon_1_SB_PB.CpPBStockCur()
            stCpPBConclusion = creon_1_SB_PB.CpPBConclusion()
            # for item in 잔고:
                # code = stUtils.get_code_from_name(item['종목명'])
                # stCpStockCur.subscribe(code, stCpStockCur)
            __stock_name = '삼성전자'
            code = stUtils.get_code_from_name(__stock_name)
            stCpStockCur.subscribe(code, stCpStockCur) # 실시간 거래 가능시간 이외에는, 현재가 고정이기 때문에 subscribe 해도 받는(receive)게 없다.

            # 체결 역시 마찬가지로, 결과를 알 수 없다. 지금 매수/매매를 걸어도 received 되는게 없기 때문에,,!
            code = stUtils.get_code_from_name(__stock_name)
            # stCpStockCur.subscribe(code, stCpStockCur) # 현재가 고정이기 때문에, subscribe 해도, 받는(receive)게 없을 듯?
            stCpPBConclusion.subscribe('', stCpPBConclusion) #
            # 내일 확인해보자!!

            # 매수
            # stTrading.주식_주문(__stock_name, 58800, 1) # 26000 원에 1주 매수

            # waiting
            # stUtils.waiting(5, log='Conclusion response',bPrint=True)
            cnt = 0
            expiration_time = 5 # sec
            while True:
                ret = pythoncom.PumpWaitingMessages() # [?] pythoncom 에 빨간줄 왜 생길까?
                cnt = cnt + 1
                sleep(1)
                # test
                current_stock_value = stCpStockCur.get_test_result()
                print('current_stock_value:', current_stock_value)
                if current_stock_value != 0:
                    # stTrading.주식_주문(__stock_name, current_stock_value-500, 1) # 현재가 보다 500 원 낮은 가격에 1주 매수
                    break
                # test end

                # if bPrint == True:
                # print('waiting', '...(', cnt, ret, ')')
                if cnt > expiration_time:
                    break

            stCpStockCur.unsubscribe()
            stCpPBConclusion.unsubscribe()
