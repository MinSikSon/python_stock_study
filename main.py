# main.py module

import sys # http://pythonstudy.xyz/python/article/17-%EB%AA%A8%EB%93%88-Module
import argparse
# import json

# from bs4 import BeautifulSoup

# import requests # import all & use function with requests.
# from requests import * # import all function & use function w/o requests.
from requests import get_html as getHTML # alias

import webcrawler.crawler as crawler

from file_inout import write_to_file, read_from_file

from time import sleep

import os
import datetime

def usage() : # how to use
    # """ means `string`
    return """
        [for Mac OS X]
        python3 main.py -u "user name"
        python3 main.py --username "user name"
        python3 main.py --website="tesla"
    """

def arg_required(args, fields = []) :
    for field in fields :
        if not getattr(args, field): # what is this?
            parser.print_help()
            sys.exit() # exit program

if __name__ == '__main__' : # run this script in the interpreter. http://pythonstudy.xyz/python/article/17-%EB%AA%A8%EB%93%88-Module
    # arg parser
    parser = argparse.ArgumentParser(description="Instagram Crawler - SMS version", usage=usage())
    parser.add_argument("-u", "--username", help="insta id")
    parser.add_argument("-pw", "--password", help="insta pw")
    parser.add_argument("-c", "--count", type=int, help="post count")
    parser.add_argument("-w", "--website", help="website name")

    args = parser.parse_args()
    print("args : %s" % args)

    print("website : %s" % args.website)
    if args.website == 'tesla' :
        print("[tesla]")
        websiteCrawler = crawler.WebsiteCrawler(False)
        # 1. move to tesla page
        websiteCrawler.move_to_url("https://www.tesla.com/ko_KR/blog")
        # 2. copy 새소식
        __뉴스제목_xpath = "/html/body/div[2]/div/div/main/div/div[1]/div/div[1]/section[1]/div/div/div/div/div[1]/div[1]/div/div/h2/a"
        __news_name = websiteCrawler.get_data_by_xpath(__뉴스제목_xpath)
        __뉴스작성자_xpath = "/html/body/div[2]/div/div/main/div/div[1]/div/div[1]/section[1]/div/div/div/div/div[1]/div[1]/div/div/div[1]"
        __news_author = websiteCrawler.get_data_by_xpath(__뉴스작성자_xpath)
        __뉴스내용_xpath = "/html/body/div[2]/div/div/main/div/div[1]/div/div[1]/section[1]/div/div/div/div/div[1]/div[1]/div/div/div[2]/div/div/div/p"
        __news = websiteCrawler.get_data_by_xpath(__뉴스내용_xpath)
        print("__news_name : %s" % __news_name)
        print("__news_author : %s" % __news_author)
        print("__news : %s" % __news)

        # 3. move to google translate
        __google_translate_url = "https://translate.google.co.kr/?hl=ko#view=home&op=translate&sl=en&tl=ko"
        websiteCrawler.move_to_url(__google_translate_url)

        # 4. paste 새소식 to Google Translate textarea
        websiteCrawler.input_and_click_btn(__news_name, input_path='textarea[id="source"]')
        sleep(1)
        __google_translate_input_xpath = "/html/body/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/div[1]/div[2]/div"
        __news_name_kor = websiteCrawler.get_data_by_xpath(__google_translate_input_xpath)
        
        websiteCrawler.input_and_click_btn(__news, input_path='textarea[id="source"]')
        sleep(3) # 영문 news 내용을 textarea 에 붙여주는 동안 기다림
        __google_translate_input_xpath = "/html/body/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/div[1]/div[2]/div"
        __news_kor = websiteCrawler.get_data_by_xpath(__google_translate_input_xpath)
        
        print("__news_name_kor : %s" % __news_name_kor)
        print("__news_author : %s" % __news_author)
        print("__news_kor : %s" % __news_kor)

        # 5. 저장!
        forder = "./%s" % args.website
        if os.path.isdir(forder) is False :
            os.mkdir(forder)

        path = "%s/%s.txt" % (forder, __news_name_kor)
        if os.path.exists(path) is False :
            # create file
            write_to_file(path=path, data=__news_kor, option='w')

            # 6. copy
            print("copy!!")
            path = "%s/README.md" % (forder)
            write_to_file(path=path, data="%s / " % __news_name_kor, option='a')
            write_to_file(path=path, data="%s / " % __news_author, option='a')
            write_to_file(path=path, data="%s / " % __news_kor, option='a')
            write_to_file(path=path, data="\n", option='a')

    elif args.website == "bbc" :
        __BBC_URL = "https://www.bbc.com/"
        __GOOGLE_TRANSLATE_URL = "https://translate.google.co.kr/?hl=ko#view=home&op=translate&sl=en&tl=ko"

        __news_item_count = 6
        __xpath_news_title = []
        __xpath_news_type = []
        for item in range(0, __news_item_count) :
            __xpath_news_title.append("/html/body/div[7]/div/section[3]/div/ul/li[%s]/div/div[2]/h3/a" % (item))
            __xpath_news_type.append("/html/body/div[7]/div/section[3]/div/ul/li[%s]/div/div[2]/a"     % (item))
        # for item in range(1, __news_item_count) :
        #     print("%s" % __xpath_news_title[item])
        #     print("%s" % __xpath_news_type[item])
        
        # 1. move to BBC website
        websiteCrawler = crawler.WebsiteCrawler(True)
        websiteCrawler.move_to_url(__BBC_URL)

        # 2. data crawling
        __news_title = [""]
        __news_type = [""]
        for item in range(1, __news_item_count) :
            eng_news_title = websiteCrawler.get_data_by_xpath(__xpath_news_title[item])
            __news_title.append(eng_news_title)
            eng_news_type = websiteCrawler.get_data_by_xpath(__xpath_news_type[item])
            __news_type.append(eng_news_type)

        for item in range(1, __news_item_count) :
            print("%s" % __news_title[item])
            print("%s" % __news_type[item])

        # 3. move to google translate

        # 4. paste 새소식 to Google Translate textarea
        __xpath_google_translate_input = "/html/body/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/div[1]/div[2]/div"
        __news_title_kor = [""]
        __news_type_kor = [""]
        for item in range(1, __news_item_count) :
            websiteCrawler.move_to_url(__GOOGLE_TRANSLATE_URL)
            websiteCrawler.input_and_click_btn(__news_title[item], input_path='textarea[id="source"]')
            sleep(1)
            __news_title_kor.append(websiteCrawler.get_data_by_xpath(__xpath_google_translate_input))
            
            websiteCrawler.move_to_url(__GOOGLE_TRANSLATE_URL)
            websiteCrawler.input_and_click_btn(__news_type[item], input_path='textarea[id="source"]')
            sleep(1) # 영문 news 내용을 textarea 에 붙여주는 동안 기다림
            __news_type_kor.append(websiteCrawler.get_data_by_xpath(__xpath_google_translate_input))

        for item in range(1, __news_item_count) :
            print("%s" % __news_title_kor[item])
            print("%s" % __news_type_kor[item])

        # 5. 저장!
        forder = "./%s" % args.website
        if os.path.isdir(forder) is False :
            os.mkdir(forder)

        dt = datetime.datetime.now()
        txt_file_name = "%s_%s_%s" % (dt.year, dt.month, dt.day)
        path = "%s/%s.txt" % (forder, txt_file_name)
        if os.path.exists(path) is False :
            write_to_file(path=path, data="empty", option='w')
            # 6. copy
            print("copy!!")
            path = "%s/README.md" % (forder)
            if os.path.exists(path) is False :
                write_to_file(path=path, data="", option='w')
            
            write_to_file(path=path, data=txt_file_name, option='a')
            for item in range(1, __news_item_count) :
                write_to_file(path=path, data="[type] %s / [title] %s \n" % (__news_type_kor[item], __news_title_kor[item]), option='a')

    elif args.website == "insta" :
        if args.username is not None :
            arg_required("username")
            arg_required("password")

            instagramCrawler = crawler.InstagramCrawler() # create instance
            print("URL : " + instagramCrawler.URL)

            instagramCrawler.login(args.username, args.password)
            instagramCrawler.login_close_noti()

            ## test. Get User Profile
            # kim_chan_yong = "kim_chan_yong"
            # kim_chan_yong = instagramCrawler.get_user_profile(kim_chan_yong)
            # print("get_user_profile : %s" % kim_chan_yong)

            # stellajang_official = "stellajang_official"
            # interstellajang = "interstellajang"
            huni543hun = "huni543hun"
            outputComment, outputList = instagramCrawler.get_user_posts(username=huni543hun, number=args.count, retComment=True, retLikeList=True)
            
            for o in outputComment :
                write_to_file(path="./output_comment.txt", data=o, option='a')

            for o in outputList :
                write_to_file(path="./output.txt", data=o, option='a')
            
            inputList = read_from_file(path="./output.txt")
            for i in inputList :
                print("%s" % i)

    else :
        parser.print_help()
        usage()
