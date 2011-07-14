import os
from pyramid.paster import get_app

application = get_app(os.path.join(os.path.dirname(__file__), 'production.ini'), 'social_farm')
