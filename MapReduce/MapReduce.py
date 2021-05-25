import couchdb
import json
import sys
import requests
import argparse
import pandas as pd

#Here are the steps to build the mapreduce algorithms!
#First build views and then send requests to find out the required items.
#The reason of containing point_with_zero and point_without_zero is preparing for data analysis.
#WE want to create two different models to test the number of zeros is important or not.
#Also we find that most of the tweets with 0 point are non-English, because TextBlob could only
#process English based text. However, there could be some Englished tweets get 0 point. So EMOTIONLESS!

#https://docs.couchdb.org/en/latest/ddocs/views/intro.html



#Create the map functions first and allocate them into the view
def build_view(db, view_name):

    #Count the total number of the tweets in the database
    count_total = '''function(doc) {
        if(doc.tweet){
            emit(doc._id, 1)
        }
    }'''

    #Count the total number of tweets which the emotion points do not equal to 0
    point_without_zero = '''function(doc) {
        if(doc.points){
            emit(doc._id, doc.points)
        }
    }'''

    #Count the total number of tweets which the emotion points include 0
    point_with_zero = '''function(doc) {
        emit(doc._id, doc.points)
    }'''

    #Emit the pure text of each tweet
    text = '''function(doc) {
        emit(doc._id, doc.tweet)
    }'''

    #Emit the timestamp of posting the tweet
    time = '''function(doc) {
        emit(doc._id, doc.time)
    }'''

    #Emit the language of the tweet
    language = '''function(doc) {
        emit(doc._id, doc.language)
    }'''

    #Emit the total number of follower of the tweet's poster
    followers = '''function(doc) {
        emit(doc._id, doc.all.user.followers_count)
    }'''

    #Emit the total number of friends of the tweet's poster
    friends = '''function(doc) {
        emit(doc._id, doc.all.user.friends_count)
    }'''

    #Starting to build the view
    view = {"_id": "_design/"+view_name, 
    "views": {

        #Total number view
        "count": {
            "reduce": "_count",
            "map": count_total
            },
        
        #No zero view
        "point_without_zero": {
            "map": point_without_zero
            },
        
        #Contain 0 view
        "point_with_zero": {
            "map": point_with_zero
            },
        
        #Pure text view
        "text": {
            "map": text
            },
        
        #Timestamp view
        "time": {
            "map": time
            },
        
        #Language view
        "language": {
            "map": language
            },

        #Followers view
        "followers" : {
            "map": followers
            },
        
        #Friends view
        "friends": {
            "map": friends
            }
        },
    "language": "javascript"
    }
    db.save(view)
    

if __name__ == "__main__":

    #Here are the required import 
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", help = "Enter the name of the design document!", required = True)
    parser.add_argument("-s", "--server", help = "Enter the ip address of your Couchdb Server! Please INCLUDE USERNAME:PASSWORD and end with '/'!!!", required = True)
    parser.add_argument("-p", "--purpose", help = "Enter your purpose! Please select from the provided list", 
                        choices=['count', 'point_without_zero', 'point_with_zero', 'text', 'time', 'language', 'followers', 'friends','build'], required = True)
    parser.add_argument("-d", "--database", help = "Enter your Database's name!", required = True)
    args = parser.parse_args()

    view_name = str(args.name) #View name of the design document
    purpose = str(args.purpose) #purpose of using mapreduce
    db_name = str(args.database) #database name
    ip = str(args.server) #ip address of the database
    server = couchdb.Server(ip)
    db = server[db_name]
    try:
        build_view(db, view_name)
        print("Successfully Create View!\n")

        if purpose == "count":
            
            #Send request to the server and get the value of the total number
            result = json.loads(requests.get(ip + db_name + "/_design/" + view_name + "/_view/count").text)["rows"][0]['value']
            print(result)

        elif purpose == "point_without_zero":
            points = 0
            pos_count = 0
            ngtv_count = 0

            
            #Send request to the server and get the value of the points without 0
            result = json.loads(requests.get(ip + db_name + "/_design/" + view_name + "/_view/" + purpose).text)["rows"]

            #Calculate the total points and count the number of positive and negative tweets.
            for i in range(0, len(result)):
                points += float(result[i]['value'])
                if float(result[i]['value']) > 0:
                    pos_count += 1
                elif float(result[i]['value']) < 0:
                    ngtv_count += 1

            print("The total points are: " + str(points))
            print("The total number of positive tweet is: " + str(pos_count))
            print("The total number of negative tweet is: " + str(ngtv_count))

            #Create a dataframe and output the data as csv file in order to do the further analysis.
            #The output is allocate to the direction where you run this program.
            point_no_zero = pd.DataFrame(result)
            point_no_zero.to_csv("point_no_zero.csv")
        
        elif purpose == "point_with_zero":
            points = 0
            pos_count = 0
            ngtv_count = 0
            zero_count = 0

            #Send request to the server and get the value of the points include 0
            result = json.loads(requests.get(ip + db_name + "/_design/" + view_name + "/_view/" + purpose).text)["rows"]

            #Calculate the total points and count the number of positive, negative, zero point tweets.
            for i in range(0, len(result)):
                points += float(result[i]['value'])
                if float(result[i]['value']) > 0:
                    pos_count += 1
                elif float(result[i]['value']) < 0:
                    ngtv_count += 1
                elif float(result[i]['value']) == 0:
                    zero_count += 1

            print("The total points are: " + str(points))
            print("The total number of positive tweet is: " + str(pos_count))
            print("The total number of negative tweet is: " + str(ngtv_count))
            print("The total number of zero is: " + str(zero_count))

            #Create a dataframe and output the data as csv file in order to do the further analysis.
            #The output is allocate to the direction where you run this program.
            point_have_zero = pd.DataFrame(result)
            point_have_zero.to_csv("point_have_zero.csv")
        
        elif purpose == "text":
            text_list = []

            #Send request to the server and get the tweets' text
            result = json.loads(requests.get(ip + db_name + "/_design/" + view_name + "/_view/" + purpose).text)["rows"]
            
            #Extract the text and store in the list
            for i in range(0, len(result)):
                text_list.append(result[i]['value'])
            
            print(text_list)
        
        elif purpose == "time":
            output = {}

            result = json.loads(requests.get(ip + db_name + "/_design/" + view_name + "/_view/" + purpose).text)["rows"]
            
            #Extract the timestamp and store them as dictionary
            for i in range(0, len(result)):
                output[result[i]['key']] = result[i]['value']

            print(output)
        
        elif purpose == "language":
            language_dict = {}

            result = json.loads(requests.get(ip + db_name + "/_design/" + view_name + "/_view/" + purpose).text)["rows"]
            
            #Extract the language and store them as dictionary
            for i in range(0, len(result)):
                language_dict[result[i]['key']] = result[i]['value']
            
            print(language_dict)
        
        elif purpose == "followers":
            follower_dict = {}
            
            result = json.loads(requests.get(ip + db_name + "/_design/" + view_name + "/_view/" + purpose).text)["rows"]

            #Extract the number of followers and store this number in the dictionary
            for i in range(0, len(result)):
                follower_dict[result[i]['key']] = result[i]['value']
            
            print(follower_dict)
        
        elif purpose == "friends":
            friend_dict = {}

            #Extract the number of friends and store this number in the dictionary
            result = json.loads(requests.get(ip + db_name + "/_design/" + view_name + "/_view/" + purpose).text)["rows"]

            for i in range(0, len(result)):
                friend_dict[result[i]['key']] = result[i]['value']
            
            print(friend_dict)
        
        elif purpose == "build":
            print("OK, just build the view")

        #If there is no views could be used
        else:
            print("The view do not contain the purpose you want to achieve!")
            print("Please check the design document and create a new view!")



    #If the design document is already created in the database, the exception will occure
    except couchdb.http.ResourceConflict:
        print("Conflict Happened!")
        print("This design document name is already in the database!\n")

        #Repeat the steps in the above
        try:
            if purpose == "count":
                result = json.loads(requests.get(ip + db_name + "/_design/" + view_name + "/_view/" + purpose).text)["rows"][0]['value']
                print(result)

            elif purpose == "point_without_zero":
                points = 0
                pos_count = 0
                ngtv_count = 0
                zero_count = 0

                result = json.loads(requests.get(ip + db_name + "/_design/" + view_name + "/_view/" + purpose).text)["rows"]
                
                for i in range(0, len(result)):
                    points += float(result[i]['value'])
                    if float(result[i]['value']) > 0:
                        pos_count += 1
                    elif float(result[i]['value']) < 0:
                        ngtv_count += 1

                print("The total points are: " + str(points))
                print("The total number of positive tweet is: " + str(pos_count))
                print("The total number of negative tweet is: " + str(ngtv_count))

                point_no_zero = pd.DataFrame(result)
                point_no_zero.to_csv("point_no_zero.csv")
        
            elif purpose == "point_with_zero":
                points = 0
                pos_count = 0
                ngtv_count = 0
                zero_count = 0
                
                
                result = json.loads(requests.get(ip + db_name + "/_design/" + view_name + "/_view/" + purpose).text)["rows"]
        
                

                for i in range(0, len(result)):
                    points += float(result[i]['value'])
                    if float(result[i]['value']) > 0:
                        pos_count += 1
                    elif float(result[i]['value']) < 0:
                        ngtv_count += 1
                    elif float(result[i]['value']) == 0:
                        zero_count += 1

                print("The total points are: " + str(points))
                print("The total number of positive tweet is: " + str(pos_count))
                print("The total number of negative tweet is: " + str(ngtv_count))
                print("The total number of zero is: " + str(zero_count))

                point_have_zero = pd.DataFrame(result)
                point_have_zero.to_csv("point_have_zero.csv")

            elif purpose == "text":
                text_list = []

                result = json.loads(requests.get(ip + db_name + "/_design/" + view_name + "/_view/" + purpose).text)["rows"]
            
                for i in range(0, len(result)):
                    text_list.append(result[i]['value'])
            
                print(text_list)

            elif purpose == "time":
                output = {}

                result = json.loads(requests.get(ip + db_name + "/_design/" + view_name + "/_view/" + purpose).text)["rows"]

                for i in range(0, len(result)):
                    output[result[i]['key']] = result[i]['value']

                print(output)
        
            elif purpose == "language":
                language_dict = {}

                result = json.loads(requests.get(ip + db_name + "/_design/" + view_name + "/_view/" + purpose).text)["rows"]

                for i in range(0, len(result)):
                    language_dict[result[i]['key']] = result[i]['value']
            
                print(language_dict)
        
            elif purpose == "followers":
                follower_dict = {}
            
                result = json.loads(requests.get(ip + db_name + "/_design/" + view_name + "/_view/" + purpose).text)["rows"]

                for i in range(0, len(result)):
                    follower_dict[result[i]['key']] = result[i]['value']
            
                print(follower_dict)
        
            elif purpose == "friends":
                friend_dict = {}

                result = json.loads(requests.get(ip + db_name + "/_design/" + view_name + "/_view/" + purpose).text)["rows"]

                for i in range(0, len(result)):
                    friend_dict[result[i]['key']] = result[i]['value']
            
                print(friend_dict)
            
            elif purpose == "build":
                print("Already built!")
            
            else:
                print("The view do not contain the purpose you want to achieve!")
                print("Please check the design document and create a new view!")
        
        except Exception as e:
            sys.exit(1)