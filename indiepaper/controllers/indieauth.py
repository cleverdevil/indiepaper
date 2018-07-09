from uuid import uuid4
from urllib.parse import urlencode
from http import cookies

from pecan import expose, redirect, request

from indiepaper import indieauth


class IndieAuthController(object):

    @expose()
    def index(self, me=''):
        if not me:
            return 'Must specify a `me` parameter'

        session = request.environ['beaker.session']
        session['me'] = me
        session['state'] = str(uuid4())
        session.save()

        indieauth.request_authorization(me, session['state'])

    @expose()
    def callback(self, code=None, state=None):
        session = request.environ['beaker.session']
        try:
            assert session['state'] == state
        except AssertionError:
            return 'Error: state mismatch'

        result = indieauth.request_token(session['me'], code)
        if not result:
            return 'Error: no token returned from token endpoint'

        target = 'https://www.indiepaper.io/indieauth.html?success=true'

        c = cookies.SimpleCookie()
        c['indiepaper-me'] = session['me']
        c['indiepaper-me']['domain'] = '.indiepaper.io'
        c['indiepaper-me']['path'] = '/'

        c['indiepaper-token'] = result['token']
        c['indiepaper-token']['domain'] = '.indiepaper.io'
        c['indiepaper-token']['path'] = '/'

        c['indiepaper-endpoint'] = result['micropub']
        c['indiepaper-endpoint']['domain'] = '.indiepaper.io'
        c['indiepaper-endpoint']['path'] = '/'

        headers = [
            ('Set-Cookie', morsel.OutputString())
            for morsel in c.values()
        ]

        redirect(target, headers=headers)
