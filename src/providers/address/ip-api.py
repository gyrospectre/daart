import json
import requests
from ..result import Result

BASE_URL = 'http://ip-api.com/json/{}'
IGNORE_KEYS = ['status', 'countryCode', 'region', 'query', 'zip']

def query(ip):
    url = BASE_URL.format(ip)

    results = []

    r = requests.get(url)

    if r.status_code == 200:
        result = {}
        moreinfo = None

        res = json.loads(r.text)
        if res['status'] == 'success':
            for k in IGNORE_KEYS:
                res.pop(k, None)

        results.append(
            Result(
                message='Found geo-location information.',
                json_result=res,
                moreinfo=moreinfo
            )
        )

    else:
        results.append(
            Result(
                message='Could not find geo-location info.'
            )
        )

    return results
