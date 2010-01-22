import httplib, urllib
import time
import sys
#from django.contrib.sites.models import Site


def log(message):
    print "[%s] %s" % (time.strftime("%I:%M:%S %p"), message)


def invoke(domain="localhost:8000", task="/fetch_messages", verbose=False):
    """Invokes a periodic service, using an HTTP call"""
    try:
        params_map = {}
        params = urllib.urlencode(params_map)
        headers = {"Content-type": "text/plain", "Accept": "text/html"}
        #site = Site.objects.get(id=1)
        #domain = site.domain
        log("Invoking %s%s..." % (domain, task))
        conn = httplib.HTTPConnection(domain)
        conn.request("GET", task, params, headers)
        response = conn.getresponse()
        if response.status == 200:
            log("Processing completed successfully.")
        else:
            log("Error in processing (HTTP status code %d)" % response.status)
        data = response.read()
        if verbose:
            print data
        conn.close()
    except:
        log("Failed to invoke %s%s" % (domain, task))
        for ei in sys.exc_info():
            log(ei)


if __name__ == "__main__":
    # todo read options from command-line (e.g., domain, interval & verbose)
    log("Periodic invoker started")
    args = {}
    if len(sys.argv) > 1:
        args["domain"] = sys.argv[1]
    if len(sys.argv) > 2:
        args["verbose"] = (sys.argv[2] == "--v")
    while (True):
        if "domain" in args and "verbose" in args:
            invoke(domain=args["domain"], verbose=args["verbose"])
        elif "domain" in args:
            invoke(domain=args["domain"])
        elif "verbose" in args:
            invoke(verbose=args["verbose"])
        else:
            invoke()
        time.sleep(70)