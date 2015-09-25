import copy
import time
import thread
import couchdb

import opts
import comms

DEFAULT_OPTS = {
     "sHost": "localhost",
     "sPort": comms.PORT,
     "sPass": "somepass",
     "sStart": 0,
     "sPublic": "public.pem",
     "sPrivate": "private.pem"
}
DEFAULT_OPTS_HELP = {
     "sHost": "Ip or hostname of swarm server",
     "sPort": "Port for swarm server",
     "sPass": "Password for the swarm server",
     "sStart": "Start as the swarm master",
     "sPublic": "Public key file to encrypt with",
     "sPrivate": "Private key file to decrypt with"
}

def options():
    return copy.deepcopy(DEFAULT_OPTS)

def options_help():
    return copy.deepcopy(DEFAULT_OPTS_HELP)

def register(default_opts, default_opts_help, ServiceClass, serviceName):
    """
    Basic repeated setup for swarmService in swarm
    """
    # Set any options needed
    options = opts.parse(default_opts, default_opts_help)
    swarmService = ServiceClass()
    swarmService.password = options["sPass"]
    swarmService.keys(options["sPublic"], options["sPrivate"])
    # Start the server
    if options["sStart"]:
        thread.start_new_thread(swarmService.start, ())
        # Give it time to start the swarm server so we can register
        # This is a problem because theres only one server in this case
        time.sleep(0.1)
    swarmService.registerWith(serviceName, password=options["sPass"], \
        host=options["sHost"], port=options["sPort"])
    return swarmService

def serve():
    """
    Serve indefinatly
    """
    while True:
        time.sleep(300)
