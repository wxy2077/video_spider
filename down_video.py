# -*- coding:utf-8 -*-
# @Author: wgPython
# @Time: 2018/7/27 15:59
# @Desc:
"""
今日头条APP 西瓜视频 批量抓取爬虫，
首先声明： 仅供学习参考， 用于其他用途出现什么用途与本人无关
技术点: 1， 逆向js解析出视频url
        2， 下载视频的时候使用 with requests.get(video_url, stream=True) as r: 保证视频完整性
"""
import base64
import json
import re
import random

import binascii
import uuid
# from urllib.parse import urlparse

import requests
import time


UA_WEB_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",

]


def parse_interface():
    """
    解析视频接口  获取详细视频页url

    :return:
    """
    # 此接口是通过fiddler抓包工具抓的
    res = requests.get("http://is.snssdk.com/api/news/feed/v82/?category=video", headers={
                                        "User-Agent": random.choice(UA_WEB_LIST),
                                        "Accept": "*/*",
                                        "Accept-Language": "zh-CN,zh;q=0.9",
                                    })
    if res.status_code == 200:
        # 解析第一层的json数据
        json_data = json.loads(res.text)
        article_id_list = list()
        for detail_data in json_data.get("data"):
            # 详细的数据本身是字符串的
            new_content = json.loads(detail_data["content"])
            # 提取出详细页文章id 好拼接详细页url
            article_id = new_content.get("item_id")
            article_id_list.append(article_id)

        return article_id_list


def parse_detail():
    """
    解析视频详细页面数据
    :return:
    """
    article_id_list = parse_interface()
    while True:
        # 接口一直请求  可以无限刷新
        for article_id in article_id_list:
            res = requests.get("https://www.toutiao.com/a{}".format(article_id), headers={
                            "User-Agent": random.choice(UA_WEB_LIST),
                            "Accept": "*/*",
                            "Accept-Language": "zh-CN,zh;q=0.9"
                        })

            # 获取视频id
            video_id = re.findall(r"videoId:\s?\'(\w{29,35})\'", res.text)
            video_id = video_id[0] if video_id else None
            if video_id:
                video_url = get_toutiao_video_url(video_id)
                with requests.get(video_url, stream=True) as r:
                    # uuid4 生成不重复的视频名字， 也可以从json数据里面 提取出视频的源名称
                    video_name = "./"+str(uuid.uuid4())+".mp4"
                    with open(video_name, "wb") as f:
                        # 保存视频字节流
                        f.write(r.content)
                print(video_name, "保存成功")

        # 睡眠  不要太频繁
        time.sleep(random.uniform(5, 8))


# 以下三个函数是用过分析JS， 逆向还原 源视频 .mp4url的生成过程
def right_shift(val, n):
    return val >> n if val >= 0 else (val + 0x100000000) >> n


def parse_video_json(url):
    html = requests.get(url, timeout=360)
    json_data = html.content.decode()
    dict_str = json.loads(json_data)
    data_str = dict_str['data']
    dict_video_list = data_str['video_list']
    dict_video1 = dict_video_list['video_1']
    main_url = dict_video1['main_url']
    return main_url


def get_toutiao_video_url(video_id):
    """
    传入头条视频的id 解析出头条的视频url
    :param video_id:
    :return: video_url
    """
    r = str(random.random())[2:]
    url = 'http://i.snssdk.com/video/urls/v/1/toutiao/mp4/{}'.format(video_id)
    n = requests.get(url).request.path_url + '?r=' + r   # 获取url路径
    c = binascii.crc32(n.encode())
    s = right_shift(c, 0)
    main_video_url = parse_video_json(url + '?r={}&s={}'.format(r, s))
    video_url = base64.b64decode(main_video_url)
    return video_url.decode()


if __name__ == '__main__':
    parse_detail()
