#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/13 15:19
# @Author  : wgPython
# @File    : test1.py
# @Software: PyCharm
# @Desc    :
"""

pip install m3u8

pip install natsort

"""

import os
import time
import m3u8
import requests
from glob import iglob
from natsort import natsorted
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
        for index, ts_url in enumerate(ts_urls):
            print(ts_url)
            self.thread_pool.submit(self.download_single_ts, [ts_url, f'{index}.ts'])
        self.thread_pool.shutdown()

    def run(self):
        self.download_all_ts()
        ts_path = '*.ts'
        with open(self.file_name, 'wb') as fn:
            for ts in natsorted(iglob(ts_path)):
                with open(ts, 'rb') as ft:
                    scline = ft.read()
                    fn.write(scline)
        for ts in iglob(ts_path):
            os.remove(ts)


if __name__ == '__main__':
    new_m3u8_url = "xxx"

    new_file_name = './t111113.mp4'

    start = time.time()
    d = DownLoadM3U8(new_m3u8_url, file_name=new_file_name)
    d.run()

    end = time.time()
    print('耗时:', end - start)

