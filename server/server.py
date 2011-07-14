from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import facebook

PORT = 80
FACEBOOK_APP_ID       = '234690403213067'
FACEBOOK_API_KEY      = '7165704a80616d58e50629512349a8c1'
FACEBOOK_APi_SECRET   = '14a74c4bcf2537f42d714c5cd8324c6e'
FACEBOOK_CALLBACK_URL = 'http://apps.facebook.com/social_farm/facebook/'

class BaseHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.split("/")[1] in Handlers.keys():
            Handlers[self.path.split("/")[1]].login(self)
        else:
            self.send_error(404,'Resource Not Found: %s' % self.path)

    def do_POST(self):
        print self.path.split("/")

class FacebookHandler():
    def login(self, request):
        if not False:
            request.send_response(200)
            request.send_header('Content-type', 'text/html')
            request.end_headers()
            response = """
            <script language="javascript">
            top.location.href='https://graph.facebook.com/oauth/authorize?client_id={0}&redirect_uri={1}&display=page&scope=publish_stream';
            </script>
            <noscript>
            <a href="https://graph.facebook.com/oauth/authorize?client_id={0}&redirect_uri={1}&display=page&scope=publish_stream" target="_top">Click here to authorize this application</a>
            </noscript>""".format(FACEBOOK_APP_ID,FACEBOOK_CALLBACK_URL)
            request.wfile.write(response)
        else:
            request.send_response(301)
            request.send_header("Location", FACEBOOK_CALLBACK_URL)
            request.end_headers()

    def get(self, request):
        request.send_response(200)
        request.send_header('Content-type', 'text/html')
        request.end_headers()
        request.wfile.write("foo")

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
