import tweepy
from key import bearer_token, key, secret, access, access_secret
import json
import nltk
import pycountry
from textblob import TextBlob

from PIL import Image
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from langdetect import detect
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer


polarity = 0
tweet_list = []
neutral_list = []
negative_list = []
positive_list = []

def sentiment_analysis(text):
    positive = 0
    neutral = 0
    negative = 0
    score = SentimentIntensityAnalyzer().polarity_scores(text)
    polarity, subjectivity = TextBlob(text).sentiment
    if score['neg'] > score['pos']:
        negative_list.append(text)
        negative += 1
    elif score['pos'] > score['neg']:
        positive_list.append(text)
        positive += 1   
    elif score['pos'] == score['neg']:
        neutral_list.append(text)
        neutral += 1
    print(positive, neutral, negative, polarity, subjectivity)



auth = tweepy.OAuthHandler(key, secret)
auth.set_access_token(access, access_secret)
api = tweepy.API(auth)
# print(api.rate_limit_status())
client = tweepy.Client(bearer_token=bearer_token)

with open("events/accounts.json", 'r') as f:
    list_accounts = json.load(f)
users = client.get_users(usernames=list_accounts)
ids = [us.id for us in users.data]

class Alerting(tweepy.Stream):

    def on_status(self, status):
        if status.user.name in list_accounts:
            print('WARNING: ', status.user.name, 'has posted')
        elif status.user.followers_count > 5000:
            if status.user.followers_count > 100000 and status.user.followers_count not in list_accounts:
                list_accounts.append(status.user.name)
                with open("events/accounts.json","w") as file:
                   json.dump(list_accounts, file)
                sentiment_analysis(status.text)
            print('big account',status.user.name, status.user.followers_count)


keywords = Alerting(key,secret,access,access_secret)
keywords.filter(track=["Bitcoin","BTC","Ethereum","ETH","Blockchain"], languages=["en"])
keywords.sample()

accounts = Alerting(key,secret,access, access_secret)
accounts.filter(follow=ids)
accounts.sample()



