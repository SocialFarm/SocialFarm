
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from templatemapper import templatemapper 

import urllib2

PORT = 8080


""" scraps
SocialFarmInterfaceWrapper
'deletebusiness' : CodeWrapper('/deletebusiness/{id}', pythonobj , method ) 
'allbusiness' : URLWrapper('/allbusiness/{startkey}/{count}', '/socialfarm/_all_docs/?start_key={startkey}&count={count}'), 
"""

class URLWrapper(object) :       

    def __init__(self, srctemplate, tgttemplate) : 
        self.template = templatemapper( srctemplate, tgttemplate )  

    def get(self, request):
        target = self.template.replace(request.path) 
        url = urllib2.urlopen("http://localhost:5984/%s" % target )
        page = url.read() if url.getcode() == 200 else "error"
        request.send_response(url.getcode())
        request.send_header('Content-type', 'text/html')
        request.end_headers()
        request.wfile.write(page) 


    def post(self, request):
        print "post"

templates_wrappers = {
'businesses'    : URLWrapper('/businesses{}',                   '/socialfarm/_design/business/_list/basic_html/all{}'),
'business'      : URLWrapper('/business/{bid}' ,                '/socialfarm/_design/business/_show/basic_html/{bid}'), 
'members'       : URLWrapper('/business/{bid}/members' ,        '/{bid}/_design/info/_list/members_basic_html/all_members'), 
'member'        : URLWrapper('/business/{bid}/member/{mid}' ,   '/{bid}/_design/info/_show/member_basic_html/{mid}'), 
'actions'       : URLWrapper('/business/{bid}/actions' ,        '/{bid}/_design/info/_list/actions_basic_html/all_actions'), 
'action'        : URLWrapper('/business/{bid}/action/{aid}' ,   '/{bid}/_design/info/_show/action_basic_html/{aid}'), 
'jobs'          : URLWrapper('/business/{bid}/jobs' ,           '/{bid}/_design/info/_list/jobs_basic_html/all_jobs'), 
'job'           : URLWrapper('/business/{bid}/job/{jid}' ,      '/{bid}/_design/info/_show/job_basic_html/{jid}'), 
'tasks'         : URLWrapper('/business/{bid}/tasks' ,          '/{bid}/_design/info/_list/tasks_basic_html/all_tasks'), 
'task'          : URLWrapper('/business/{bid}/task/{tid}' ,     '/{bid}/_design/info/_show/task_basic_html/{tid}'), 
}





class BaseHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        map_key = self.path.split('/')[1] if len(self.path.split('/')) < 4 else self.path.split('/')[3]
        print map_key
        if map_key in templates_wrappers.keys(): 
            templates_wrappers[map_key].get(self)
            
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




