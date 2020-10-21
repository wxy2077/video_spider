#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/20 16:52
# @Author  : CoderCharm
# @File    : main.py
# @Software: PyCharm
# @Github  : github/CoderCharm
# @Email   : wg_python@163.com
# @Desc    :
"""
获取抖音分享链接的视频

pip install fastapi
pip install uvicorn
pip install requests

"""
import re
import urllib3
import traceback

import requests

from loguru import logger
from fastapi import FastAPI, Body, Request

urllib3.disable_warnings()

app = FastAPI(
    # 关闭各种在线文档,需要打开直接注释就行
    # openapi_url=None,
    # docs_url=None,
    # redoc_url=None,
    # swagger_ui_oauth2_redirect_url=None
)


@app.exception_handler(Exception)
async def request_validation_exception_handler(request: Request, exc: Exception):
    """
    请求参数验证异常
    :param request: 请求头信息
    :param exc: 异常对象
    :return:
    """
    # 日志记录异常详细上下文
    logger.error(f"全局异常\nURL{request.url}\n\n{traceback.format_exc()}")
    return {"code": 500, "msg": f"error: {traceback.format_exc()}"}

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
}


@app.post("/dy/share/url/parse")
async def dy_share(
        share_url: str = Body(..., alias="shareUrl", title='分享的URL', embed=True),
):
    video_id = fetch_video_id(share_url)

    video_info = fetch_video_info(video_id)

    return {"code": 200, "msg": "success", "data": video_info}


# 以下函数皆为同步函数
def fetch_video_id(share_url: str) -> str:
    """
    通过分享链接获取video_id
    :param share_url:
    :return:
    """
    resp = requests.get(share_url, headers=headers, timeout=10, verify=False)
    video_id = re.search(r"video/(\d+)/", resp.url)
    return video_id.group(1)


def fetch_video_info(video_id: str) -> dict:
    """
    获取视频信息
    :param video_id:
    :return:
    """
    url = f"https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={video_id}"
    resp = requests.get(url, headers=headers, timeout=10, verify=False)
    video_json_info = resp.json().get("item_list")[0]

    # 获取到视频链接
    video_url = video_json_info.get("video").get("play_addr").get("url_list")[0]
    video_url = replace_vm(video_url)

    video_info = {
        "videoUrl": video_url,
        "videoId": video_json_info.get("video").get("play_addr").get("uri"),
        "title": video_json_info.get("desc"),
        "cover": video_json_info.get("video").get("cover").get("url_list"),
    }
    return video_info


def replace_vm(url: str) -> str:
    """
    替换掉去水印掉
    :param url:
    :return:
    """
    return url.replace("playwm", "play")


if __name__ == "__main__":
    import uvicorn

    # 官方推荐是用命令后启动 在main.py同文件下下启动
    # uvicorn main:app --host=127.0.0.1 --port=8130 --workers=4
    uvicorn.run(app='main:app', host="127.0.0.1", port=8130, reload=True, debug=True)
