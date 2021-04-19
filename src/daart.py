import json
import os
import socket
import sys
import validators

import providers.address
import providers.domain

from pprint import pprint
LOGFORMAT='visual'


class IP:
    pass

class Domain:
    pass

def usage(name):
    print('{} <valid IPv4 address>'.format(name))
    sys.exit(2)

def logResult(provider, result):

    moreinfo = result.get('moreinfo')
    result_txt = result['result']
        
    if LOGFORMAT == 'visual':
        if moreinfo:
            result_txt = result_txt + ' See {} for more info.'.format(moreinfo)

        if isinstance(result_txt, list):
            for res in result_txt:
                print('{}: {}'.format(
                        provider,
                        result_txt
                    )
                )
        else:
            print('{}: {}'.format(
                    provider,
                    result_txt
                )
            )
    elif LOGFORMAT == 'json':
        json_result = {
            'provider': provider,
            'result': result_txt,
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
        print("* Running IP address '{}' through {} address providers.".format(
            address,
            len(addr_providers))
        )
    else:
        return

    for provider,module in addr_providers.items():
        print("-- {} --".format(provider))
        for result in module.query(address):
            logResult(provider,result)
        print('--')

    print('* End address providers.')

def runDomainProviders(domain):
    domain_providers = import_providers(providers.domain)

    if len(domain_providers) > 0:
        print("* Running domain '{}' through {} domain providers.".format(
            domain,
            len(domain_providers))
        )
    else:
        return

    for provider,module in domain_providers.items():
        print("-- {} --".format(provider))
        for result in module.query(domain):
            logResult(provider,result)
        print('--')

    print('* End domain providers.')

if __name__ == "__main__":

#    try:
        if paramType(sys.argv[1]) is IP:
            runAddressProviders(sys.argv[1])
            domain = reverseLookup(sys.argv[1])
            if domain and paramType(domain) is Domain:
                print("IP successfully resolved to {}.".format(domain))
                runDomainProviders(domain)
            else:
                print("IP could not be resolved to a domain.")

        elif paramType(sys.argv[1]) is Domain:
            runDomainProviders(sys.argv[1])
            ip = dnsLookup(sys.argv[1])
            if ip and paramType(ip) is IP:
                print("Domain successfully resolved to {}.".format(ip))
                runAddressProviders(ip)
            else:
                print("Domain could not be resolved to an IP.")

#    except Exception as e:
#        print(e)
#        usage(sys.argv[0])
