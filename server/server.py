from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import facebook

PORT = 8080
FACEBOOK_APP_ID       = '234690403213067'
FACEBOOK_API_KEY      = '7165704a80616d58e50629512349a8c1'
FACEBOOK_APi_SECRET   = '14a74c4bcf2537f42d714c5cd8324c6e'
FACEBOOK_CALLBACK_URL = 'http://apps.facebook.com/social_farm/'

class FBHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.user = None
        BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

    def setUser(self):
        cookies = self.headers.get('Cookie')
        if cookies:
            morsel = Cookie.BaseCookie(cookies).get('user')
            if morsel:
                self.user = morsel.value

    def do_GET(self):

        self.setUser()

        if not self.user:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            response = """
            <script language="javascript">
                top.location.href='https://graph.facebook.com/oauth/authorize?client_id={0}&redirect_uri={1}&display=page&scope=publish_stream';
            </script>
            <noscript>
            <a href="https://graph.facebook.com/oauth/authorize?client_id={0}&redirect_uri={1}&display=page&scope=publish_stream" target="_top">
                Authorize this application
            </a>
            </noscript>""".format(FACEBOOK_APP_ID,FACEBOOK_CALLBACK_URL)
            self.wfile.write(response)
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("user: %s" % (self.user))

    def do_POST(self):
        print self.path.split("/")





def main():
    try:
        server_address = ('', PORT)
        server = HTTPServer(server_address, FBHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()
