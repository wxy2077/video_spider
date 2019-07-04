# -*- coding:utf-8 -*-
# @Author: wgPython
# @Time: 2018/10/22 16:11
# @Desc: 
"""
根据腾讯视频vid 找出源视频

找到 iframe 中的vid
"""
import re
import requests
import json

# vid = "b1327kwk6cq"
# 通过vid 构造  获取源mp4 url
temp_url = "http://vv.video.qq.com/getinfo?vids={}&platform=101001&charge=0&otype=json&defn=shd"

# 目标url  获取里面的视频源地址
url = "https://mp.weixin.qq.com/s?__biz=MjM5MDc0NTY2OA==&mid=2651470124&idx=1&sn=77b8ab5b3d0c80636954f86579575941&chksm=bdbe8c078ac90511b325e1dc2209b0463395cb43411da94972945fd64d371d206c6da7cf4cbd"


def get_vid():
    """
    正则匹配出vid
    :return:
    """
    res = requests.get(url, headers={"Host": "mp.weixin.qq.com",
                                     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
                                     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                                     })

    re.search(r"data-src=[\"\']https://v.qq.com/iframe[^\"\']]", res.text)
    s = "https://v.qq.com/iframe/player.html?auto=0&vid=w0725m2uqwq"
    res = re.search(r"[\s\S]*?vid=([\w]+)[^\w]?", s)
    return res.group(1)


def get_source_url(vid):
    """
    通过vid 获取 源mp4 url
    :param vid: 
    :return: 
    """
    video_info = requests.get(
        temp_url.format(vid),
        timeout=30,
    )
    video_info_json = video_info.text[len('QZOutputJson='):-1]
    temp_str = json.loads(video_info_json)
    try:
        mp4_url = temp_str['vl']['vi'][0]['ul']['ui'][0]['url'] + temp_str['vl']['vi'][0]['fn'] + \
                  "?vkey=" + temp_str['vl']['vi'][0]['fvkey']
    except Exception as e:
        return "获取原视频url出错了{}".format(e)
    else:
        return mp4_url


if __name__ == '__main__':
    mp4_vid = get_vid()
    source_mp4_url = get_source_url(mp4_vid)
    print(source_mp4_url)
