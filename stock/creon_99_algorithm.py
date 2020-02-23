from stock import utils

from stock import creon

from stock import creon_98_stocks_by_industry

from time import sleep

from stock import creon_1_SB_PB

from stock import creon_0_Init

from stock import login # .gitignore

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

    후보군_종목_리스트 = (
        '삼륭물산',
        '우진비앤지',
        '럭슬',
        'SFA반도체',
        '아이씨디',
        '인프라웨어',
        '에스텍파마',
        '큐브앤컴퍼니',
        '에이치엘비파워',
        '오픈베이스',
        '인터플렉스',
        '오성첨단소재',
        '제일바이오',
        'APS홀딩스',
        '신스타임즈',
        '에이치엘비생명과학',
        '유비쿼스홀딩스',
        '한양디지텍',
        '두올산업',
        '디이엔티',
        '젬백스',
        '루미마이크로',
        '수성',
        '아이티엠반도체',
        '진바이오텍',
        '이원컴포텍',
        '켐트로닉스',
        '제이티',
        'SDN',
        '파인테크닉스',
        '우리넷',
        '엠에스오토텍',
        '키네마스터',
        '메지온',
        '포티스',
        '세경하이테크',
        '인트로메딕',
        '스타모빌리티',
        '유테크',
        '테라셈',
        '알테오젠',
        '텔콘RF제약',
        '액션스퀘어',
        '미스터블루',
        '셀바스헬스케어',
        '신라젠',
        '제테마',
        '제너셈',
        '핸디소프트',
        '한류AI센터',
        '마이크로텍',
        '줌인터넷',
        '케이피에스',
        '이더블유케이',
        '알리코제약',
        '데이타솔류션',
        '셀리버리',
        '압타바이오',
        '에이비엘바이오',
        '라온피플',
        '티움바이오',
        '티라유텍'
        )

        # 0218 매수 종목
    매수_목록_0218 = (
        '삼륭물산',
        '우진비앤지',
        '아이씨디',
        '제일바이오',
        'APS홀딩스'
    )

    매수_목록_0220 = (
        '파인테크닉스',
        '이더블유케이',
        '인프라웨어',
        '에이치엘비파워',
        '제일바이오',
    )

    매도_가격_0220 = (
        4060,
        15200,
        1285,
        1425,
        9000 # 8995 였는데, 자리수 맞췄어야 함, 
    )

    크레온_수수료 = 0.015 # %

    def __init__(self):
        self.stInit = creon_0_Init.Connection(logging=True)

        self.stUtils = utils.Utils()
        self.stStockByIndustry = creon_98_stocks_by_industry.StocksByIndustry()

        self.stStockInfo = creon.StockInfo()

        self.stTrading = creon.Trading()

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
    def algorithm_3__stock_purchase_recommandation(self, marketType=0, top=5, bPrint=False, comparison_period=2000):
        stTrading = creon.Trading()

        if stTrading.trade_init() == True:
            추천_종목_리스트 = []
            추천_종목_이름_리스트 = []
            투자_후보_예상수익 = []

            if marketType == 0:
                __markeyType = creon_98_stocks_by_industry.StocksByIndustry.MARKET['코스피']
            elif marketType == 1:
                __markeyType = creon_98_stocks_by_industry.StocksByIndustry.MARKET['코스닥']

            # stock_code_list = self.stStockByIndustry.getStockListByMarket(creon_98_stocks_by_industry.StocksByIndustry.MARKET['코스피'])
            # stock_code_list = self.stStockByIndustry.getStockListByMarket(__markeyType)
            # stock_name_list = self.stUtils.get_nameList_from_codeList(stock_code_list)
            
            stock_name_list = self.후보군_종목_리스트
            stock_code_list = self.stUtils.get_codeList_from_nameList(stock_name_list)

            if bPrint == True:
                print(stock_code_list)
                print(stock_name_list)

            날짜 = utils.Utils.InputValue_StockChart_Field_type['날짜']
            고가 = utils.Utils.InputValue_StockChart_Field_type['고가']
            종가 = utils.Utils.InputValue_StockChart_Field_type['종가']

            # comparison_period=500
            # comparison_period=100
            # __기대_조건성립률=93
            __기대_조건성립률=80
            # __기대_주가_대비_수익률=1.5
            기대수익률=5
            if bPrint == True:
                print('__기대_조건성립률:', __기대_조건성립률, '기대수익률:', 기대수익률)
            result_list = []
            for j in range(len(stock_code_list)):
                item = {}
                item['종목명'] = stock_name_list[j]
                item['종목코드'] = stock_code_list[j]
                item['정보'] = self.stUtils.get_stock_value_n_days(stock_code_list[j], comparison_period)
                result_list.append(item)
                
            # for j in range(len(result_list)):
            #     print(result_list[j])

            ###################################################################################
            # 계산식 잘못 된 부분 있을거 같은데, 찾자!
            ############ 금일 고가로 계산하는게 아니라, % 로 계산해야 한다..! (수정함)
            ############ "(n-2) 종가 ==> (n-1) 고가" 를 활용해 n 종가에 구매해서 n + 1 에 팔도록 해야 한다...
            ###################################################################################

            ###########################################
            ## 비교기간만 바꿔봤을 때, 수익
            # CREON API response time 때문에, 우선 "삼륭물삼 ~ 에이치엘비생명과학" 만 비교
            # __비교기간 = 1 # 3754
            __비교기간 = 2 # 5093 # BEST
            # __비교기간 = 3 # 4410
            # __비교기간 = 5 # 4333
            # __비교기간 = 10 # 4232
            # __비교기간 = 50 # 1814
            # __비교기간 = 100 # -102

            ## 뭔가 구멍이 있는듯?
            ###########################################

#######################################################
# Simulator
#######################################################
            __전체기간 = 10 # 2주
            __전체수익 = 0
            __종목별_매매_수량 = 1 # top 5 각 1 주씩 매수
            bFirst = 0
            for __오늘부터며칠전 in range(2, __전체기간+1):
                __추천_종목_리스트, __수익_리스트 = self.기간_별_추천_종목(result_list, __오늘부터며칠전, __비교기간, 최고수익=False, 수익률=기대수익률, top=top, bPrint=False)
                
                __매수비용 = 0
                __하루수익 = 0
                __추천_종목_이름_리스트 = []
                for i in range(len(__수익_리스트)):
                    ################################################
                    # [중요] 세금 적용이 되지 않았습니다!!!!!!!!!!!!!
                    ################################################

                    __매수비용 += __추천_종목_리스트[i]['정보'][__오늘부터며칠전 + 1][종가] * __종목별_매매_수량
                    __하루수익 += __수익_리스트[i] * __종목별_매매_수량
                    __추천_종목_이름_리스트.append(__추천_종목_리스트[i]['종목명'])
                if bPrint == True:
                    print('[%s일전]** 수익: %6s (매수비용: %s), 수익_리스트: %s [%s] ' % (__오늘부터며칠전, __하루수익, __매수비용, __수익_리스트, __추천_종목_이름_리스트))
                __전체수익 += __하루수익
                # for i in range(len(__추천_종목_리스트)):
                #     print('(%2s/%2s) %s' % (__추천_종목_리스트[i]['성공횟수'], __비교기간, __추천_종목_리스트[i]['종목명']))

                # 오늘 기준으로 매수할 종목 추천
                if bFirst == 0:
                    추천_종목_리스트 = __추천_종목_리스트
                    추천_종목_이름_리스트 = __추천_종목_이름_리스트
                    투자_후보_예상수익 = __수익_리스트
                    bFirst = 1

            if bPrint == True:
                print('>> 전체수익: %s' % (round(__전체수익, 2)))
            return 추천_종목_리스트, 추천_종목_이름_리스트, 투자_후보_예상수익

# nm
# n + 2(m - 1) = n + m
# m : 전체기간 ( 100 )
# n : 비교기간 ( 10 )
# n + 2(m - 1) = n + m
# n + 2(m - 1) = n + 2m - 2 = n + m
# 
# nm
# 
#   
# nm => n + m = >
#           
    def 기간_별_추천_종목(self, stock_info_list, 오늘로부터며칠전, 비교기간, 최고수익=False, 수익률=2, top=5, bPrint=False):
        if bPrint == True:
            print('##############################################################')
        __추천_종목_리스트 = []

        날짜 = utils.Utils.InputValue_StockChart_Field_type['날짜']
        고가 = utils.Utils.InputValue_StockChart_Field_type['고가']
        종가 = utils.Utils.InputValue_StockChart_Field_type['종가']

        if bPrint == True:
            print('> [오늘: %s]' % (self.stUtils.현재_시간()))
            print('> 오늘로부터며칠전: %s, 비교기간: %s' % (오늘로부터며칠전, 비교기간))
        for i in range(len(stock_info_list)):
            item = stock_info_list[i] # 종목 정보
            유효기간 = len(item['정보'])
            if bPrint == True:
                print('유효기간: %s' % (유효기간))
            
            __목표_수익_달성_횟수 = 0
            __성공여부 = '>'
            for j in range(오늘로부터며칠전, 오늘로부터며칠전+비교기간):
                if 유효기간 > 오늘로부터며칠전+비교기간:
                    # (n-1)일 종가와, (n)일 고가 비교
                    if item['정보'][j][고가] > item['정보'][j+1][종가]:
                        __수익 = item['정보'][j][고가] - item['정보'][j+1][종가]
                        if __수익 > (item['정보'][j+1][종가] * (수익률 / 100)):
                            __목표_수익_달성_횟수 += 1
                            __성공여부 = '>'
                        else:
                            __성공여부 = '<'
                    else:
                        __성공여부 = '<'
                        # item['종목명']
                        # item['종목코드']
                        # item['정보']

                    if bPrint == True:
                        print('[%s 고가:%s] %s [%s 종가:%s] <종목명: %s>'
                            % (
                                item['정보'][j][날짜], item['정보'][j][고가],
                                __성공여부,
                                item['정보'][j+1][날짜], item['정보'][j+1][종가],
                                item['종목명']
                            )
                        )
            if bPrint == True:
                print('__목표_수익_달성_횟수: (%s/%s)' % (__목표_수익_달성_횟수, 비교기간))
            item['성공횟수'] = __목표_수익_달성_횟수
            __추천_종목_리스트.append(item)

        # sorting
        __추천_종목_리스트 = sorted(__추천_종목_리스트, key=lambda item:item['성공횟수'], reverse=True)

        
        # 수익 정보
        __수익_리스트 = []
        for i in range(0, top):
            __매도날_고가 = __추천_종목_리스트[i]['정보'][오늘로부터며칠전][고가]
            __매도날_종가 = __추천_종목_리스트[i]['정보'][오늘로부터며칠전][종가]
            __매수날_종가 = __추천_종목_리스트[i]['정보'][오늘로부터며칠전+1][종가]
            __수익 = __매도날_고가 - __매수날_종가
            if __수익 >= (__매수날_종가 * (수익률 / 100)):
                if 최고수익 == False:
                    __수익 = __매수날_종가 * (수익률 / 100)
            else:
                # 매도날 종가에 팔고, 새로 계산된 top 5 를 구매....
                __수익 = __매도날_종가 - __매수날_종가

            __수익_리스트.append(__수익)

        if bPrint == True:
            print('##############################################################')
        return __추천_종목_리스트, __수익_리스트




# 시나리오
# TODO: 9 시 인지 확인
# TODO: 크레온 로그인
# 장 중인지 확인
# >> 장 열릴 때까지 대기
# 장 열림!
# >> 어제 매수한 종목 있으면, 수익률(ex. 2%) 에 맞춰 매도 걸어놓음
# >>> 매도 시, 가격 최소 단위? 맞춰서 매도 걸어야 함.;;
# 목표 수익률에 매도 등록
# 매도 완료 시 장 마감 2분 전까지 sleep
# 장 마감 1분 전, 현재 주가로 1 주 매수
# >> 장 마감 1분 전인지 확인 (1분 이상 남았다면 대기)
# >> 매수 종목 정보 검색
# >> 매수 수행
# >>> (optional) 실시간 주가 subscribe
# >>> 매수 성공 확인
# >>> 모든 subscribe 해제
# (처음으로 돌아가서 반복) <-- x
# TODO: 크레온 프로그램 종료
    def algorithm_4(self):

        __bDBG = True

        __bExit = False
        __bIsStockMarketOpen = False

        while True:
# 장 중인지 확인
            __bIsStockMarketOpen = self.stUtils.장_중인지_확인()
            bConnect = self.stInit.do_connect() # NOTE: always return True. 
            if __bDBG == True:
                __bIsStockMarketOpen = True
                bConnect = True
                print('__bIsStockMarketOpen: %s, bConnect: %s' % (__bIsStockMarketOpen, bConnect))

# >> 장 열릴 때까지 대기
            if (bConnect == False) | (__bIsStockMarketOpen == False):
                print('# >> 장 열릴 때까지 대기')
                while True:
                    sleep(1)
                    print('현재 시간 : %s' % (self.stUtils.현재_시간()))
                    if self.stUtils.장_중인지_확인() == True:
                        print('주식 장 시작!!!!!!!!!!!!!!!!!!!')
                        break
            else:
# 장 열림!
                print('# [2] 장 열림!')
                bTradeInit = self.stTrading.trade_init()
                if bTradeInit == False:
                    exit()
# >> 어제 매수한 종목 있으면, 수익률(ex. 2%) 에 맞춰 매도 걸어놓음
# >>> 매도 시, 가격 최소 단위? 맞춰서 매도 걸어야 함.;;

                # 잔고 확인 (보유 주식)
                주식_잔고_리스트 = self.stTrading.주식_잔고_조회(bPrint=False)


                # 매수_목록_0218
                # 매수_목록_0220 로 갈아끼우자,
                # 매도 <-- 어제 매수한 종목에 대한 매도 주문
                selling_subscribe_stockconclusion_list = []
                for i in range(len(주식_잔고_리스트)):
                    for j in range(len(self.매수_목록_0220)):
                        if 주식_잔고_리스트[i]['종목명'] == self.매수_목록_0220[j] :
                            # subscribe
                            __stCpStockConclusion = creon_1_SB_PB.CpPBConclusion()
                            __code = self.stUtils.get_code_from_name(주식_잔고_리스트[i]['종목명'])
                            __stCpStockConclusion.subscribe(__code, __stCpStockConclusion)
                            selling_subscribe_stockconclusion_list.append(__stCpStockConclusion)

                            # 매도 수행
                            self.stTrading.주식_주문( # *** 매수/매도 주문은 정상 동작함
                                매매 = 1, # 1: 매도, 2: 매수
                                stockName=self.매수_목록_0220[j],
                                # 주문단가=(주식_잔고_리스트[i]['손익단가'] * 1.02), # 손익단가 * 1.02 == 2 % 높게 매도
                                주문단가=self.매도_가격_0220[j], # 손익단가 * 1.02 == 2 % 높게 매도
                                # 주문 단가 자리 수 맞춰야 함.
                                주문수량=1,
                                bPrint=False,
                                bTest=False
                            )


# 장 마감? 1분 전, 현재 주가로 1 주 씩 매수
                __top = 5 # 5 개 회사 추천
                __추천_종목_리스트, __투자_후보_이름, __투자_후보_예상수익 = self.algorithm_3__stock_purchase_recommandation(marketType=1, top=__top) # marketType(0: 코스피, 1: 코스닥)
                print('** 추천 종목:', __투자_후보_이름, __투자_후보_예상수익)

# >> 장 마감 1분 전인지 확인 (1분 이상 남았다면 대기)
                # sleep(1)
                __투자_후보_현재_정보_리스트 = []
                __bBuyStock = False
                # if __bDBG == True:
                #     __bBuyStock = True
                __매수_타이밍 = 60
                while __bBuyStock == False:
                    __마감까지_남은시간 = self.stUtils.마감_까지_남은_시간().total_seconds()
                    # if __bDBG == True:
                    #     __bBuyStock = True # for DBG
                    # else:
                    __bBuyStock = (__마감까지_남은시간 <= __매수_타이밍)

                    print('장 마감까지 %s 초 남음 (%s) (매수 타이밍: %s 초 전)' % (__마감까지_남은시간, __bBuyStock, __매수_타이밍))
                    sleep(1)
                    
# >> 매수 종목 정보 검색
                for i in range(len(__투자_후보_이름)):
                    print(__투자_후보_이름[i])
                    __투자_후보_현재_정보_리스트.append(self.stStockInfo.getInfoDetail(__투자_후보_이름[i], bPrint=True)) # 출력되는 정보 순서 참고. 추후 dictionary 로 변경하면 좋을 듯,
                
# >> 매수 수행
                if bTradeInit == True:
# >>> (optional) 실시간 주가 subscribe
                    subscribe_stockcur_list = []
                    for i in range(len(__투자_후보_이름)):
                        __stCpStockCur = creon_1_SB_PB.CpPBStockCur() # 실시간 주가 변동 확인 위해서 사용 *************** 현재 가격 받아오는건 정상동작 안함..
                        __code = self.stUtils.get_code_from_name(__투자_후보_이름[i])
                        __stCpStockCur.subscribe(__code, __stCpStockCur) # 실시간 거래 가능시간 이외에는, 현재가 고정이기 때문에 subscribe 해도 받는(receive)게 없다.
                        subscribe_stockcur_list.append(__stCpStockCur)

                    subscribe_stockconclusion_list = []
                    
                    for i in range(len(__투자_후보_이름)):
                        __stCpStockConclusion = creon_1_SB_PB.CpPBConclusion()
                        __code = self.stUtils.get_code_from_name(__투자_후보_이름[i])
                        __stCpStockConclusion.subscribe(__code, __stCpStockConclusion)
                        subscribe_stockconclusion_list.append(__stCpStockConclusion)
                        self.stTrading.주식_주문( # *** 매수 주문은 정상 동작함
                            매매 = 2, # 매수
                            stockName=__투자_후보_이름[i],
                            주문단가=__투자_후보_현재_정보_리스트[i][0], # 현재가
                            주문수량=1,
                            bPrint=False,
                            bTest=False
                        )
                
                    __selling_conclusion_count = 0
                    __selling_conclusion_max = len(selling_subscribe_stockconclusion_list)
                    __conclusion_count = 0
                    __conclusion_max = len(__투자_후보_이름)
# >>> 매수 성공 확인
                    while True:
                        sleep(1)
                        for i in range(__selling_conclusion_max):
                            if selling_subscribe_stockconclusion_list[i].getConclusion() == True:
                                __selling_conclusion_count += 1
                        for i in range(__conclusion_max):
                            if subscribe_stockconclusion_list[i].getConclusion() == True:
                                __conclusion_count += 1
                        
                        print('[%s] 매도 성공 대기: (%s/%s)' % (self.stUtils.현재_시간(), __selling_conclusion_count, __selling_conclusion_max))
                        print('[%s] 매수 성공 대기: (%s/%s)' % (self.stUtils.현재_시간(), __conclusion_count, __conclusion_max))
                        
                        if (__selling_conclusion_count == __selling_conclusion_max) & (__conclusion_count == __conclusion_max):
                            break
                        else:
                            __selling_conclusion_count = 0
                            __conclusion_count = 0

                        # 매도 실패에 대한 예외처리 필요.
                        if self.stUtils.마감_까지_남은_시간().total_seconds() <= 60:
                            # 현재가로 매도 필요한 종목 목록..!
                            for i in range(__selling_conclusion_max):
                                if selling_subscribe_stockconclusion_list[i].getConclusion() == False: # 매도 안된 경우
                                    __종목명 = self.매수_목록_0218[i]
                                    print(__종목명)
                                    __stockInfo = self.stStockInfo.getInfoDetail(__종목명, bPrint=True)
                                    __현재가 = __stockInfo[0]
                                    # [TODO] 매도 주문 취소

                        exit()

# >>> 모든 subscribe 해제
                    # 매도 종목 unsubscribe
                    for i in range(len(len(self.매수_목록_0218))):
                        selling_subscribe_stockconclusion_list[i].unsubscribe()
                    # 매수 종목 unsubscribe
                    for i in range(len(__투자_후보_이름)):
                        subscribe_stockcur_list[i].unsubscribe()
                        subscribe_stockconclusion_list[i].unsubscribe()

                if __bDBG == True:
                    __bExit = True


            if __bExit == True:
                break
                

# [TEST] 장 열리기 전에 매수 걸어 놓으면 어떻게 되는지 확인