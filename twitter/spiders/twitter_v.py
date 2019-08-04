# 爬取twitter指定用户的视频

import requests
import json
import hashlib
import urllib.parse
from pymongo import MongoClient
import time
from lxml import etree

# 获取首页列表
# url = "https://api.twitter.com/2/timeline/home.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_composer_source=true&include_ext_alt_text=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&earned=1&count=20&lca=true&ext=mediaStats%2ChighlightedLabel%2CcameraMoment"

proxy = "127.0.0.1:1087"

proxies={
    'http': 'http://' + proxy,
    'https': 'https://' + proxy
}

# user_id = "986488498109562881" # 妖姬  https://twitter.com/wanjucute
# user_id = "1073177482537295873" # 阿朱啊 https://twitter.com/azhua1997
# user_id = "944521982007238656" #是肉肉本人 https://twitter.com/babebabe_y
# user_id = "1118012614506713089" #完具 https://twitter.com/Curries_baby
# user_id = "1140635967696490496" #rourou https://twitter.com/rourou233
# user_id = "1101105195356966912" #qiuqiu https://twitter.com/qiuqiu918
# user_id = "1105575933778513920" #露西 https://twitter.com/bennett29938
# user_id = "1112253205067358208" #樱崽ovo https://twitter.com/yizhipijiang
# user_id = "1097475087299735553" # https://twitter.com/youyincute
# user_id = "1098019793544724480" # https://twitter.com/WGloia
# user_id = "1072361969984761856" #https://twitter.com/llllllll520
user_id = "1127067376162205696" #https://twitter.com/CandyTt0211

client = MongoClient('localhost')
db = client.twitter
video_collection = db.video_sexy
pic_collection = db.pic_sexy

#请求头
headers = {
    "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
    "x-csrf-token": "b232f0ccf098109f604c5b337ab129c8",
    "x-twitter-active-user": "yes",
    "x-twitter-auth-type": "OAuth2Session",
    "x-twitter-client-language": "en",
    "Cookie": 'moments_profile_moments_nav_tooltip_self=true; co=us; moments_profile_moments_nav_tooltip_other=true; remember_checked_on=1; _ga=GA1.2.2110148524.1496804068; kdt=5FJgKGLJ1mOkWXItakp3MBFGxe9Yi98gth2BHcjL; csrf_same_site_set=1; csrf_same_site=1; lang=en; guest_id=v1%3A156473141970109415; ct0=b232f0ccf098109f604c5b337ab129c8; _gid=GA1.2.1496508497.1564731649; _sl=1; personalization_id="v1_wT+QRVEdFRwEHNeoY11Yyw=="; rweb_optin=side_no_out; ads_prefs="HBIRAAA="; _twitter_sess=BAh7CiIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCCy6iVFsAToMY3NyZl9p%250AZCIlYTU3MzI3ZTAwZTZhNzRlNzNmN2VlNmQ4ZGUzMDRmMzI6B2lkIiVkZDE5%250ANTQxMjNkODJlYzMxNGM0ZmY1OTg1Njg0MDQ2MToJdXNlcmkEoNgvDg%253D%253D--d395ad12612b86156fd5a5270daa32841b38ced5; auth_token=c73ac5c65383f741ad838ad2209790f3406dee0a; twid=u%3D238016672"'
}

# def get_home():
#     response = requests.get(url, headers=headers, proxies=proxies)
#     try:
#         with open("home.json","w") as f:
#             f.write(response.text)
#     except Exception as e:
#         print(e)


def crawl_img():
    url = "https://twitter.com/CandyTt0211"
    response = requests.get(url, headers=headers, proxies=proxies)
    print(response)
    # html = etree.HTML(response.content)
    # img_url = html.xpath("//div[@aria-label='Image']//img/@src")
    # print(img_url)



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

def handle_pic(dic):
    pass


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


def save_mongo(urls):
    if urls.count == 0:
        return
    video_collection.insert_many(urls)
    print("mongo save successed")


def get_md5(url):
    m = hashlib.md5()
    if isinstance(url, str):
        url = url.encode('utf-8')
    m.update(url)
    return m.hexdigest()


def download_mp4(url):
    if url == "":
        return;
    response = requests.get(url, headers=headers,proxies=proxies)
    try:
        with open("{}.mp4".format(get_md5(url)),"wb") as f:
            f.write(response.content)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    # crawl_data("")
    crawl_img();