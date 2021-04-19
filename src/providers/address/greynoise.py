import json
import requests

BASE_URL = 'https://api.greynoise.io/v3/community/{}'

def query(ip):
    url = BASE_URL.format(str(ip))

    headers = {
        'Accept': 'application/json'
    }
    results = []

    r = requests.get(url, headers=headers)
    if r.status_code == 404:
        results.append(
            {
                'result': 'No results found.',
            }
        )
 
    else:
        full_result = json.loads(r.text)

        if full_result['noise']:
            results.append(
                {
                    'result': 'Classified as noise, last seen {}.'.format(
                        full_result['last_seen']
                    ),
                    'moreinfo': full_result['link']
                }
            )

        else:
            results.append(
                {
                    'result': 'Not classified as noise.'    
                }
            )

        if full_result['riot']:
            results.append(
                {
                    'result': "Found in RIOT DB as '{}', unlikely to be malicious.".format(
                        full_result['name']
                    ),
                    'moreinfo': full_result['link']
                }
            )
        else:
            results.append(
                {
                    'result': 'Not found in RIOT DB'
                }
            )

    return results
