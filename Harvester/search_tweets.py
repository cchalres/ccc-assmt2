import tweepy
import time
import couchdb
import json
from textblob import TextBlob

#This program is used to apply the search API method. We input the API authentication, database, query, 
#searching center and radius into this program to gain the tweets we want.

#https://docs.tweepy.org/en/latest/getting_started.html
#https://couchdb-python.readthedocs.io/en/latest/
#https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/overview




#Use Twitter search APIs find tweets from specific location.
class searcher():

    #Set variables required by Twitter Search API.
    def __init__(self, api, db, query, geo):
        
        self.api = api
        self.database = db
        self.query = query
        self.geo = geo
    
    
    def search(self):
        count = 100 #Every time harvest 100 tweets
        total = 0 #Simply count the total number
        slep = False #The switch of program sleeping or not
        last_id = None #The break point of the program

        #Start harvest
        while True:
            try:
                #If there is no break point
                if slep == False:
                    new_tweets = self.api.search(q = self.query, geocode = self.geo, count = count)
                
                #If the break point exist
                else:
                    new_tweets = self.api.search(q = self.query, geocode = self.geo, count = count, since_id = last_id)
                    slep = False
                
                #If all the tweets in database are harvested, stop the program
                if not new_tweets:
                    print("NO tweets in the Database!")
                    break
                
                #If there are more than one tweets been harvested
                if len(new_tweets) > 1:
                    for tweet in new_tweets:
                        json_tweet = tweet._json #Transform the data type

                        #Initially extract some useful information
                        id = json_tweet['id_str'] #The unique ID of each tweet
                        text = json_tweet["text"] #The text of each tweet
                        testimonial = TextBlob(text)
                        score = testimonial.sentiment.polarity #Analysis the sentiment score
                        time = json_tweet["created_at"] #The timestamp of post
                        language =json_tweet["lang"] #The language of the tweet
                        location = json_tweet["geo"] #The geo location information of this tweet

                        #Check duplicate
                        if id in self.database:
                            print("This tweet is already in the database!")
                        else:
                            info = {'_id': id, "time": time, "language": language, 'tweet': text, "points": score, "Geo": location, "all": json_tweet}
                            self.database.save(info)
                            total += 1
                    
                    #Ensure that the break point is updataed.
                    last_id = new_tweets[-1].id_str
                
                #If there is only one tweet been harvested
                #Here we need to change a little bit to transform its data type
                #Then repeat the steps above
                else:
                    json_tweet = new_tweets[0]._json
                    id = json_tweet['id_str']
                    text = json_tweet["text"]
                    testimonial = TextBlob(text)
                    score = testimonial.sentiment.polarity
                    time = json_tweet["created_at"]
                    language =json_tweet["lang"]   
                    location = json_tweet["geo"]                 
                    if id in self.database:
                        print("This tweet is already in the database!")
                    else:
                        info = {'_id': id, "time": time, "language": language, 'tweet': text, "points": score, "Geo": location, "all": json_tweet}
                        self.database.save(info)
                        total += 1

                    last_id = new_tweets[-1].id_str

            #Error handling
            except tweepy.RateLimitError:
                time.sleep(15*60)
                slep = True
            
            except tweepy.TweepError as e:
                print("TweepyError")
                break