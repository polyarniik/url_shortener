import hashlib
import random


def shorter(link):
    link_hash = hashlib.md5(str(link[0]).encode('UTF-8'))
    short_link = ''
    for i in range(0, random.randrange(4, 7)):
        short_link += link_hash.hexdigest()[random.randrange(len(link_hash.hexdigest()))]
    print(short_link)
    return short_link
