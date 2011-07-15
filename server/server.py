
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from templatemapper import templatemapper 
from SocialFarmHelper import SocialFarm

import urllib2

PORT = 8080
FACEBOOK_APP_ID       = '234690403213067'
FACEBOOK_API_KEY      = '7165704a80616d58e50629512349a8c1'
FACEBOOK_APi_SECRET   = '14a74c4bcf2537f42d714c5cd8324c6e'
FACEBOOK_CALLBACK_URL = 'http://apps.facebook.com/social_farm/'

#SocialFarmInterfaceWrapper
class URLWrapper(object) :       

    def __init__(self, srctemplate, tgttemplate, prefixcode, suffixcode) : 
        self.prefixcode = prefixcode
        self.suffixcode = suffixcode 
        self.template = templatemapper( srctemplate, tgttemplate )  

    def get(self, request):
        request.send_response(200)
        request.send_header('Content-type', 'text/html')
        request.end_headers()

        target = self.template.replace(request.path) 

        json = urllib2.urlopen("http://localhost:5984/%s" % target ).read()

        request.wfile.write(self.prefixcode)
        request.wfile.write("json = %s;" % json.strip()) 
        request.wfile.write(self.suffixcode) 


    def post(self, request):
        print "post"

prefix = """
<!doctype html>  
<html lang="en">
    <head>  
        <meta charset="utf-8">  
        <title>social_farm</title>  
        <meta name="description" content="...">  
        <meta name="author" content="Social Farm"> 
        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js" type="text/javascript"></script> 

        <!--
        ### in the future prefex script should be included here and called below
        ### for now I am imitating what it would do below, normally, the document ready would look like: 
        ### prefix_js.run()
        ---> 
        
        <script>
        """

suffix = """
        $(document).ready(function() {
            jQuery.each(json, function() {
                $("#json_wrapper").append('<p>' + this.toString() + '</p>');
                console.log(this)
            });

        });
   </script>

    </head>  
    <body>
        <h1>social_farm</h1>
        <ul>
            <li><a href='""" + FACEBOOK_CALLBACK_URL + """getbusiness/testbus'> get testbus</a></li>
        </ul>
        <div id="json_wrapper"></div>

        <div id="fb-root"></div>
        <script>
            window.fbAsyncInit = function() {
                FB.init({
                appId  : '""" + FACEBOOK_APP_ID + """',
                status : true, // check login status
                cookie : true, // enable cookies to allow the server to access the session
                xfbml  : true  // parse XFBML
                });
            };

            (function() {
                var e = document.createElement('script');
                e.src = document.location.protocol + '//connect.facebook.net/en_US/all.js';
                e.async = true;
                document.getElementById('fb-root').appendChild(e);
            }());
            FB.api('/me', function(response) {
                alert(response.name);
            });
        </script>
        
    </body>
</html>

""" 

templates_wrappers = {
'allbusiness' : URLWrapper('/allbusiness/{startkey}/{count}', '/socialfarm/_all_docs/?start_key={startkey}&count={count}', prefix, suffix), 
'getbusiness' : URLWrapper('/getbusiness/{id}' , '/socialfarm/{id}', prefix, suffix), 
#'deletebusiness' : CodeWrapper('/deletebusiness/{id}', pythonobj , method ) 
}




class BaseHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if len(self.path.split('/')) == 2:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(prefix)
            self.wfile.write(suffix)
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




