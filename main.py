# main.py module

import sys # http://pythonstudy.xyz/python/article/17-%EB%AA%A8%EB%93%88-Module
import argparse
# import json

from bs4 import BeautifulSoup

# import requests # import all & use function with requests.
# from requests import * # import all function & use function w/o requests.
from requests import get_html as getHTML # alias

import crawler

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

    args = parser.parse_args()

    if args.username is not None :
        arg_required("username")

        instagramCrawler = crawler.InstagramCrawler() # create instance
        print("URL : " + instagramCrawler.URL)

        instagramCrawler.get_user_posts(args.username)

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
