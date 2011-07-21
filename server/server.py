
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from templatemapper import templatemapper 

import urllib2

PORT = 80

#SocialFarmInterfaceWrapper
class URLWrapper(object) :       

    def __init__(self, srctemplate, tgttemplate) : 
        self.template = templatemapper( srctemplate, tgttemplate )  

    def get(self, request):
        request.send_response(200)
        request.send_header('Content-type', 'text/html')
        request.end_headers()
        target = self.template.replace(request.path) 
        page = urllib2.urlopen("http://localhost:5984/%s" % target ).read()
        request.wfile.write(page) 


    def post(self, request):
        print "post"

templates_wrappers = {
'getbusiness' : URLWrapper('/getbusiness/{id}' , '/socialfarm/_design/business/_show/mustache_show/{id}'), 
}

""" list views which need to be wrapped
'deletebusiness' : CodeWrapper('/deletebusiness/{id}', pythonobj , method ) 
'allbusiness' : URLWrapper('/allbusiness/{startkey}/{count}', '/socialfarm/_all_docs/?start_key={startkey}&count={count}'), 
"""




class BaseHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.split('/')[1] in templates_wrappers.keys(): 
            templates_wrappers[self.path.split('/')[1]].get(self)
           
          
    def do_POST(self):
        print self.path.split("/")


def main():
    try:
        server_address = ('', PORT)
        server = HTTPServer(server_address, BaseHandler)
        print 'started httpserver at http://127.0.0.1:%s' % PORT
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()




