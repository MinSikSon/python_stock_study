import argparse
import webcrawler.crawler as crawler

if __name__ == '__main__' :
    print('__main__')

    print('----1. input : 자본금, 사려는 주식 이름')
    print('--------------------------------------------------')
    __stock_capital = 1000000 # 100 만원
    __stock_name = "tesla"
    __stock_count = 0
    print('1> 자본 : %s' % __stock_capital)
    print('2> 종목 : %s' % __stock_name)
    print('3> 수량 : %s' % __stock_count)
    
    print('----2. 구매 가능한지 비교 : ** web crawling 필요')
    print('--------------------------------------------------')
    __crawler = crawler.WebsiteCrawler(True)
    __crawler.move_to_url(__crawler.GOOGLE_URL) # google 로 이동
    __crawler.input_and_click_btn(
        '%s 주식' % __stock_name, 
        __crawler.XPATH_GOOGLE_INPUT)
        # __crawler.XPATH_GOOGLE_SEARCH_BTN)
    
    # __crawler.sleep(2) # delay 를 주지 않을 경우, 검색되기 전에 __stock_value 를 찾으려고 하는 경우 존재함.

    __xpath_stock_value = "/html/body/div[7]/div[3]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/g-card-section/div/g-card-section/span[1]/span/span[1]"
    __stock_value = __crawler.get_data_by_xpath(__xpath_stock_value)

    __xpath_stock_currency = "/html/body/div[7]/div[3]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/g-card-section/div/g-card-section/span[1]/span/span[2]"
    __stock_currency = __crawler.get_data_by_xpath(__xpath_stock_currency)
    
    if __stock_value is not None :
        print('__stock_value : %s (%s)' % (__stock_value, __stock_currency))

        print('[구매 전략] 여유 자금이 있으면 구매')
        if __stock_currency == "KRW" :
            __stock_value = int(__stock_value.replace(",", "")) # 콤마 제거 후 숫자로 변환
        else :
            __USD_exchange_rate = 1000
            __stock_value = float(__stock_value) * __USD_exchange_rate
            __stock_value = int(round(__stock_value))

        if __stock_capital >= __stock_value :
            print('구매 성공')
            __stock_capital = __stock_capital - __stock_value
            __stock_count = __stock_count + 1
        else :
            print('구매 실패')

        print('-----3. output : 잔여금, 주식 상황')
        print('--------------------------------------------------')
        print('[result]')
        print('1> 자본 : %s' % __stock_capital)
        print('2> 종목 : %s' % __stock_name)
        print('3> 수량 : %s' % __stock_count)
    else :
        print('** 비상장 종목 입니다 **')
        print('--------------------------------------------------')

    print('- END -')