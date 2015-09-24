import sys
import json
import time
import uuid
import stratus
import couchdb

import opts

SERVICE_NAME = "couchdbChangeListener"
OPTS = {
     "dbServer": "http://localhost:5984/",
     "sPort": stratus.PORT,
     "dbName": "dbName",
     "sHost": "localhost"
}
OPTS_HELP = {
     "dbServer": "URL of couchdb server",
     "sPort": "Port for stratus server",
     "dbName": "Name of database to watch",
     "sHost": "Ip or hostname of stratus server"
}

class service(stratus.stratus):

    def couchdbListen(self, dbServer=OPTS["dbServer"], \
        dbName=OPTS["dbName"]):
        couch = couchdb.Server(dbServer)

        # select database
        db = couch[dbName]

        since = db.info()["update_seq"]
        while True:
            changes = db.changes(since=since)
            since = changes["last_seq"]
            for changeset in changes["results"]:
                try:
                   doc = db[changeset["id"]]
                except couchdb.http.ResourceNotFound:
                   continue
                else:
                   print(doc)

def main():
    # Set any options needed
    options = opts.parse(OPTS, OPTS_HELP)
    # # Create the listener service
    # to_launch = service()
    # name = SERVICE_NAME + options["dbServer"] + options["dbName"]
    # print(name)
    # # Connect service to cluster
    # to_launch.connect(name=name, host=options["sHost"], \
    #     port=options["sPort"], service=SERVICE_NAME)
    # # Host services
    # while True:
    #     time.sleep(300)

if __name__ == '__main__':
    main()
