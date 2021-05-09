import couchdb
import json
import sys
import requests
import argparse

def build_count_view(db, view_name, purpose):
    map_fun = '''function(doc) {
        if(doc.tweet){
            emit(doc.tweet, 1)
        }
    }'''
    view = {"_id": "_design/"+view_name, 
    "views": {
        purpose: {
            "reduce": "_" + purpose,
            "map": map_fun
            }
        },
    "language": "javascript"
    }
    db.save(view)


def build_coord_view(db, view_name, purpose):
    map_fun = '''function(doc) {
        if(doc.points){
            emit(doc._id, doc.points)
        }
    }'''

    view = {"_id": "_design/"+view_name, 
    "views": {
        purpose: {
            "map": map_fun
            }
        },
    "language": "javascript"
    }
    db.save(view)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", help = "输入视图的名称", required = True)
    parser.add_argument("-p", "--purpose", help = "输入你的目的，选项有'count', 'point'", required = True)
    parser.add_argument("-d", "--database", help = "输入你的目标数据库，选项有'melb_tweet'", required = True)
    args = parser.parse_args()

    view_name = str(args.name)
    purpose = str(args.purpose)
    db_name = str(args.database)
    server = couchdb.Server("http://admin:admin@127.0.0.1:5984/")
    db = server[db_name]
    if purpose == "count":
        try:
            build_count_view(db, view_name, purpose)

            ip = "http://admin:admin@127.0.0.1:5984/"
            result = json.loads(requests.get(ip + db_name + "/_design/" + view_name + "/_view/" + purpose).text)["rows"][0]['value']
            print(result)
        except couchdb.http.ResourceConflict:
            ip = "http://admin:admin@127.0.0.1:5984/"
            result = json.loads(requests.get(ip + db_name + "/_design/" + view_name + "/_view/" + purpose).text)["rows"][0]['value']
            print(result)

    elif purpose == "point":
        points = 0
        pos_count = 0
        ngtv_count = 0
        try:
            build_coord_view(db, view_name, purpose)
            
            ip = "http://admin:admin@127.0.0.1:5984/"
            result = json.loads(requests.get(ip + db_name + "/_design/" + view_name + "/_view/" + purpose).text)["rows"]
            for i in range(0, 10):
                points += float(result[i]['value'])
                if float(result[i]['value']) > 0:
                    pos_count += 1
                elif float(result[i]['value']) < 0:
                    ngtv_count += 1
            print(points)
            print(pos_count)
            print(ngtv_count)


        except couchdb.http.ResourceConflict:
            ip = "http://admin:admin@127.0.0.1:5984/"
            result = json.loads(requests.get(ip + db_name + "/_design/" + view_name + "/_view/" + purpose).text)["rows"]
            for i in range(0, 10):
                points += float(result[i]['value'])
                if float(result[i]['value']) > 0:
                    pos_count += 1
                elif float(result[i]['value']) < 0:
                    ngtv_count += 1
            print(points)
            print(pos_count)
            print(ngtv_count)
                