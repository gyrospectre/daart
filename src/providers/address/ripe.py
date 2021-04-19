import json
import requests
from pprint import pprint

BASE_URL = 'https://rest.db.ripe.net/{}'
SOURCES = [
    'RIPE', 'AFRINIC-GRS', 'APNIC-GRS', 'ARIN-GRS', 'JPIRR-GRS', 'LACNIC-GRS', 'RADB-GRS'
]
USEFUL = {
    'inetnum': [
        'inetnum', 'netname', 'descr', 'country', 'last-modified'        
    ],
    'organisation': [
        'org-name', 'country', 'address', 'phone', 'e-mail'
    ]
}

def query(ip):
    url = BASE_URL.format('search')

    for source in SOURCES:
        print(source)
        params = {
            'source': source,
            'query-string': str(ip)
        }

        headers = {
            'Accept': 'application/json'
        }
        results = []

        r = requests.get(url, headers=headers, params=params)

        if r.status_code == 200:
            res = json.loads(r.text)
            for obj in res['objects']['object']:
                if 'inetnum' in obj['link']['href']:
                    moreinfo = obj['link']['href']

                for attr in obj['attributes']['attribute']:
                    if attr.get('name'):
                        if (attr['name'] == 'netname' and attr['value'] == 'NON-RIPE-NCC-MANAGED-ADDRESS-BLOCK'):
                            break
                        if USEFUL.get(obj['type']) and attr['name'] in USEFUL[obj['type']]:                        
                            print(attr)

    return results
