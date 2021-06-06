import json
import os
import socket
import sys
import validators

import providers.address
import providers.domain

from providers.result import Result

from pprint import pprint

LOGFORMAT='visual'

class COLOUR:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class IP:
    pass

class Domain:
    pass

def usage(name):
    print('{} <valid IPv4 address>'.format(name))
    sys.exit(2)

def logResult(provider, results):

    if LOGFORMAT == 'visual':
        for result in results:
            print('{}{}: {}{} {}'.format(
                    COLOUR.CYAN,
                    provider,
                    COLOUR.YELLOW,
                    result.message,
                    COLOUR.ENDC
                )
            )
            if result.json_result:
                pprint(result.json_result)

            if result.moreinfo:
                print('{}See {} for more info.{}'.format(
                        COLOUR.YELLOW,
                        result.moreinfo,
                        COLOUR.ENDC
                    )
                )


    elif LOGFORMAT == 'json':
        json_result = {
            'provider': provider,
            'result': result['result'],
            'link': moreinfo
        }
        print(json.dumps(json_result))

def paramType(value):
    if validators.ip_address.ipv4(value):
        return IP
    elif validators.domain(value):
        return Domain

def reverseLookup(address):
    try:
        return socket.gethostbyaddr(address)[0]

    except:
        return None

def dnsLookup(domain):
    try:
        return socket.gethostbyname(domain)

    except:
        return None

def provider_names(package):
    # Just python modules that don't start with '__'
    folder = os.path.split(package.__file__)[0]

    for name in os.listdir(folder):
        if name.endswith(".py") and not name.startswith("__"):
            yield name[:-3]

def import_providers(package):
    names = list(provider_names(package))

    m = __import__(package.__name__, fromlist=names)
    return dict((name, getattr(m, name)) for name in names)

def runAddressProviders(address):
    addr_providers = import_providers(providers.address)
    if len(addr_providers) > 0:
        print("{}Running IP address {}'{}'{} through {} address providers.{}".format(
            COLOUR.GREEN,
            COLOUR.BOLD,
            address,
            COLOUR.ENDC+COLOUR.GREEN,
            len(addr_providers),
            COLOUR.ENDC
        ))
    else:
        return

    for provider,module in addr_providers.items():
        logResult(provider,module.query(address))

def runDomainProviders(domain):
    domain_providers = import_providers(providers.domain)

    if len(domain_providers) > 0:
        print("{}Running domain {}'{}'{} through {} domain providers.{}".format(
            COLOUR.GREEN,
            COLOUR.BOLD,
            domain,
            COLOUR.ENDC+COLOUR.GREEN,
            len(domain_providers),
            COLOUR.ENDC
        ))
    else:
        return

    for provider,module in domain_providers.items():
        logResult(provider,module.query(domain))

if __name__ == "__main__":

#    try:
        if paramType(sys.argv[1]) is IP:
            runAddressProviders(sys.argv[1])
            domain = reverseLookup(sys.argv[1])
            if domain and paramType(domain) is Domain:
                print(COLOUR.BLUE+"\nIP successfully resolved to {}.".format(domain))
                runDomainProviders(domain)
            else:
                print("\nIP could not be resolved to a domain.")

        elif paramType(sys.argv[1]) is Domain:
            runDomainProviders(sys.argv[1])
            ip = dnsLookup(sys.argv[1])
            if ip and paramType(ip) is IP:
                print("\nDomain successfully resolved to {}.".format(ip))
                runAddressProviders(ip)
            else:
                print("\nDomain could not be resolved to an IP.")

#    except Exception as e:
#        print(e)
#        usage(sys.argv[0])
