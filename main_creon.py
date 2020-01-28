from stock import creon
from stock.creon import StockInfo
# from stock.creon import Trading
from time import sleep

TRUE = 1
FALSE = 0

# global variables

if __name__ == '__main__':
    bViewAll = FALSE

    if creon.Connection(logging=False).check_connect() == TRUE :
        stUtils = creon.Utils()

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

# 알고리즘?
        # print('거래 기간 대비 오늘 거래량 상승폭')
        몇배 = 1.5
        __days = 10
        # buyList = []
        # for i in range(codeListLen):
        #     if stStockInfo.stockVolumeAnalysis(종목리스트[i], 몇배, days=__days) == 1:
        #         buyList.append(종목리스트[i])
        # print('buyList : %s' % (buyList))

        # exit()

        # stStockInfo.업종_별_코드_리스트()

        # 음식료품_코드_리스트 = stStockInfo.업종_내_종목_코드_리스트(stStockInfo.종목코드_음식료품)

        # sumPER = 0
        # sumCount = 0
        # for stockCode in 음식료품_코드_리스트:
        #     name = stStockInfo.get_name_from_code(stockCode)
        #     if stStockInfo.stockVolumeAnalysis(name, 몇배) == 1:
        #         buyList.append(name)
                
        #     PER = stStockInfo.GetPER(name)[0]
        #     if PER > 0:
        #         sumPER += PER
        #         sumCount += 1
        #     # time.sleep(1)
        
        # print('sumPER %s' % (sumPER))
        # print('sumCount %s' % (sumCount))
        # print('avg PER = %s' % (round((sumPER/sumCount), 4)))

# 종목리스트 관련
        request_type_list = (StockInfo.현재가_4, 
                            StockInfo.거래량_10, 
                            StockInfo.거래대금_11, 
                            StockInfo.총상장주식수_20,
                            StockInfo.PER_67, 
                            StockInfo.BPS_89
                            )
        # for i in range(codeListLen):
        #     request_result_list = stStockInfo.GetInfo(종목리스트[i], requestType=request_type_list)
        #     print('현재가:%7s 원 || 0거래량:%10s 회 |1거래대금:%15s 원 |2총상장수식수:%13s 개 |3PER:%6s 배 |4BPS:%8s 원 [[종목명: %s]]' 
        #         % (
        #         format(request_result_list[0], ','), 
        #         format(request_result_list[1], ','), 
        #         format(request_result_list[2], ','), 
        #         format(request_result_list[3], ','), 
        #         round(request_result_list[4], 2),
        #         format(request_result_list[5], ','),
        #         종목리스트[i]))

# 주식 잔고 및 거래 관련
        stTrading = creon.Trading(logging=True)
        잔고 = ''
        if stTrading.trade_init() == 0: # 0 : 성공
            잔고 = stTrading.주식_잔고_조회(bPrint=False)

            # request_type_list 에는 낮은 값 부터 넣어야 합니다.
            종목리스트_구매 = []
            # request_type_list = (creon.StockInfo.VOLUME, creon.StockInfo.거래대금, creon.StockInfo.PER, creon.StockInfo.BPS, creon.StockInfo.총상장주식수)
            request_type_list = (StockInfo.현재가_4, 
                    StockInfo.거래량_10, 
                    StockInfo.거래대금_11, 
                    StockInfo.총상장주식수_20,
                    StockInfo.PER_67, 
                    StockInfo.BPS_89
                    )
            
            for item in 잔고:
                request_result_list = stStockInfo.GetInfo(item['종목명'], requestType=request_type_list)
                종목리스트_구매.append(item['종목명'])

                # 거래량 증가폭
                __거래량_배수 = stStockInfo.stockVolumeAnalysis(item['종목명'], 0.1, 30)
                # 결과값들 출력
                print(
                    '현재가:'  , format(request_result_list[0], ','), '원 |',
                    '잔고수량:', item['잔고수량'], '|',
                    '거래량:'  , format(request_result_list[1], ','), '회',
                    '(',__거래량_배수,'배)',
                    # '거래대금:', format(request_result_list[2], ','), '원',
                    # '총상장주식수', format(request_result_list[3], ','), '개',
                    'PER:'    , format(round(request_result_list[4], 2), ','), '배',
                    'BPS:'    , format(request_result_list[5], ','), '원',
                    '[[종목명:', item['종목명'], ']]')
                # print(request_result_list, item['종목명'])


# 매수
            # stCpConclusion = creon.CpPBConclusion()
            stCpStockCur = creon.CpPBStockCur()
            stCpPBConclusion = creon.CpPBConclusion()
            # for item in 잔고:
                # code = stUtils.get_code_from_name(item['종목명'])
                # stCpStockCur.subscribe(code, stCpStockCur)
            # code = stUtils.get_code_from_name('삼성전자')
            # stCpStockCur.subscribe(code, stCpStockCur) # 현재가 고정이기 때문에, subscribe 해도, 받는(receive)게 없을 듯?
            # 체결 역시 마찬가지로, 결과를 알 수 없다. 지금 매수/매매를 걸어도 received 되는게 없기 때문에,,!
            code = stUtils.get_code_from_name('삼성전자')
            # stCpStockCur.subscribe(code, stCpStockCur) # 현재가 고정이기 때문에, subscribe 해도, 받는(receive)게 없을 듯?
            stCpPBConclusion.subscribe('', stCpPBConclusion)
            # 내일 확인해보자!!
            
            # 매수 (실시간 거래 가능시간 09:00 ~ 15:20)
            # stTrading.주식_주문('삼성전자', 58800, 1) # 26000 원에 1주 매수

            # waiting
            stUtils.waiting(100, False)
            
            # stCpStockCur.unsubscribe()
            stCpPBConclusion.unsubscribe()
