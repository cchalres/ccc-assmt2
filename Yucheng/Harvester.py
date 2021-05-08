import json
import sys
import tweepy
import couchdb
import argparse
from tweepy import OAuthHandler, Stream, StreamListener

from search_tweets import searcher
from stream_search import stream_searcher

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

def get_location(config):
    with open(config) as f:
        json_config = json.load(f)

    try:
        bounding_box = [float(json_config["Locations"]["box"][0]),
                        float(json_config["Locations"]["box"][1]),
                        float(json_config["Locations"]["box"][2]),
                        float(json_config["Locations"]["box"][3])]
            
        location = json_config["Locations"]["location"]
        
    except Exception as e:
        print("No bounding box coordinates or location name!")
        sys.exit(3)
    
    return bounding_box, location

def get_geo(config):
    with open(config) as f:
        json_config = json.load(f)

    try:
        geo = json_config["Locations"]["geo_range"]
        
    except Exception as e:
        print("No geo range provided!")
        sys.exit(4)
    return geo

def get_db(config, ip):
    with open(config) as f:
        json_config = json.load(f)

    try:
        admin = json_config["Database"]["admin"]
        password = json_config["Database"]["password"]

        tweet_db_name = json_config["Database"]["tweets_db"]
        user_db_name = json_config["Database"]["user_db"]

        server = couchdb.Server("http://" + admin + ":" + password + "@"+ip+":5984/")

        if tweet_db_name in server:
            print(tweet_db_name + " has already in the server!")
            tweet_db = server[tweet_db_name]
        else:
            print("Create " + tweet_db_name +" in the server!")
            tweet_db = server.create(tweet_db_name)
            
        if user_db_name in server:
            print(user_db_name + " has already in the server!")
            user_db = server[user_db_name]
        else:
            print("Create " + user_db_name +" in the server!")
            user_db = server.create(user_db_name)
        
    except Exception as e:
        print("Problems happened in the db part")
        sys.exit(5)
        
    return tweet_db, user_db

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", required = True)
    parser.add_argument("-s", "--server", required = True)
    parser.add_argument("-m", "--method", default = "search", required = False)
    args = parser.parse_args()

    config = args.config
    ip = args.server
    method = args.method
    
    consumer_key, consumer_secret, access_token, access_secret = get_credentials(config)
    bounding_box, location = get_location(config)
    geo = get_geo(config)
    tweet_db, user_db = get_db(config, ip)

    if method == "search":
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

        search_api = searcher(api, tweet_db, '*', geo)
        search_api.search()
    
    elif method == "stream":
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        
        l = stream_searcher(tweet_db, user_db)
        stream = Stream(auth, l)
        stream.filter(locations = bounding_box)