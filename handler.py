import configparser
import json
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

# twitterAPI認証
def tweepy_oath():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)

def get_timeline(tweepy_api, cotoha_access_token):
    # タイムライン取得
    tweets = tweepy_api.user_timeline(
              screen_name='',
              count=10,
              tweet_mode='extended'
             )
    return tweets