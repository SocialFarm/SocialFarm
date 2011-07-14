#!/usr/bin/env python 

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urllib2
import urlparse

PORT = 8080


class MultiplexerHandler(BaseHTTPRequestHandler):

    def register
    def do_GET(self):
        #print 'got path' , self.path 
        
        h = self.path.split("/")
        print repr(h) 

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
