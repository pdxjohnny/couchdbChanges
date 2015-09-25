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
     "dbServer": "URL of postgress server",
     "dbName": "Name of database to input to"
})


class Importer(comms.swarm):

    def __init__(self):
        super(Importer, self).__init__()
        self.options = OPTS

    def couchdbImport(self, data, addr):
        print data

def main():
    # Set any options needed
    options = opts.parse(OPTS, OPTS_HELP)
    swarmService = defaults.register(OPTS, OPTS_HELP, \
        Importer, "couchdbImporter")
    # Serve forever
    defaults.serve()

if __name__ == '__main__':
    main()
