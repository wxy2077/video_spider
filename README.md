# video_spider

## 声明:仅供学习使用，切勿用于其他用途

## 今日头条视频 

[今日头条 toutiao_video.py](./toutiao_video.py)

<details>
<summary>逻辑分析</summary>

```
1 先通过今日头条APP,charles抓包工具抓包,抓取视频列表页接口,列表页可改变部分参数，一直循环获取.(注意:要加延迟，友好一点，不对服务器造成负担)
2 循环列表页，访问详细页， 通过正则获取videoId.
3 通过接口 http://i.snssdk.com/video/urls/1/toutiao/mp4/{videoId} 获取原视频详细信息： 如 http://i.snssdk.com/video/urls/1/toutiao/mp4/v02004d10000bfhquksuatle7ofug3v0
4 原视频详细信息，有不同清晰度的，选择一个清晰度的main_url 然后base64解码 就得到了原视频链接，注意原视频链接是有时间限制的。
```

</details>


## 🍉西瓜视频

[西瓜视频 xi_gua.py](./xi_gua.py)

## 腾讯视频 
> 原始url 源视频连接获取方式
[腾讯视频 tencent_video.py](./tencent_video.py)

## 抖音分享链接解析

[抖音分享链接解析，获取无水印视频链接](./douyin_share/README.md)

<details>
<summary>解析逻辑</summary>

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
 
</details>
 
> 已使用FastAPI封装 成接口, 测试分享短链接: https://v.douyin.com/JPa1xhq/

<details>
<summary>API解析分享返回json数据示例</summary>

```json
{
    "code": 200,
    "msg": "success",
    "data": {
        "videoUrl": "https://aweme.snssdk.com/aweme/v1/play/?video_id=v0300f9f0000bu3ctfaajd99kv7dbidg&ratio=720p&line=0",
        "videoId": "v0300f9f0000bu3ctfaajd99kv7dbidg",
        "title": "重庆，迷一样的城市 这样的道路是来考验技术的#重庆美好推荐官  #我的家乡在重庆   #神操作  #心动的旅行",
        "cover": [
            "https://p3-dy-ipv6.byteimg.com/img/tos-cn-i-0813/48f2b080e29a45088c896249d8294455~tplv-dmt-logoccm:300:400:tos-cn-i-0813/f7008a75e28f406dac080d2048f33540.jpeg?from=2563711402_large",
            "https://p1-dy-ipv6.byteimg.com/img/tos-cn-i-0813/48f2b080e29a45088c896249d8294455~tplv-dmt-logoccm:300:400:tos-cn-i-0813/f7008a75e28f406dac080d2048f33540.jpeg?from=2563711402_large",
            "https://p29-dy.byteimg.com/img/tos-cn-i-0813/48f2b080e29a45088c896249d8294455~tplv-dmt-logoccm:300:400:tos-cn-i-0813/f7008a75e28f406dac080d2048f33540.jpeg?from=2563711402_large"
        ]
    }
}
```

</details>

## m3u8 视频下载

[m3u8_down 仅供参考](./m3u8_download/README.md)
