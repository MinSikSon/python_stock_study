from browser import Browser
import secret

import utils
from exceptions import RetryException
from tqdm import tqdm

# fetch.py 는 단순히 가져옴
# from .fetch import fetch_caption
# from .fetch import fetch_comments
# from .fetch import fetch_datetime
# from .fetch import fetch_imgs
# from .fetch import fetch_likers
# from .fetch import fetch_likes_plays
# from .fetch import fetch_details
# end

# ??
import sys
import json
import traceback
from time import sleep

class Crawler :
    pass


class InstagramCrawler (Crawler) : # inherit Crawler class
# class variables. (all class instance share this variables.)
    URL = "https://www.instagram.com"

    def __init__(self, has_screen=False) : # Initializer
        print("[crawler.py] __init__()")
        self.browser = Browser(has_screen)

    def _dismiss_login_prompt(self) : 
        print("[crawler.py] _dissmiss_login_prompt()")
        # ele_login = self.browser.find_one(".sqdOP.L3NKy.y3zKF")
        ele_login = self.browser.find(".sqdOP.L3NKy.y3zKF")
        # print(ele_login)
        # ele_login = self.browser.find_one(".Ls00D .Szr5J")
        if ele_login[2] :
            ele_login[2].click()

    def login(self, username="username", password="password") :
        print("[crawler.py] login()")
        browser = self.browser
        # browser = Browser(True)
        __url = "%s/accounts/login/" % (InstagramCrawler.URL)
        browser.get(__url)
        __u_input = browser.find_one('input[name="username"]')
        # __u_input.send_keys(secret.username)
        __u_input.send_keys(username)

        __p_input = browser.find_one('input[name="password"]')
        # __p_input.send_keys(secret.password)
        __p_input.send_keys(password)

        __login_btn = browser.find_one(".L3NKy")
        __login_btn.click()

    def login_close_noti(self) :
        browser = self.browser

        # browser.implicitly_wait(1)

        __later_btn = browser.find_one(".aOOlW.HoLwm")
        __later_btn.click()

    def get_user_profile(self, username) :
        print("[crawler.py] get_user_profile()")
        browser = self.browser
        __url = "%s/%s" % (InstagramCrawler.URL, username)
        browser.get(__url)
        __name = browser.find_one(".rhpdm")
        __desc = browser.find_one(".-vDig span")
        __photo = browser.find_one("._fq-tv")
        __statistics = [ele.text for ele in browser.find(".g47SY")] # list comprehension (http://pythonstudy.xyz/python/article/12-컬렉션--List)
        __post_num, __follower_num, __following_num = __statistics

        return {
            "name" : __name.text,
            "desc" : __desc.text if __desc else None,
            # "photo_url" : __photo.get_attribute("src"),
            "post_num" : __post_num,
            "follower_num" : __follower_num,
            "following_num" : __following_num
        }

    def get_user_posts(self, username, number=3, detail=False, retComment=False, retLikeList=False) :
        print("[crawler.py] get_user_posts()")

        browser = self.browser

        __user_profile = self.get_user_profile(username)
<<<<<<< Updated upstream
        print("get_user_posts : %s" % __user_profile)

        if number is None :
            __number = utils.instagram_int(__user_profile["post_num"])
=======
        print("get_user_profile : %s" % __user_profile)
>>>>>>> Stashed changes

        # # browser.page_down()

        if number is None :
            __number = utils.instagram_int(__user_profile["post_num"])
        else :
            __number = number + 1
        __post = browser.find_one("._9AhH0")
        # __post = browser.find_one_by_xpath("/html/body/span/section/main/div/div[4]/article[2]/div[1]/div/div[1]/div[1]/a/div/div[2]")
        # print("__post : %s" % __post)
        __post.click()


        __get_comments = []
        __get_elements = []
        for cnt in range(1, __number) :
            __btns = browser.find(".sqdOP.yWX7d._8A5w5")
            __like_btn = __btns[1]
            __like_btn.click()

            # browser.implicitly_wait(5)
            
            # comments
            __get_comment = browser.find_one_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/div[1]/ul/div/li/div/div/div[2]/span')
            print("__get_comment.text : %s" % __get_comment.text)
            __get_comments.append(__get_comment.text)

            # like
            like_idx = 1
            while(True) :
                xpath = "/html/body/div[5]/div/div[3]/div/div/div[%s]/div[2]/div[1]/div/a/div/div/div" % like_idx
                __get_element = browser.find_one_by_xpath(xpath)
                if(__get_element is None) : break
                __get_elements.append(__get_element.text)
                # print("__get_elements : %s" % __get_elements)
                # browser.page_down()
                like_idx = like_idx + 1

            print("__get_elements : %s" % __get_elements)

            # close
            __close_btn = browser.find_one_by_xpath('/html/body/div[5]/div/div[1]/div/div[2]/button')
            __close_btn.click()

            # next

            if cnt is not __number - 1 :
                __next_btn = browser.find_one_by_xpath('/html/body/div[4]/div[1]/div/div/a[2]')
                if __next_btn is None :
                    __next_btn = browser.find_one_by_xpath('/html/body/div[4]/div[1]/div/div/a')
                __next_btn.click()
        
        if retComment == True and retLikeList == True:
            return __get_comments, __get_elements
        if retLikeList == True:
            return __get_elements

        # __posts = [ele.text for ele in browser.find("._9AhH0")]

        # return __post
        # if detail is not False :
        #     return self._get_posts_full(number)
        # else :
        #     return self._get_posts(number)


    # def get_user_posts(self, username, number=None, detail=False) :
    #     __user_profile = self.get_user_profile(username)
    #     print("get_user_posts : %s" % __user_profile)

    #     if number is None :
    #         __number = utils.instagram_int(__user_profile["post_num"])

    #     self._dismiss_login_prompt()

    #     # if detail is not False :
    #     #     return self._get_posts_full(number)
    #     # else :
    #     #     return self._get_posts(number)


    # ???!!!
#     def _get_posts_full(self, num):
#         # @retry()
#         def check_next_post(cur_key):
#             ele_a_datetime = browser.find_one(".eo2As .c-Yi7")

#             # It takes time to load the post for some users with slow network
#             if ele_a_datetime is None:
#                 raise RetryException()

#             next_key = ele_a_datetime.get_attribute("href")
#             if cur_key == next_key:
#                 raise RetryException()

#         browser = self.browser
#         browser.implicitly_wait(1)
#         browser.scroll_down()
#         ele_post = browser.find_one(".v1Nh3 a")
#         ele_post.click()
#         dict_posts = {}

#         pbar = tqdm(total=num)
#         pbar.set_description("fetching")
#         cur_key = None

#         # Fetching all posts
#         for _ in range(num):
#             dict_post = {}

#             # Fetching post detail
#             try:
#                 check_next_post(cur_key)

#                 # Fetching datetime and url as key
#                 ele_a_datetime = browser.find_one(".eo2As .c-Yi7")
#                 cur_key = ele_a_datetime.get_attribute("href")
#                 dict_post["key"] = cur_key
#                 fetch_datetime(browser, dict_post)
#                 fetch_imgs(browser, dict_post)
#                 fetch_likes_plays(browser, dict_post)
#                 fetch_likers(browser, dict_post)
#                 fetch_caption(browser, dict_post)
#                 fetch_comments(browser, dict_post)

#             except RetryException:
#                 sys.stderr.write(
#                     "\x1b[1;31m"
#                     + "Failed to fetch the post: "
#                     + cur_key or 'URL not fetched'
#                     + "\x1b[0m"
#                     + "\n"
#                 )
#                 break

#             except Exception:
#                 sys.stderr.write(
#                     "\x1b[1;31m"
#                     + "Failed to fetch the post: "
#                     + cur_key if isinstance(cur_key,str) else 'URL not fetched'
#                     + "\x1b[0m"
#                     + "\n"
#                 )
#                 traceback.print_exc()

#             # self.log(json.dumps(dict_post, ensure_ascii=False))
#             dict_posts[browser.current_url] = dict_post

#             pbar.update(1)
#             left_arrow = browser.find_one(".HBoOv")
#             if left_arrow:
#                 left_arrow.click()

#         pbar.close()
#         posts = list(dict_posts.values())
#         if posts:
#             posts.sort(key=lambda post: post["datetime"], reverse=True)
#         return posts

#     def _get_posts(self, num):
#         """
#             To get posts, we have to click on the load more
#             button and make the browser call post api.
#         """
#         TIMEOUT = 600
#         browser = self.browser
#         key_set = set()
#         posts = []
#         pre_post_num = 0
#         wait_time = 1

#         pbar = tqdm(total=num)

#         def start_fetching(pre_post_num, wait_time):
#             ele_posts = browser.find(".v1Nh3 a")
#             for ele in ele_posts:
#                 key = ele.get_attribute("href")
#                 if key not in key_set:
#                     dict_post = { "key": key }
#                     ele_img = browser.find_one(".KL4Bh img", ele)
#                     dict_post["caption"] = ele_img.get_attribute("alt")
#                     dict_post["img_url"] = ele_img.get_attribute("src")

#                     fetch_details(browser, dict_post)

#                     key_set.add(key)
#                     posts.append(dict_post)

#                     if len(posts) == num:
#                         break

#             if pre_post_num == len(posts):
#                 pbar.set_description("Wait for %s sec" % (wait_time))
#                 sleep(wait_time)
#                 pbar.set_description("fetching")

#                 wait_time *= 2
#                 browser.scroll_up(300)
#             else:
#                 wait_time = 1

#             pre_post_num = len(posts)
#             browser.scroll_down()

#             return pre_post_num, wait_time

#         pbar.set_description("fetching")
#         while len(posts) < num and wait_time < TIMEOUT:
#             post_num, wait_time = start_fetching(pre_post_num, wait_time)
#             pbar.update(post_num - pre_post_num)
#             pre_post_num = post_num

#             loading = browser.find_one(".W1Bne")
#             if not loading and wait_time > TIMEOUT / 2:
#                 break

#         pbar.close()
#         print("Done. Fetched %s posts." % (min(len(posts), num)))
#         return posts[:num]


#     # not used =========================================
#     def get_posts(self, number=None) :
#         if number is not None :
#             print("get posts")
#         else :
#             print("fail `get posts`")

#     def __private_method(self) : # private method
#         pass

#     @staticmethod # static method inaccessible to class variables & instance variables
#     def static_method() :
#         pass

#     @classmethod # class method accessible to class variables
#     def class_method(cls) :
#         print(cls.URL)
#         pass

#     # Special Method (Magic Method)
#     def __add__(self, other) :
#         pass
# class Etc :
#     pass
