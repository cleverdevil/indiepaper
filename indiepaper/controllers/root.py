from pecan import expose, redirect, request, abort, conf
from pecan.hooks import HookController, PecanHook

import requests


from indiepaper.extract import parse
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
        if request.method == 'GET':
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
        mf2 = parse(url)

        # send micropub request
        if mf2:
            self._send_micropub(mf2, destination, token)
        else:
            return dict(result='failure')

        return dict(result='success')


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
