import couchdb

couch = couchdb.Server()

# select database
db = couch['testdb']

since = 0
while True:
    changes = db.changes(since=since)
    since = changes["last_seq"]
    for changeset in changes["results"]:
        try:
           doc = db[changeset["id"]]
        except couchdb.http.ResourceNotFound:
           continue
        else:
           print doc
