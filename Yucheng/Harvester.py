import json
import sys
import tweepy
import couchdb
import argparse
from tweepy import OAuthHandler

from search_tweets import searcher

#This is the main function of the harvester. What we do here is extract the required information from the config file and run the searcher.
#We assigned API's access and token, searching circle's center and radius, database's name in the config file.
#That's what we do in the beginning of this program.
#After having all the elements, we start the harvester.

#https://docs.tweepy.org/en/latest/getting_started.html
#https://couchdb-python.readthedocs.io/en/latest/
#https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/overview


#Get the API's access information and token information from the config file.
def get_credentials(config):
    with open(config) as f:
        json_config = json.load(f)

    try:
        consumer_key = json_config["Authentication"]["ConsumerKey"]
        consumer_secret = json_config["Authentication"]["ConsumerSecret"]
        access_token = json_config["Authentication"]["AccessToken"]
        access_secret = json_config["Authentication"]["AccessSecret"]
        
    except Exception as e:
        print("Authorization Error!")
        sys.exit(2)

    return consumer_key, consumer_secret, access_token, access_secret

#Get the center and radius of the searching circle.
def get_geo(config):
    with open(config) as f:
        json_config = json.load(f)

    try:
        geo = json_config["Locations"]["geo_range"]
        
    except Exception as e:
        print("No geo range provided!")
        sys.exit(3)
    return geo

#Get the authentication and name of the database.
def get_db(config, ip):
    with open(config) as f:
        json_config = json.load(f)

    try:
        admin = json_config["Database"]["admin"]
        password = json_config["Database"]["password"]

        tweet_db_name = json_config["Database"]["tweets_db"]

        server = couchdb.Server("http://" + admin + ":" + password + "@"+ip+":5984/")
        
        #Check the duplication of database
        if tweet_db_name in server:
            print(tweet_db_name + " has already in the server!")
            tweet_db = server[tweet_db_name]
        else:
            print("Create " + tweet_db_name +" in the server!")
            tweet_db = server.create(tweet_db_name)
        
    except Exception as e:
        print("Problems happened in the db part")
        sys.exit(4)
        
    return tweet_db

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", required = True)
    parser.add_argument("-s", "--server", required = True)
    args = parser.parse_args()

    config = args.config
    ip = args.server
    
    #Input of Searcher
    consumer_key, consumer_secret, access_token, access_secret = get_credentials(config)
    geo = get_geo(config)
    tweet_db= get_db(config, ip)

    #Authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

    #Start running the harvester
    try:
        search_api = searcher(api, tweet_db, '*', geo)
        search_api.search()
    
    except Exception as e:
        print("Problem happend in search!")
        sys.exit(5)