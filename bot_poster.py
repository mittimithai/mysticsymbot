import json
import time
import os
import argparse
import csv
import inspect
import sys

from mastodon import Mastodon
import tweepy

class Bot:
    def __init__(self, config):
        self.config = config
        self.subconfig = self.config[self.__class__.__name__]

    def loginandpost(self, text, image_filename):
        pass

class Neenster(Bot):
    def loginandpost(self, text, image_filename):
        mastodon = Mastodon(**self.subconfig)
        media_id = mastodon.media_post(image_filename)
        mastodon.status_post(text, media_ids = media_id)

class BotsInSpace(Bot):
    def loginandpost(self, text, image_filename):
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
                       
    with open(os.path.join(rsrc_dir,"to_post.csv"), 'r') as f:
        reader = csv.reader(f, quotechar='"', delimiter=',',
                     quoting=csv.QUOTE_ALL, skipinitialspace=True)
        title,image_filename = next(reader)
        rows = list(reader)

    text = f'"{title}"  {app_url}'
    image_filename = os.path.join(rsrc_dir,"images",image_filename)    
    
    print(f"Current file: {title}, {image_filename}")

    for BotClass in get_subclasses(sys.modules[__name__],Bot):
        bot = BotClass(c)
        bot.loginandpost(text,image_filename)
        print(f"Posted: {text}, {image_filename} with {BotClass.__name__}")
        

    with open(os.path.join(rsrc_dir,'to_post.csv'), 'r+') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerows(rows)
        f.truncate()

    with open(os.path.join(rsrc_dir,"posted.csv"), 'a') as f:
        csvwriter = csv.writer(f, quotechar='"', delimiter=',',
                     quoting=csv.QUOTE_ALL)
        csvwriter.writerow([title,image_filename])

    
if __name__ == '__main__':
    main()
    
