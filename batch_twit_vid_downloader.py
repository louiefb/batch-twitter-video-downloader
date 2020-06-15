import re
import requests
import time
import random

from selenium import webdriver

def download(url, filename, chunk_size=255):
    """ Downloads given url onto filename. Filename must include extensions. """
    print(f"Downloading {url} as '{filename}'...")
    r=requests.get(url)

    output = open(filename, "wb")
    for chunk in r.iter_content(chunk_size=chunk_size):
        if chunk:
            output.write(chunk)
    output.close()

    print(f"'{filename}' has been downloaded.")

def get_twitter_video(url, filename):
    print(f"Accessing '{url}'...")
    opts = webdriver.chrome.options.Options()
    opts.headless = True
    opts.add_experimental_option("prefs", {"safebrowsing.enabled": True})

    #turn on headerless browser
    browser = webdriver.Chrome(options=opts)
    browser.get(r"http://twittervideodownloader.com/")

    while True:
        try:
            #submit url to form
            submit_form = browser.find_element_by_class_name("input-group-field")
            submit_form.send_keys(url)
            submit_form.submit()

            #get url of highest resolution
            videos = browser.find_elements_by_partial_link_text("Download Video")
            links = [video.get_attribute("href") for video in videos]
            resolutions = [re.findall(r"\d+x\d+", link)[0] for link in links]
            max_res = max(resolutions, key=lambda res:int(res.split("x")[0]))
            max_idx = resolutions.index(max_res)
            break

        except ValueError:
            print(f"Requesting '{filename}' failed. Trying again...")

    browser.quit()

    #download video
    download(links[max_idx], filename)

def get_batch_videos():
    print("Please input url list. Hit Ctrl+D when done.")

    video_links = []
    while True:
        try:
            link = input()
        except EOFError:
            break
        video_links.append(link)

    for idx, link in enumerate(video_links):
        get_twitter_video(link, str(idx) + ".mp4")
        time.sleep(random.random())

if __name__ == "__main__":
    get_batch_videos()
