# Toutiao_spider
爬取今日头条视频

### 声明:仅供学习使用，切勿用于其他用途
- 步骤
  - 1 先通过今日头条APP,charles抓包工具抓包,抓取视频列表页接口,列表页可改变部分参数，一直循环获取.(注意:要加延迟，友好一点，不对服务器造成负担)
  - 2 循环列表页，访问详细页， 通过正则获取videoId.
  - 3 通过接口 http://i.snssdk.com/video/urls/1/toutiao/mp4/{videoId} 获取原视频详细信息： 如 http://i.snssdk.com/video/urls/1/toutiao/mp4/v02004d10000bfhquksuatle7ofug3v0
  - 4 原视频详细信息，有不同清晰度的，选择一个清晰度的main_url 然后base64解码 就得到了原视频链接，注意原视频链接是有时间限制的。
  
#### 新增腾讯视频 原始url 源视频连接获取方式
- [tencent_video.py](https://github.com/wgPython/Toutiao_spider/blob/master/tencent_video)
