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
     "dbName": "dbName",
     "sHost": "localhost",
     "sPort": stratus.PORT
}
OPTS_HELP = {
     "dbServer": "URL of couchdb server",
     "dbName": "Name of database to watch",
     "sHost": "Ip or hostname of stratus server",
     "sPort": "Port for stratus server"
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
                print(changeset["id"])

def main():
    # Set any options needed
    options = opts.parse(OPTS, OPTS_HELP)
    # Create the listener service
    to_launch = service()
    name = options["dbServer"] + options["dbName"]
    # Connect service to cluster, so we know it is listening
    to_launch.connect(name=name, host=options["sHost"], \
        port=options["sPort"], service=SERVICE_NAME)
    # Listen
    to_launch.couchdbListen(dbServer=options["dbServer"], \
        dbName=options["dbName"])

if __name__ == '__main__':
    main()
