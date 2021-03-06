import configparser
import json
import os
import sys
import re
import logging
import traceback
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
from lib import tweepy

# ローカル開発用
OAUTH_INI = configparser.ConfigParser()
OAUTH_INI.read('oauth.ini', encoding='utf-8')
# TODO:lambdaの環境変数に都県を記載
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']


def main(event, context):
    tweepy_api = tweepy_oath()
    retweet(tweepy_api)

# twitterAPI認証
def tweepy_oath():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)

# 自分のタイムラインから対象の単語が入っているツイートをリツイート
def retweet(tweepy_api):
    exclude_exp_obj = re.compile(r'.*(コロナ|COVID)(.|\s)*$')

    for tweet in tweepy_api.home_timeline(count=200):
        if exclude_exp_obj.match(tweet.text):
            id = tweet.id
            print(tweet.text)
            print(tweet.id)

            try:
                tweepy_api.create_favorite(id)
                tweepy_api.retweet(id)
            # 例外発生はログだけ残して処理停止はしない
            except:
                logging.error(traceback.format_exc())
                pass
