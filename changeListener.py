import time
import thread
import couchdb

import opts
import comms

import defaults


OPTS = defaults.options()
OPTS.update({
     "dbServer": "http://localhost:5984/",
     "dbName": "dbName"
})
OPTS_HELP = defaults.options_help()
OPTS_HELP.update({
     "dbServer": "URL of couchdb server",
     "dbName": "Name of database to watch"
})


class Listener(comms.swarm):

    def __init__(self):
        super(Listener, self).__init__()
        self.options = OPTS

    def couchdbListen(self, options):
        # Set the options
        self.options = options
        # Connect to couchdb
        couch = couchdb.Server(options["dbServer"])
        # Select database
        db = couch[options["dbName"]]
        # Get the last update sequence
        since = db.info()["update_seq"]
        # Listen for changes forever
        while True:
            changes = db.changes(since=since)
            # Update the update sequence
            since = changes["last_seq"]
            # Distribute the importing
            for changeset in changes["results"]:
                self.callDist("couchdbImporter", "couchdbImport", \
                    options["sHost"], options["sPort"], changeset, \
                    waitResponse=False)

def main():
    # Set any options needed
    options = opts.parse(OPTS, OPTS_HELP)
    swarmService = defaults.register(OPTS, OPTS_HELP, \
        Listener, "couchdbListener")
    swarmService.couchdbListen(options)
    # Serve forever
    defaults.serve()

if __name__ == '__main__':
    main()
