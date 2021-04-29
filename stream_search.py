import tweepy
from tweepy import OAuthHandler, Stream, StreamListener
import json
import couchdb

consumer_key="B1YMqtkC4pUt4jrC0hwCIWM7j"
consumer_secret="0gd00U1TkhmU2DVGLvebE8VmefsS5YVsiYT5kWLtXlDKkmiYjy"

access_token="1110906258272313344-8wkeDsdpALCmASt3YcoNj2ZsPAz0DL"
access_token_secret="WlGjdg2SjIoPmC6QAk6XQY8AzCXthhsyfqFhr3LMkbyWJ"

class StdOutListener(StreamListener):

    def __init__(self, tweets_db, user_db, location):
        self.tweets_db = tweets_db
        self.user_db = user_db
        self.location = location
        self.tweet_count = 0
        self.user_count = 0
    
    def on_data(self, data):
        json_tweet = json.loads(data)
        id = json_tweet['id_str']
        text = json_tweet["text"]
        user_id = str(json_tweet["user"]['id'])
        print(json_tweet)
        return True

    def on_error(self, status):
        print(status)

'''
if __name__ == '__main__':
    l = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(locations = [144.947,-38.468,145.0659,-36.882])
'''
