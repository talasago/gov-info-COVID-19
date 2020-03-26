import configparser
import json
import os
import sys
import re
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
from lib import tweepy

# ローカル開発用
OAUTH_INI = configparser.ConfigParser()
OAUTH_INI.read('oauth.ini', encoding='utf-8')
# TODO:lambdaの環境変数に都県を記載
CONSUMER_KEY = OAUTH_INI['twitter_API']['CONSUMER_KEY']
CONSUMER_SECRET = OAUTH_INI['twitter_API']['CONSUMER_SECRET']
ACCESS_TOKEN = OAUTH_INI['twitter_API']['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = OAUTH_INI['twitter_API']['ACCESS_TOKEN_SECRET']


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
    exclude_exp_obj = re.compile(r'.*[コロナ|COVID].*$')

    for tweet in tweepy_api.home_timeline(count=50):
        if exclude_exp_obj.match(tweet.text):
            id = tweet.id

            try:
              tweepy_api.create_favorite(id)
              tweepy_api.retweet(id)
            # 例外発生はログだけ残して処理停止はしない
            except:
              print(sys.exc_info())
              pass
