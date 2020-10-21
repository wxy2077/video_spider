# 抓取抖音分享的接口


## 实现逻辑

注意:全程得用移动端ua才行(以下测试全程用的iPhone7UA)，chrome直接打不开。

- 1 通过分享的短链接，获取长链接
  - 如分享短链接 https://v.douyin.com/JPa1xhq/
  - 直接访问获取到长链接 https://www.iesdouyin.com/share/video/6883418578486349070/?region=CN&mid=6883418927515421454&u_code=0&titleType=title&did=59084494265&iid=2304201954427479&utm_source=copy_link&utm_campaign=client_share&utm_medium=android&app=aweme

- 2 获取video_id
  - 直接正则获取到上图的video后面的一串数字，video_id即上面链接中的6883418578486349070

- 3 拼接video_id获取，视频信息json数据
  - 上面video_id拼接成如下结果
  - https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=6883418578486349070

- 4 获取上面json数据中想要的数据
  - json数据基本包含了，作者信息，视频信息(封面，bgm, 视频链接)如下：
  ```
  # 如下视频信息播放地址(默认包含水印)
  {
    "uri": "v0300f9f0000bu3ctfaajd99kv7dbidg",
    "url_list": [
        "https://aweme.snssdk.com/aweme/v1/playwm/?video_id=v0300f9f0000bu3ctfaajd99kv7dbidg&ratio=720p&line=0"
    ]
  }
  ``` 
- 5 获取无水印的视频
  - 第4步中获取的播放地址是包含水印的，获取无水印的也简单   
  - 把视频url参数中的`playwm`替换成`play` (wm 没猜错就是`water mark`:水印的首字母缩写)
  - https://aweme.snssdk.com/aweme/v1/play/?video_id=v0300f9f0000bu3ctfaajd99kv7dbidg&ratio=720p&line=0
 
 
## Python FastAPI框架实现抖音分享解析API
 
`success` 示例

```
{
  "code": 200,
  "msg": "success",
  "data": {
    "videoUrl": "https://aweme.snssdk.com/aweme/v1/play/?video_id=v0300f9f0000bu3ctfaajd99kv7dbidg&ratio=720p&line=0",
    "videoId": "v0300f9f0000bu3ctfaajd99kv7dbidg",
    "title": "重庆，迷一样的城市 这样的道路是来考验技术的#重庆美好推荐官  #我的家乡在重庆   #神操作  #心动的旅行",
    "cover": [
      "https://p9-dy.byteimg.com/img/tos-cn-i-0813/48f2b080e29a45088c896249d8294455~tplv-dmt-logoccm:300:400:tos-cn-i-0813/f7008a75e28f406dac080d2048f33540.jpeg?from=2563711402_large",
      "https://p6-dy-ipv6.byteimg.com/img/tos-cn-i-0813/48f2b080e29a45088c896249d8294455~tplv-dmt-logoccm:300:400:tos-cn-i-0813/f7008a75e28f406dac080d2048f33540.jpeg?from=2563711402_large",
      "https://p3-dy-ipv6.byteimg.com/img/tos-cn-i-0813/48f2b080e29a45088c896249d8294455~tplv-dmt-logoccm:300:400:tos-cn-i-0813/f7008a75e28f406dac080d2048f33540.jpeg?from=2563711402_large"
    ]
  }
}
```

 
## 如何运行

#### 安装依赖

python3.6+

```
pip install -r requirements.txt -i https://pypi.douban.com/simple
```

#### 启动
```
# 官方命令启动
uvicorn main:app --host=127.0.0.1 --port=8130 --workers=4

# or

python main.py
```

#### 在线swagger文档地址
```
http://127.0.0.1:8130/docs
```

## Docker方式 运行 测试启动失败
```
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./main.py /app

COPY ./requirements.txt /app

CMD cd /app

RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.douban.com/simple

CMD uvicorn main:app --host=0.0.0.0 --port=8130 --workers=4


docker build -t douyin .

docker run -d --name api_tool -p 8050:8050 douyin

```