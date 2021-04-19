from crtsh import crtshAPI
import json

BASE_URL = 'https://dnsdumpster.com/'

def query(domain):
    results = []

    full_result = crtshAPI().search(domain,expired=False)

    if len(full_result) == 0:
        results.append(
            {
                'result': 'No results found.',
            }
        )
    else:
        for res in full_result:
            results.append(
                {
                    'result': 'Cert found for {}, valid from {}.'.format(
                        res['common_name'],
                        res['not_before']
                    )
                }
            )

    return results
