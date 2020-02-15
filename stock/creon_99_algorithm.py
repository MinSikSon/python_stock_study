from stock import utils

from stock import creon

from stock import creon_98_stocks_by_industry

from time import sleep

class Algorithm:
    관심_종목_리스트 = (
        '삼성전자',
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

    보유_종목_리스트 = (
        'CJ',
        '현대제철',
        '삼성전자',
        '금강공업',
        '아시아나항공',
        '케이맥',
        '셀트리온',
        '인터로조',
    )

    크레온_수수료 = 0.015 # %

    def __init__(self):
        self.stUtils = utils.Utils()
        self.stStockByIndustry = creon_98_stocks_by_industry.StocksByIndustry()

        self.stStockInfo = creon.StockInfo()

# 1. 현재 산업에서, 저평가된 종목 탐색 알고리즘
# return : 저평가 종목 리스트
    def algorithm_1(self):
        bViewAll = True
        if bViewAll == True:
            stockListByMarket = self.stStockByIndustry.getStockListByMarket(creon_98_stocks_by_industry.StocksByIndustry.MARKET['코스피'])
            stockListByMarketLen = len(stockListByMarket)
            print('stockListByMarketLen : %s' % (stockListByMarketLen))
            종목리스트 = []
            for i in range(stockListByMarketLen):
                name = self.stUtils.get_name_from_code(stockListByMarket[i])
                종목리스트.append(name)

        else:
            stockListByMarketLen = len(Algorithm.관심_종목_리스트)

# 현재가, 손익단가, 평가손익(천), 수익률, 평가금액(천), 잔고수량, 을 가져오도록
# cj : 82800, 110713, -725,    -25.26, 2147, 26
# 크레온 수수료..? 도 가져올 수 있도록 : 0.015% + 국가 세금 그냥 약 0.3 %
# 10000 10140  10200  9800 = 맞다.
# 그런 다음, 기타 정보를 산업 평균과 비교
    def algorithm_2(self):
        stTrading = creon.Trading()

        if stTrading.trade_init() == True:
            주식_잔고_리스트 = stTrading.주식_잔고_조회()

            for item in 주식_잔고_리스트:
                print(
                    '[종목명:', item['종목명'], ']',
                )
                print(
                    '  >'
                    ' 현재가:%7s'           % format(item['현재가'], ','),
                    '| 손익단가:%7s'        % format(item['손익단가'], ','),
                    '| 평가손익(천):%8s'    % format(item['평가손익'], ','),
                    '| 수익률:%6s'          % round(item['수익률'], 4), '%',
                    '| 평가금액:%10s'       % format(item['평가금액'], ','),
                    '| 잔고수량:%2s'        % item['잔고수량'],
                )


            stock_code_list = self.stStockByIndustry.getStockListByMarket(creon_98_stocks_by_industry.StocksByIndustry.MARKET['코스피'])
            stock_name_list = []
            # print(stock_code_list)
            for stock_code in stock_code_list:
                stock_name_list.append(self.stUtils.get_name_from_code(stock_code))

            print(stock_name_list)





# 적중 횟수 측정 (count) -> 기업들이 여러개
# 적중 횟수 / 수집 기간 => (%) 높은 ~ 낮은
# algorithm_3 : "금일 고가 > 전일 종가" 인 횟수를 counting
# 세금 : 매수, 매도 ==> 그냥 0.3 % 정도라고 생각하면 됨...
# "종가 < 다음날 고가" 비교할 때, 수수료도 포함 시켜야 더 정확하겠다.
    def algorithm_3(self, marketType=0):
        stTrading = creon.Trading()

        if stTrading.trade_init() == True:
            투자_후보_목록 = []

            # stTrading.주식_잔고_조회(bPrint=True)

            if marketType == 0:
                __markeyType = creon_98_stocks_by_industry.StocksByIndustry.MARKET['코스피']
            elif marketType == 1:
                __markeyType = creon_98_stocks_by_industry.StocksByIndustry.MARKET['코스닥']

            stock_code_list = self.stStockByIndustry.getStockListByMarket(__markeyType)
            stock_name_list = self.stUtils.get_nameList_from_codeList(stock_code_list)

            # stock_name_list = Algorithm.보유_종목_리스트
            # stock_code_list = self.stUtils.get_codeList_from_nameList(stock_name_list)

            # print(stock_code_list)
            # exit()
            # __name = 'SK하이닉스'
            # __name2 = '삼성전자'
            # stock_code_list = [self.stUtils.get_code_from_name(__name), self.stUtils.get_code_from_name(__name2)]
            # stock_name_list = [__name, __name2]

            print(stock_code_list)
            print(stock_name_list)

            날짜 = utils.Utils.InputValue_StockChart_Field_type['날짜']
            고가 = utils.Utils.InputValue_StockChart_Field_type['고가']
            종가 = utils.Utils.InputValue_StockChart_Field_type['종가']

            # __비교기간=500
            __비교기간=60
            __기대_조건성립률=93
            __기대_주가_대비_이익률=3
            bPrint=False
            for j in range(len(stock_code_list)):
                result = self.stUtils.get_stock_value_n_days(stock_code_list[j], __비교기간)
                
                실제비교기간=len(result)
                if 실제비교기간!=0:
                    비교횟수=실제비교기간-1
                    고저차=0
                    고저차누적=0
                    조건성립횟수=0
                    for i in range(실제비교기간):
                        if i < 실제비교기간-1:
                            고저차 = result[i][고가] - result[i+1][종가]
                            고저차누적 = 고저차누적 + 고저차
                            if result[i][고가] > result[i+1][종가]:
                                조건성립횟수+=1
                        if bPrint == True:
                            print('[%s][%s] 고가: %s, 종가: %s (고저차: %s, 고저차누적: %s)' 
                            % (i, result[i][날짜], result[i][고가], result[i][종가], 고저차, 고저차누적))

                    __금일종가=format(result[0][종가], ',')
                    __조건성립률=round(조건성립횟수/비교횟수*100, 2)
                    __평균고저차=round(고저차누적/비교횟수, 0)
                    __주가_대비_이익률=round(__평균고저차/result[0][종가]*100, 0)
                    if (__조건성립률 > __기대_조건성립률) & (__주가_대비_이익률 > __기대_주가_대비_이익률):
                        print('조건성립횟수: %s, 비교횟수: %s (성립률: %5s %%) (금일종가: %6s, 평균고저차: %5s => %4s %%) [종목명: %s]' 
                            % (조건성립횟수, 비교횟수, __조건성립률, __금일종가, __평균고저차, __주가_대비_이익률, stock_name_list[j]) )
                        투자_후보_목록.append(self.stUtils.get_name_from_code(stock_code_list[j]))
                else:
                    if bPrint == True:
                        print('[종목명: %s] 데이터 얻기 실패' % (stock_name_list[j]))

            return 투자_후보_목록


# 시나리오
# 장 중인지 확인
# >> 장 열릴 때까지 대기
# 장 열림!
# >> 평균고저차에 맞춰, 목표 수익률 계산
# 목표 수익률에 매도 등록
# 매도 완료 시 장 마감 2분 전까지 sleep
# 장 마감 1분 전, 현재 주가로 1 주 매수
# (처음으로 돌아가서 반복)
    def algorithm_4(self, 투자_후보_목록):
        __stock_market_start_time = self.stUtils.주식_장_시작_시간()
        __time_until_start = self.stUtils.시작_까지_남은_시간(True)
        __time_until_end = self.stUtils.마감_까지_남은_시간(True)

        while True:
# 장 중인지 확인
            print('# 장 중인지 확인')
            bIsStockMarketOpen = self.stUtils.장_중인지_확인()
            if bIsStockMarketOpen == False:
# >> 장 열릴 때까지 대기
                print('# >> 장 열릴 때까지 대기')
                while True:
                    sleep(1)
                    __time_until_start = self.stUtils.시작_까지_남은_시간()
                    print('주식 시작까지 남은 시간 : %s (%s)' % (__time_until_start, __time_until_start.total_seconds()))
                    if __time_until_start.total_seconds() < 0:
                        print('주식 장 시작!!!!!!!!!!!!!!!!!!!')
                        break
            else:
# 장 열림!
                print('# 장 열림!')
# >> 평균고저차에 맞춰, 목표 수익률 계산

# 장 마감 1분 전, 현재 주가로 1 주 매수

                pass
            
            