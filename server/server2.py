from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from templatemapper import templatemapper 

import urllib2

PORT = 8080

templates_wrappers = {
    'allbusiness' : URLWrapper('/allbusiness/{startkey}/{count}' , '/socialfarm/_all_docs/?start_key={startkey}&count={count}' , 'http://.../someprefix.js' , 'http://.../somesuffix.js') , 
    'getbusiness' : URLWrapper('/getbusiness/{id}' , '/socialfarm/{id}' , 'http://.../someprefix.js' , 'http://.../somesuffix.js' )
    'deletebusiness' : CodeWrapper('/deletebusiness/{id}', pythonobj , method ) 
    }




class BaseHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        for t in templates_wrappers: 
            if t.match(self.path) :

        h = self.path.split("/")[1]
        if h in Handlers.keys():
            Handlers[h].get(self)
        else:
            self.send_error(404,'Resource Not Found: %s' % self.path)

    def do_POST(self):
        print self.path.split("/")





class URLWrapper(SocialFarmInterfaceWrapper) :       

    def __init__(self, srctemplate, tgttemplate, prefixcode, suffixcode) : 
        self.prefixcode = prefixcode
        self.suffixcode = suffixcode 
        self.template = templatemapper( srctemplate, tgttemplate )  

    def get(self, request):
        request.send_response(200)
        request.send_header('Content-type', 'text/html')
        request.end_headers()

        target = self.template.replace(request.path) 

        json = urllib2.urlopen("http://localhost:5984/%s" % target )

        request.wfile.write(self.prefixcode)
        request.wfile.write(json) 
        request.wfile.write(self.suffixcode) 


    def post(self, request):
        print "post"






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




