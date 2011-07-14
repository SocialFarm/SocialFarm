from pyramid.security import authenticated_userid
from pyramid.httpexceptions import HTTPForbidden



class BaseHandler(object):
    def __init__(self, request):
        self.request = request
        self.c = self.request.tmpl_context 
        self.template_vars = {'title':'base title'}

    def forbidden(self):
        return HTTPForbidden("Forbidden")
  
