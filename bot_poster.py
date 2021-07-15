import json
import time
import os
import argparse
import csv
import inspect
import sys
from pathlib import Path

from mastodon import Mastodon
import tweepy

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException


class Bot:
    def __init__(self, config):
        self.config = config
        self.subconfig = self.config[self.__class__.__name__]

    def loginandpost(self, text, image_filename):
        pass

class Neenster(Bot):
    def loginandpost(self, text, image_filename):
        print(image_filename)
        mastodon = Mastodon(**self.subconfig)
        media_id = mastodon.media_post(image_filename)
        mastodon.status_post(text, media_ids = media_id)

class BotsInSpace(Bot):
    def loginandpost(self, text, image_filename):
        print(image_filename)
        mastodon = Mastodon(**self.subconfig)
        media_id = mastodon.media_post(image_filename)
        mastodon.status_post(text, media_ids = media_id)

class Twitter(Bot):
    def loginandpost(self, text, image_filename):
        auth = tweepy.OAuthHandler(
            self.subconfig["api_key"],
            self.subconfig["api_secret_key"]
            )

        auth.set_access_token(
            self.subconfig['access_token'],
            self.subconfig['access_token_secret']
            )
        
        api = tweepy.API(auth)
        status = api.update_with_media(image_filename, status=text)

"""
class Facebook(Bot):
    def loginandpost(self, text, image_filename):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})

        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(5)

        driver.get("http://www.facebook.com")

        time.sleep(4)

        el = driver.find_element_by_id("email")
        el.send_keys(self.subconfig["usr"])

        el = driver.find_element_by_id("pass")
        el.send_keys(self.subconfig["pwd"])
        el.send_keys(Keys.RETURN)

        time.sleep(4)

        driver.get("https://www.facebook.com/groups/3577929125766069")
        time.sleep(4)

        html = driver.find_element_by_tag_name('html')
        [html.send_keys(Keys.PAGE_DOWN) for x in range(0,14)]

        whats_on_your_mind = driver.find_element_by_xpath('/html/body/
        div[1]/div/div[4]/div/div[1]/div[3]/div/div/div[1]/div/div[2]/div')
        post_input = whats_on_your_mind.find_element_by_xpath('..')
        post_input.click()
        el = driver.find_element_by_xpath('//*[@id="mount_0_0_U6"]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div[4]/div/div/div/div/div[1]/div[1]/div/div/div/div[2]/div/div[2]/div[2]')
        
        el.send_keys(image_filename)
        time.sleep(5)

        el = driver.find_element_by_xpath('//*[@id="mount_0_0_bG"]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/div')
        el.send_keys(text)
        el.send_keys(Keys.RETURN)

        el = driver.find_element_by_xpath('//*[@id="mount_0_0_eL"]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[3]/div[2]/div[1]/div/div/div[1]')
        el.click()
"""
        
def get_subclasses(mod, cls):
    """Yield the classes in module ``mod`` that inherit from ``cls``"""
    for name, obj in inspect.getmembers(mod):
        if hasattr(obj, "__bases__") and cls in obj.__bases__:
            yield obj

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='File to load the config from.', default='config.json')

    args = parser.parse_args()
    config_file = args.config

    c = json.load(open(config_file,'r'))
    rsrc_dir = c["rsrc_dir"]
    app_url = c["app_url"]
                       
    with open(Path(rsrc_dir, "to_post.csv"), 'r') as f:
        reader = csv.reader(f, skipinitialspace=True)
        image_filename = next(reader)[0]
        rows = list(reader)

    title = str(Path(image_filename).stem).replace("_"," ")
    text = f'"{title}"  {app_url}'
    image_filename = str(Path(rsrc_dir,"images",image_filename))
    
    print(f"Current file: {title}, {image_filename}")

    for BotClass in get_subclasses(sys.modules[__name__],Bot):
        bot = BotClass(c)
        try:
            bot.loginandpost(text,image_filename)
            print(f"Posted: {text}, {image_filename} with {BotClass.__name__}")
        except:
            print(f"Error occured for {BotClass.__name__} bot")
            pass
        

    with open(Path(rsrc_dir,'to_post.csv'), 'r+') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerows(rows)
        f.truncate()

    with open(Path(rsrc_dir,"posted.csv"), 'a') as f:
        csvwriter = csv.writer(f, quotechar='"', delimiter=',',
                     quoting=csv.QUOTE_ALL)
        csvwriter.writerow([title,image_filename])

    
if __name__ == '__main__':
    main()
    
