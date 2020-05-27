# twitter_video_scraper
crawl twitter video 

爬取twitter个人主页视频。

目前仅实现手动输入user_id来爬取某个用户的twitter时间线的视频文件。

可以爬取个人首页上时间线的所有用户的，或者following用户或者follower用户的id，然后批量获取时间线视频，这里没有去做这个。

这个好实现，http请求地址和请求参数已有。这里就不具体介绍了。


用浏览器工具分析得到获取timeline的api，以及params参数，下拉翻页用的是cursor，首次加载cursor为空，以后每次的cursor都是从前一次的api中返回的。 因为twitter不能访问，所以记得这里要设置代理。header里面还要添加cookie信息
``` python
def crawl_data(cursor_id):
    if cursor_id == "":
        url = "https://api.twitter.com/2/timeline/profile/{}.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_composer_source=true&include_ext_alt_text=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&include_tweet_replies=false&userId={}&count=20&ext=mediaStats%2ChighlightedLabel%2CcameraMoment".format(user_id,user_id);
    else:
        url = "https://api.twitter.com/2/timeline/profile/{}.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_composer_source=true&include_ext_alt_text=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&include_tweet_replies=false&userId={}&count=20&ext=mediaStats%2ChighlightedLabel%2CcameraMoment&cursor={}".format(user_id,user_id,cursor_id);
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.status_code == 200:
        print("response is: ",response)
        try:
            response_dic = json.loads(response.text)
            # 获取图片地址，存入数据库
            # handle_pic(response_dic)
            #获取视频地址，存入数据库
            handle_video(response_dic)
            # 获取cursor 翻下一页
            request_next(response_dic)
        except Exception as e:
            print('error is ', e)

```

解析json，获得视频的下载地址。有多个码率，获取码率最大的那个，清晰度最好。

``` python
def handle_video(dic):
    # 获取视频下载地址 并存入数据库
    tweets_dic = dic["globalObjects"]["tweets"]
    if tweets_dic == '':
        return
    tweets = tweets_dic.values()
    video_url_list = []
    for tweet in tweets:
        if "extended_entities" in tweet:
            media = tweet["extended_entities"]["media"][0]
            if "video_info" in media.keys():
                videos = media["video_info"]["variants"]
                max = 0
                video_url = ""
                for video in videos:
                    if video["content_type"] == "video/mp4":
                        # 排序 选出码率最大的视频
                        if video["bitrate"] > max:
                            max = video["bitrate"]
                            video_url = video["url"].split("?tag")[0]
                video_url_list.append({"video_url": video_url})
                print('url is ',video_url, 'bitrate is', max)
                # download_mp4(video_url)
    # print("video get successed, video_urls is", video_url_list)
    save_mongo(video_url_list)
```

爬取下拉后的新一页：
``` python
def request_next(dic):
    instructions = dic["timeline"]["instructions"]
    for instruction in instructions:
        if "addEntries" in instruction.keys():
            entries = instruction["addEntries"]["entries"]
            for entry in entries:
                content = entry["content"]
                if "operation" in content.keys():
                    #带有cursor的字典
                    cursor = content["operation"]["cursor"]
                    if "stopOnEmptyResponse" in cursor.keys():
                        #最终的cursor
                        cursor_id = cursor["value"]
                        print("cursor_id is ",cursor_id)
                        break
    # 获得cursor_id后爬取下一页
    time.sleep(5)
    if cursor_id != "":
        crawl_data(cursor_id)
```

最后从mongo读取出下载地址，用多线程下载。
``` python
if __name__ == "__main__":
    temps = collection.find({"video_url": {'$regex': '^http.*'}})
    videos = list(temps)
    for i in (1,10):
        t = threading.Thread(target=download_video, args=(videos,))
        t.start()
```

开始下载
``` python
def download_video(videos):
    while videos:
        lock.acquire()
        video = videos[0]
        del videos[0]
        lock.release()
        download(video["video_url"])

def download(url):
    print("url is", url)
    try:
        response = requests.get(url, proxies=proxies)
        with open((path + "/video/{}.mp4").format(get_md5(url)), "wb") as f:
            f.write(response.content)
    except Exception as e:
        print(e)
```
爬了几个用户的页面，下了几百个视频，还有一些下载失败了，503。被屏蔽了吧。

![](http://ww1.sinaimg.cn/large/007dl3HPly1g5o0c9opw4j304i05ot93.jpg)
