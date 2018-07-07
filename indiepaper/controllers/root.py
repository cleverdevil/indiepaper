from pecan import expose, redirect, request, abort, conf
from pecan.hooks import HookController, PecanHook

import requests
import json


from .indieauth import IndieAuthController


class CorsHook(PecanHook):

    def after(self, state):
        state.response.headers['Access-Control-Allow-Origin'] = '*'
        state.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        state.response.headers['Access-Control-Allow-Headers'] = 'origin, authorization, accept, mp-destination'


class RootController(HookController):

    __hooks__ = [CorsHook()]

    indieauth = IndieAuthController()

    @expose(generic=True)
    def index(self):
        redirect('https://www.indiepaper.io/')


    @index.when(method='POST', template='json')
    def index_post(self, url):
        # get the micropub information from the headers
        destination = request.headers.get('mp-destination')
        token = request.headers.get('Authorization')

        if not destination:
            abort(400, detail='No micropub destination specified in "mp-destination" header.')
        elif not token:
            abort(400, detail='No bearer token provided in "Authorization" header.')
        elif not url:
            abort(400, detail='No URL provided as an HTTP POST parameter.')

        # parse URL
        result = self._parse_url(url)

        # transform to MF2
        mf2 = self._transform_to_mf2(result)

        # send micropub request
        self._send_micropub(mf2, destination, token)

        return dict(result='success')


    def _parse_url(self, url):
        response = requests.get(
            conf.mercury.endpoint,
            params={'url': url},
            headers={'x-api-key': conf.mercury.api_key}
        )

        if response.status_code != 200:
            abort(400, detail='Error parsing the specified URL.')

        return response.json()


    def _transform_to_mf2(self, result):
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


    def _send_micropub(self, mf2, destination, token):
        result = requests.post(
            destination,
            json=mf2,
            headers={'Authorization': token}
        )

        if result.status_code not in (200, 201):
            print("-" * 80)
            print(result.status_code)
            print(result.text)
            print("-" * 80)

            abort(400, detail='Failed to publish to specified endpoint.')
