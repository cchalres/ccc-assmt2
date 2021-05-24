import tweepy
from tweepy import OAuthHandler, Stream, StreamListener
import json
import couchdb
from textblob import TextBlob

class stream_searcher(StreamListener):

    def __init__(self, tweets_db, user_db):
        self.tweets_db = tweets_db
        self.user_db = user_db
    
    def on_data(self, data):
        print(data)
        
        json_tweet = json.loads(data)
        tweet_id = json_tweet['id_str']
        text = json_tweet["text"]
        testimonial = TextBlob(text)
        score = testimonial.sentiment.polarity

        user_id = str(json_tweet["user"]['id'])
        user_name = json_tweet["user"]['name']
        user_des = json_tweet["user"]["description"]
        
        if tweet_id in self.tweets_db:
            print("This tweet has already in the database!")
        else:
            tweet_info = {"_id": tweet_id, "text": text, "points": score}
            self.tweets_db.save(tweet_info)

        if user_id in self.user_db:
            print("This user has already in the database!")
        else:
            user_info = {"_id": user_id, "name": user_name, "user_description": user_des}
            self.user_db.save(user_info)

        return True

    def on_error(self, status):
        print(status)