import binascii
import hashlib
import os
import random


def shorter(link):
    """
    Укорачивание ссылки
    :param link:
    :return:
    """
    salt = binascii.hexlify(os.urandom(5)).decode()
    link += salt
    link_hash = hashlib.md5(link.encode("UTF-8")).hexdigest()
    short_link = ""
    for i in range(8):
        short_link += link_hash[random.randint(0, len(link_hash) - 1)]
    return short_link
