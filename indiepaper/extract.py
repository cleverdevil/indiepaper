from pecan import conf

import requests
import mf2py


def parse(url):
    result = parse_with_mf2py(url)

    if result:
        return result
    else:
        return parse_with_mercury(url)


def parse_with_mercury(url):
    response = requests.get(
        conf.mercury.endpoint,
        params={'url': url},
        headers={'x-api-key': conf.mercury.api_key}
    )

    if response.status_code != 200:
        return None

    result = response.json()

    mf2 = {
        'type': ['h-entry'],
        'properties': {
            'name': [result['title']],
            'content': [{
                'html': result['content'],
                'value': ''
            }],
            'syndication': [
                result['url']
            ],
            'url': [
                result['url']
            ]
        }
    }

    if result.get('author'):
        mf2['properties']['author'] = [result['author']]
    if result.get('date_published'):
        mf2['properties']['published'] = [result['date_published']]

    return mf2


def parse_with_mf2py(url):
    result = mf2py.parse(url=url)

    if not result:
        return None

    if len(result.get('items', [])) == 0:
        return None

    item = result['items'][0]

    if not item['properties'].get('name'):
        return None

    if not item['properties'].get('content'):
        return None

    mf2 = {
        'type': ['h-entry'],
        'properties': {
            'name': item['properties']['name'],
            'content': item['properties']['content'],
            'syndication': [
                url
            ],
            'url': [
                url
            ]
        }
    }

    if item['properties'].get('author'):
        mf2['properties']['author'] = item['properties']['author']
    if item['properties'].get('published'):
        mf2['properties']['published'] = item['properties']['published']

    return mf2
