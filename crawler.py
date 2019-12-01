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
        print("init nothing")
        self.browser = Browser(has_screen)

    def _dismiss_login_prompt(self) : 
        ele_login = self.browser.find_one(".Ls00D .Szr5J")
        if ele_login :
            ele_login.click()

    def login(self) :
        print("crawler - login()")
        browser = self.browser
        # browser = Browser(True)
        __url = "%s/accounts/login/" % (InstagramCrawler.URL)
        browser.get(__url)
        __u_input = browser.find_one('input[name="username"]')
        __u_input.send_keys(secret.username)
        __p_input = browser.find_one('input[name="password"]')
        __p_input.send_keys(secret.password)

        __login_btn = browser.find_one(".L3NKy")
        __login_btn.click()

    # ??
    def get_user_profile(self, username) :
        print("crawler - get_user_profile()")
        browser = self.browser
        __url = "%s/%s" % (InstagramCrawler.URL, username)
        browser.get(__url)
        __name = browser.find_one(".rhpdm")
        __desc = browser.find_one(".-vDig span")
        __photo = browser.find_one("._fq-tv")
        __statistics = [ele.text for ele in browser.find(".g47SY")]
        __post_num, __follower_num, __following_num = __statistics

        return {
            "name" : __name.text,
            "desc" : __desc.text if __desc else None,
            "photo_url" : __photo.get_attribute("src"),
            "post_num" : __post_num,
            "follower_num" : __follower_num,
            "following_num" : __following_num
        }


    def get_user_posts(self, username, number=None, detail=False) :
        __user_profile = self.get_user_profile(username)
        if number is None :
            __number = utils.instagram_int(__user_profile["post_num"])

        self._dismiss_login_prompt()

        # if detail is not False :
        #     return self._get_posts_full(number)
        # else :
        #     return self._get_posts(number)


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
