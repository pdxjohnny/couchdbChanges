import opts
import comms

PADDING = 4
OPTS = {
     "host": "localhost",
     "port": comms.PORT
}
OPTS_HELP = {
     "host": "Hostname or IP of master swarm server",
     "port": "Port of master swarm server"
}

def countServices(services):
    longest = 0
    for serviceType in services:
        if len(serviceType) > longest:
            longest = len(serviceType)
    for serviceType in services:
        padding = " " * (longest - len(serviceType) + PADDING)
        print "{0}:{1}{2}".format(serviceType, padding, \
            len(services[serviceType]))

def main():
    options = opts.parse(OPTS, OPTS_HELP)
    client = comms.service()
    client.keys("private.pem", "private.pem")
    services, error = client.call("nodeList", \
        options["host"], options["port"], {})
    if not error:
        countServices(services)
    else:
        raise comms.error(services, error)

if __name__ == '__main__':
    main()
