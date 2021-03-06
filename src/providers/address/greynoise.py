import json
import requests

from ..result import Result

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
            Result(
                message='No results found.'
            )
        )

    else:
        full_result = json.loads(r.text)

        if full_result['noise']:
            results.append(
                Result(
                    message='Classified as noise, last seen {}.'.format(
                        full_result['last_seen']
                    ),
                    moreinfo=full_result['link']
                )
            )

        else:
            results.append(
                Result(
                    message='Not classified as noise.'
                )
            )

        if full_result['riot']:
            results.append(
                Result(
                    message="Found in RIOT DB as '{}', unlikely to be malicious.".format(
                        full_result['name']
                    ),
                    moreinfo=full_result['link']
                )
            )

        else:
            results.append(
                Result(
                    message='Not found in RIOT DB.'
                )
            )

    return results
