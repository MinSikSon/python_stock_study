import random

from time import sleep

def instagram_int(string) :
    return int(string.replace(",", ""))

def randmized_sleep(average=1):
    __min, __max = average * 1 / 2, average * 3 / 2
    sleep(random.uniform(__min, __max))