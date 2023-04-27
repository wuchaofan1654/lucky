# coding=utf-8
"""
# Create by wuchaofan 
# At 2023/4/13
# Current Dir custom/utils
"""


from django.core.cache import cache  # 引入缓存模块

cache.set('v', '555', 60 * 60)      # 写入key为v，值为555的缓存，有效期30分钟
cache.get('v')


class RedisUtil(object):
    def __init__(self):
        pass

    def set(self):
        pass

    def get(self):
        pass
