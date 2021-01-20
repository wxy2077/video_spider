#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/13 17:10
# @Author  : CoderCharm
# @File    : test4.py
# @Software: PyCharm
# @Github  : github/CoderCharm
# @Email   : wg_python@163.com
# @Desc    :
"""

pip install m3u8

"""


import time
import m3u8
import requests
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor


class DownLoadM3U8(object):

    def __init__(self, m3u8_url, file_name='./new.mp4'):
        self.m3u8_url = m3u8_url
        self.file_name = file_name

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        }
        self.thread_pool = ThreadPoolExecutor(max_workers=5)

    def get_ts_url(self):
        m3u8_obj = m3u8.load(self.m3u8_url)
        base_uri = m3u8_obj.base_uri

        for seg in m3u8_obj.segments:
            yield urljoin(base_uri, seg.uri)

    def download_single_ts(self, url_info):
        url, ts_name = url_info
        res = requests.get(url, headers=self.headers, verify=False)
        with open(ts_name, 'wb') as fp:
            fp.write(res.content)

    def download_all_ts(self):
        ts_urls = self.get_ts_url()

        with open(self.file_name, "wb") as merged:
            for index, ts_url in enumerate(ts_urls):
                print(ts_url)
                res = requests.get(ts_url, headers=self.headers, verify=False, stream=True)
                merged.write(res.content)

    def run(self):
        self.download_all_ts()


if __name__ == '__main__':
    new_m3u8_url = "http://cctvalih5ca.v.myalicdn.com/live/cctv1_2/index.m3u8"

    start = time.time()
    d = DownLoadM3U8(new_m3u8_url)
    d.run()

    end = time.time()
    print('耗时:', end - start)
