from pecan import make_app, conf
from beaker.middleware import SessionMiddleware


def setup_app(config):

    app_conf = dict(config.app)

    app = make_app(
        app_conf.pop('root'),
        logging=getattr(config, 'logging', {}),
        **app_conf
    )

    app = SessionMiddleware(app, conf.beaker)

    return app
