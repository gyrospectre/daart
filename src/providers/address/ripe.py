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

    results = []

    for source in SOURCES:
        params = {
            'source': source,
            'query-string': str(ip)
        }

        headers = {
            'Accept': 'application/json'
        }

        r = requests.get(url, headers=headers, params=params)

        if r.status_code == 200:
            result = {}
            moreinfo = None

            res = json.loads(r.text)
            for obj in res['objects']['object']:
                if 'inetnum' in obj['link']['href']:
                    moreinfo = obj['link']['href']

                for attr in obj['attributes']['attribute']:
                    if attr.get('name'):
                        if USEFUL.get(obj['type']) and attr['name'] in USEFUL[obj['type']]:                        
                            result[attr['name']] = attr['value']

            if result.get('netname') != 'NON-RIPE-NCC-MANAGED-ADDRESS-BLOCK' and len(result)>0:
                results.append(
                    {
                        'result': "Found in RIR {}: {}".format(
                            source,
                            json.dumps(result)
                        ),
                        'moreinfo': moreinfo
                    }
                )

    if len(results) == 0:
            results.append(
                {
                    'result': 'Not found in any RIR database.'
                }
            )

    return results
