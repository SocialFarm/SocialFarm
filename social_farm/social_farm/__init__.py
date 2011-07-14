from pyramid import request
from pyramid.config import Configurator

from handlers import facebook


def main(global_config, **settings):

    config = Configurator(settings=settings)
    config.include('pyramid_handlers')
    config.add_static_view('static', 'social_farm:static')

    config.add_handler('facebook', '/facebook/{action}/{id}', handler=facebook.FacebookHandler)

    config.scan('social_farm')

    return config.make_wsgi_app()

