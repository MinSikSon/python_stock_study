from stock import creon

TRUE = 1
FALSE = 0

# global variables

if __name__ == '__main__':
    종목명 = '삼성전자'
    bViewAll = FALSE

    if creon.Connection(logging=True).check_connect() == TRUE :
        stUtils = creon.Utils()
        종목코드 = stUtils.get_code_from_name(종목명)
        print("%s 종목코드 : %s, 종목명 : %s" % (종목명, 종목코드, 종목명))

        print("[get_stock_value_n_days]")
        stUtils.get_stock_value_n_days(종목코드, days=1, bPrint=True)

        stStockInfo = creon.StockInfo()

        stStockInfo.GetInfo(종목명, creon.StockInfo.PER)
        
        # for i in range(len(종목리스트)):
        #     print('[%s. %s]' % (i, 종목리스트[i]))
        #     stStockInfo.GetPER(종목리스트[i])

        # print('이전 60일 대비 오늘 거래량 비율')
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

        몇배 = 1.5
        # buyList = []
        # for i in range(codeListLen):
        #     # if stStockInfo.stockVolumeAnalysis(종목리스트[i], 몇배) == 1:
        #     stStockInfo.stockVolumeAnalysis(종목리스트[i], 몇배)

        #         # buyList.append(종목리스트[i])
        #     time.sleep(1)

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
        request_type_list = (creon.StockInfo.현재가, creon.StockInfo.VOLUME, creon.StockInfo.거래대금, creon.StockInfo.PER, creon.StockInfo.BPS, creon.StockInfo.총상장주식수)
        for i in range(codeListLen):
            request_result_list = stStockInfo.GetInfo(종목리스트[i], requestType=request_type_list)
            print('현재가:%7s 원 || 0거래량:%10s 회 |1거래대금:%15s 원 |2총상장수식수:%13s 개 |3PER:%6s 배 |4BPS:%8s 원 [[종목명: %s]]' 
                % (
                format(request_result_list[0], ','), 
                format(request_result_list[1], ','), 
                format(request_result_list[2], ','), 
                format(request_result_list[3], ','), 
                round(request_result_list[4], 2),
                format(request_result_list[5], ','),
                종목리스트[i]))

        # 주식 잔고 및 거래 관련
        stTrading = creon.Trading(logging=True)
        잔고 = ''
        if stTrading.trade_init() == 0: # 0 : 성공
            잔고 = stTrading.주식_잔고_조회(bPrint=False)

            # request_type_list 에는 낮은 값 부터 넣어야 합니다.
            request_type_list = (creon.StockInfo.VOLUME, creon.StockInfo.거래대금, creon.StockInfo.PER, creon.StockInfo.BPS, creon.StockInfo.총상장주식수)
            for item in 잔고:
                request_result_list = stStockInfo.GetInfo(item['종목명'], requestType=request_type_list)
                print('현재가:%7s 원 || 잔고수량:%3s |0거래량:%10s 회 |1거래대금:%15s 원 |2총상장수식수:%13s 개 |3PER:%6s 배 |4BPS:%8s 원 [[종목명: %s]]' 
                    % (
                    format(item['현재가'], ','), 
                    item['잔고수량'], 
                    format(request_result_list[0], ','), 
                    format(request_result_list[1], ','), 
                    format(request_result_list[2], ','), 
                    round(request_result_list[3], 2),
                    format(request_result_list[4], ','),
                    item['종목명']))

