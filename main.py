# main.py module

import sys # http://pythonstudy.xyz/python/article/17-%EB%AA%A8%EB%93%88-Module
import argparse
# import json

from bs4 import BeautifulSoup

# import requests # import all & use function with requests.
# from requests import * # import all function & use function w/o requests.
from requests import get_html as getHTML # alias

import crawler

from file_inout import write_to_file, read_from_file

def usage() : # how to use
    # """ means `string`
    return """
        python3 main.py -u "user name"
        python3 main.py --username "user name"
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

    args = parser.parse_args()
    print("args : %s" % args)
    # sys.exit()

    if args.username is not None :
        arg_required("username")
        arg_required("password")

        instagramCrawler = crawler.InstagramCrawler() # create instance
        print("URL : " + instagramCrawler.URL)

        # instagramCrawler.get_user_posts(args.username)

        # instagramCrawler.login()
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
        # stellajang_official = instagramCrawler.get_user_posts(stellajang_official)
        # print("get_user_posts : %s" % stellajang_official)

        instagramCrawler.login();

        # # etc
        # URL = "https://www.instagram.com/" + args.username
        # html = getHTML(url = URL) # Named Parameter
        # soup = BeautifulSoup(html, 'html.parser')
        # print(soup)

        # #param = "react-root"
        # field = "div"
        # param = "area_newsstand"
        # #table = soup.find('section', {'class': class_name})
        # table = soup.find(field, {'class': param})
        # print(table)
    else :
        parser.print_help()
        usage()
