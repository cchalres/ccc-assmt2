import tweepy
import time
import couchdb
import json
from textblob import TextBlob

class searcher():
    """Use Twitter search APIs find tweets from specific location."""

    def __init__(self, api, db, query, geo):
        """Set variables required by Twitter Search API."""
        self.api = api
        self.database = db
        self.query = query
        self.geo = geo
    
    
    def search(self):
        count = 100
        total = 0
        slep = False
        last_id = None
        while True:
            try:
                if slep == False:
                    new_tweets = self.api.search(q = self.query, geocode = self.geo, count = count)
                else:
                    new_tweets = self.api.search(q = self.query, geocode = self.geo, count = count, since_id = last_id)
                    slep = False
                
                if not new_tweets:
                    print("NO tweets in the Database!")
                    break

                if len(new_tweets) > 1:
                    for tweet in new_tweets:
                        json_tweet = tweet._json

                        id = json_tweet['id_str']
                        text = json_tweet["text"]
                        testimonial = TextBlob(text)
                        score = testimonial.sentiment.polarity
                        if id in self.database:
                            print("This tweet is already in the database!")
                        else:
                            info = {'_id': id, 'tweet': text, "points": score}
                            self.database.save(info)
                            total += 1

                    last_id = new_tweets[-1].id_str
                else:
                    json_tweet = new_tweets[0]._json
                    id = json_tweet['id_str']
                    text = json_tweet["text"]
                    testimonial = TextBlob(text)
                    score = testimonial.sentiment.polarity                    
                    if id in self.database:
                        print("This tweet is already in the database!")
                    else:
                        info = {'_id': id, 'tweet': text, "points": score}
                        self.database.save(info)
                        total += 1

                    last_id = new_tweets[-1].id_str

            except tweepy.RateLimitError:
                time.sleep(15*60)
                slep = True
            
            except tweepy.TweepError as e:
                print("TweepyError")
                break