from pymongo import MongoClient
import requests
import os
import hashlib
import time
import threading

client = MongoClient('localhost')
db = client.twitter
collection = db.video_sexy

path = os.path.dirname(__file__)

proxy = "127.0.0.1:1087"

proxies={
    'http': 'http://' + proxy,
    'https': 'https://' + proxy
}

lock = threading.Lock()

def download_video(videos):
    while videos:
        lock.acquire()
        video = videos[0]
        del videos[0]
        lock.release()
        # t = threading.Thread(target=download, args=(video["video_url"],))
        # t.start()
        download(video["video_url"])
    # for video in videos:
    #     print("url is", video["video_url"])
    #     t = threading.Thread(target=download(), args=(video["video_url"],))
    #     t.start()




def download(url):
    print("url is", url)
    try:
        response = requests.get(url, proxies=proxies)
        with open((path + "/video/{}.mp4").format(get_md5(url)), "wb") as f:
            f.write(response.content)
    except Exception as e:
        print(e)

def get_md5(url):
    m = hashlib.md5()
    if isinstance(url, str):
        url = url.encode('utf-8')
    m.update(url)
    return m.hexdigest()


if __name__ == "__main__":
    temps = collection.find({"video_url": {'$regex': '^http.*'}})
    videos = list(temps)
    for i in (1,10):
        t = threading.Thread(target=download_video, args=(videos,))
        t.start()