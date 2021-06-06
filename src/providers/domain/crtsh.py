from crtsh import crtshAPI
import json

from ..result import Result

BASE_URL = 'https://dnsdumpster.com/'

def query(domain):
    results = []

    full_result = crtshAPI().search(domain,expired=False)

    if len(full_result) == 0:
        results.append(
            Result(
                message='No results found.'
            )
        )

    else:
        for res in full_result:
            results.append(
                Result(
                    message="Found certificate info.",
                    json_result={
                        'common_name': res['common_name'],
                        'valid_from': res['not_before']
                    }
                )
            )

    return results
