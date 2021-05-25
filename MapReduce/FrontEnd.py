import couchdb
import json
import sys
import requests
import argparse

#This file is connecting the backend and frontend


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", help = "Enter the name of the design document!", required = True)
    parser.add_argument("-s", "--server", help = "Enter the ip address of your Couchdb Server! Please INCLUDE USERNAME:PASSWORD and end with '/'!!!", required = True)
    parser.add_argument("-d", "--database", help = "Enter your Database's name!", required = True)
    args = parser.parse_args()

    view_name = str(args.name)
    ip = str(args.server)
    db_name = str(args.database)

    server = couchdb.Server(ip)
    db = server[db_name]

    try:
        total = json.loads(requests.get(ip + db_name + "/_design/" + view_name + "/_view/count").text)["rows"][0]['value']
        result = json.loads(requests.get(ip + db_name + "/_design/" + view_name + "/_view/point_without_zero").text)["rows"]
        points = 0
        pos_count = 0
        ngtv_count = 0

        for i in range(0, len(result)):
            points += float(result[i]['value'])
            if float(result[i]['value']) > 0:
                pos_count += 1
            elif float(result[i]['value']) < 0:
                ngtv_count += 1
        
        pos_percent = pos_count / total
        nega_percent = ngtv_count / total

        print(total)
        print(pos_percent)
        print(nega_percent)

    except Exception as e:
        print("Error Here")
        sys.exit(1)