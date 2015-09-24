import stratus

import opts

OPTS = {
    "host": "localhost",
    "port": stratus.PORT,
    "service": "couchdbChangeListener"
}
OPTS_HELP = {
     "host": "Ip or hostname of stratus server",
     "port": "Port for stratus server",
     "service": "Service to list"
}

def byService(connected, serviceName):
    """
    Given the connected nodes this will list the ones that are of the
    specified service
    """
    for node in connected:
        if "service" in connected[node] and \
            connected[node]["service"] == serviceName:
            print(node)

def main():
    """
    Lists connected nodes in a service
    """
    # Set any options needed
    options = opts.parse(OPTS, OPTS_HELP)
    # Create a client and connect to stratus server
    client = stratus.client()
    client.connect(**options)
    # Get the connected clients
    connected = client.connected()
    # List the services reqested
    byService(connected, options["service"])

if __name__ == '__main__':
    main()
