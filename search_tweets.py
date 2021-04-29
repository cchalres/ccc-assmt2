import tweepy
import time
import couchdb

class search_tweets():
    """Use Twitter search APIs find tweets from specific location."""

    def __init__(self, api, db, query, geo):
        """Set variables required by Twitter Search API."""
        self.api = api
        self.database = db
        self.query = query
        self.geo = geo
    
    
    def search(self):
        count = 10
        limit = 100
        total = 0
        slep = False
        last_id = None
        while total < limit:
            try:
                if slep == False:
                    new_tweets = self.api.search(q = self.query, geocode = self.geo, count = count)
                else:
                    new_tweets = self.api.search(q = self.query, geocode = self.geo, count = count, since_id = last_id)
                    slep = False
                
                '''
                if not new_tweets:
                    break
                '''
                
                if len(new_tweets) > 1:
                    for tweet in new_tweets:
                        json_tweet = tweet._json

                        id = json_tweet['id_str']
                        text = json_tweet["text"]
                        if id in self.database:
                            print("This ID is already in the database!")
                        else:
                            info = {'id': id, 'tweet': json_tweet}
                            self.database.save(info)
                        total += 1

                    last_id = new_tweets[-1].id_str
                else:
                    json_tweet = tweet[0]._json
                    id = json_tweet['id_str']
                    text = json_tweet["text"]
                    if id in self.database:
                        print("This ID is already in the database!")
                    else:
                        info = {'id': id, 'tweet': json_tweet}
                        self.database.save(info)
                    total += 1

                    last_id = new_tweets[-1].id_str
                
                print("Total is: {}".format(total))



            except tweepy.RateLimitError:
                time.sleep(15*60)
            
            except tweepy.TweepError as e:
                break


if __name__ == '__main__':
    auth = tweepy.OAuthHandler("B1YMqtkC4pUt4jrC0hwCIWM7j", "0gd00U1TkhmU2DVGLvebE8VmefsS5YVsiYT5kWLtXlDKkmiYjy")
    auth.set_access_token("1110906258272313344-8wkeDsdpALCmASt3YcoNj2ZsPAz0DL", "WlGjdg2SjIoPmC6QAk6XQY8AzCXthhsyfqFhr3LMkbyWJ")


    api = tweepy.API(auth)

    admin = "admin"
    password = "admin"
    ip = '127.0.0.1'

    db_name = "test"
    server = couchdb.Server('http://' + admin + ':' + password + '@'+ip+':5984/')
    if db_name in server:
        print("This database is already in the server!")
        db = server[db_name]
    else:
        print("Create database: {}".format(db_name))
        db = server.create(db_name)

    geo = "-37.813628,144.963058,5km"

    searcher = search_tweets(api, db, '*', geo)
    searcher.search()

    
