import tweepy
import json
import couchdb

auth = tweepy.OAuthHandler("B1YMqtkC4pUt4jrC0hwCIWM7j", "0gd00U1TkhmU2DVGLvebE8VmefsS5YVsiYT5kWLtXlDKkmiYjy")
auth.set_access_token("1110906258272313344-8wkeDsdpALCmASt3YcoNj2ZsPAz0DL", "WlGjdg2SjIoPmC6QAk6XQY8AzCXthhsyfqFhr3LMkbyWJ")


api = tweepy.API(auth)


admin = "admin"
password = "admin"
ip = '127.0.0.1'

db_name = 'test'
server = couchdb.Server('http://' + admin + ':' + password + '@'+ip+':5984/')
if db_name in server:
    print("This database is already in the server!")
    db = server[db_name]
else:
    print("Create database: {}".format(db_name))
    db = server.create(db_name)


count = 10
limit = 100
total = 0
slep = False
last_id = None
geo = "-37.813628,144.963058,5km"
while total < limit:
    new_tweets = api.search(q = '*', geocode = geo, count = count)
                
    if len(new_tweets) > 1:
        for tweet in new_tweets:
            json_tweet = tweet._json
            total += 1
        
            id = json_tweet["user"]["id"]
            name = json_tweet["user"]["name"]
            location = json_tweet["user"]["location"]
            user_doc = {'id': id, 'name': name, 'location': location}
            db.save(user_doc)



    else:
        json_tweet = tweet[0]._json
        total += 1
        id = json_tweet["user"]["id"]
        name = json_tweet["user"]["name"]
        location = json_tweet["user"]["location"]
        user_doc = {'id': id, 'name': name, 'location': location}
        db.save(user_doc)
    
    print("Total is: {}".format(total))




