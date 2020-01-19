from stock import creon

TRUE = 1
FALSE = 0

# global variables
확인종목 = '삼성전자'
bViewAll = FALSE

if __name__ == '__main__':
    stCreon = creon.Creon()
    bConnect = stCreon.check_connect()

    if bConnect == TRUE :
        # TEST
        code = stCreon.get_code_from_name(확인종목)
        name = stCreon.get_name_from_code(code)
        print("%s code : %s, name : %s" % (확인종목, code, name))

        stCreon.get_stock_value_n_days(code, 1)

        stCreon.GetPER(확인종목)

        

        # for i in range(len(확인종목List)):
        #     print('[%s. %s]' % (i, 확인종목List[i]))
        #     stCreon.GetPER(확인종목List[i])

        # print('이전 60일 대비 오늘 거래량 비율')
        if bViewAll == 1:
            codeList = stCreon.getStockListByMarket()
            codeListLen = len(codeList)
            print('codeListLen : %s' % (codeListLen))
            확인종목List = []
            for i in range(codeListLen):
                name = stCreon.get_name_from_code(codeList[i])
                확인종목List.append(name)

        else:
            확인종목List = ('삼성전자',
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
            codeListLen = len(확인종목List)

        몇배 = 1.5
        # buyList = []
        # for i in range(codeListLen):
        #     # if stCreon.stockVolumeAnalysis(확인종목List[i], 몇배) == 1:
        #     stCreon.stockVolumeAnalysis(확인종목List[i], 몇배)

        #         # buyList.append(확인종목List[i])
        #     time.sleep(1)

        # stCreon.업종_별_코드_리스트()

        # 음식료품_코드_리스트 = stCreon.업종_내_종목_코드_리스트(stCreon.종목코드_음식료품)

        # sumPER = 0
        # sumCount = 0
        # for stockCode in 음식료품_코드_리스트:
        #     name = stCreon.get_name_from_code(stockCode)
        #     if stCreon.stockVolumeAnalysis(name, 몇배) == 1:
        #         buyList.append(name)
                
        #     PER = stCreon.GetPER(name)[0]
        #     if PER > 0:
        #         sumPER += PER
        #         sumCount += 1
        #     # time.sleep(1)
        
        # print('sumPER %s' % (sumPER))
        # print('sumCount %s' % (sumCount))
        # print('avg PER = %s' % (round((sumPER/sumCount), 4)))


        # 주식 거래 관련
        # print(stCreon.tradeInit()) 

        if stCreon.tradeInit() == 0: # 0 : 성공
            stCreon.주식_잔고_조회()