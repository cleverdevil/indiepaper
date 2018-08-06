from urllib.parse import urlparse, urlencode, parse_qs

from bs4 import BeautifulSoup, SoupStrainer
from pecan import redirect

import requests


def discover_endpoints(me):
    response = requests.get(me)

    all_links = BeautifulSoup(
        response.content,
        'html.parser',
        parse_only=SoupStrainer(name='link')
    ).find_all('link')

    result = {}

    for link in all_links:
        rel = link.get('rel', [None])[0]

        if rel in ('authorization_endpoint', 'token_endpoint', 'redirect_uri', 'micropub'):
            href = link.get('href', None)
            if href:
                url = urlparse(href)
                if url.scheme in ('http', 'https'):
                    result.setdefault(rel, set()).add(url)

    return result


def request_authorization(me, state):
    endpoints = discover_endpoints(me)

    if len(endpoints.get('authorization_endpoint', [])) == 0:
        raise Exception('No authorization endpoint discovered.')

    auth_endpoint = endpoints['authorization_endpoint'].pop().geturl()

    ns = {
        'me': me,
        'redirect_uri': 'https://indiepaper.io/indieauth/callback',
        'client_id': 'https://indiepaper.io',
        'state': state,
        'scope': 'save create update',
        'response_type': 'code'
    }
    auth_target = auth_endpoint + '?' + urlencode(ns)
    redirect(auth_target)


def request_token(me, code):
    endpoints = discover_endpoints(me)

    if len(endpoints.get('token_endpoint', [])) == 0:
        raise Exception('No token endpoint discovered.')

    if len(endpoints.get('micropub', [])) == 0:
        raise Exception('No micropub endpoint discovered.')

    token_endpoint = endpoints['token_endpoint'].pop().geturl()
    micropub_endpoint = endpoints['micropub'].pop().geturl()

    response = requests.post(token_endpoint, data={
        'grant_type': 'authorization_code',
        'me': me,
        'code': code,
        'redirect_uri': 'https://indiepaper.io/indieauth/callback',
        'client_id': 'https://indiepaper.io'
    })

    if response.status_code != 200:
        raise Exception(
            'Error returned from token endpoint: ' + str(response.status_code)
        )

    try:
        data = response.json()
        return {
            'token': data.get('access_token'),
            'micropub': micropub_endpoint
        }
    except:
        return {
            'token': parse_qs(response.text).get('access_token', [None])[0],
            'micropub': micropub_endpoint
        }
