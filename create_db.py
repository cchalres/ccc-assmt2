import couchdb

admin = "admin"
password = "admin"
ip = '127.0.0.1'

db_name = 'test2'
server = couchdb.Server('http://' + admin + ':' + password + '@'+ip+':5984/')
if db_name in server:
    print("This database is already in the server!")
    db = server[db_name]
    print(type(db))
else:
    print("Create database: {}".format(db_name))
    db = server.create(db_name)
    print(type(db))
