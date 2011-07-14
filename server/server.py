from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from mako.template import Template
from mako.lookup import TemplateLookup

import urllib2

PORT = 8080

tl = TemplateLookup(directories=['templates'], module_directory='/tmp/mako_modules')

class BaseHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        h = self.path.split("/")[1]
        if h in Handlers.keys():
            Handlers[h].get(self)
        else:
            self.send_error(404,'Resource Not Found: %s' % self.path)

    def do_POST(self):
        print self.path.split("/")

class FacebookHandler():
    def get(self, request):
        request.send_response(200)
        request.send_header('Content-type', 'text/html')
        request.end_headers()
        template ='facebook/canvas.mak'
        json = urllib2.urlopen("http://localhost:5984/socialfarm_public/_all_docs")
        request.wfile.write(tl.get_template(template).render(json))

    def post(self, request):
        print "post"

Handlers = {'facebook': FacebookHandler()}


def main():
    try:
        server_address = ('', PORT)
        server = HTTPServer(server_address, BaseHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()
