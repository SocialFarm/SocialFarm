
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

        http_code = url.getcode()
        content_type = 'text/html' if request.path.split('/')[1] != 'api' else 'application/json'

        request.send_response(http_code)
        request.send_header('Content-type', content_type)
        request.end_headers()
        request.wfile.write(page) 


    def post(self, request):
        print "post"

wrappers = {
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

'api.businesses'             : URLWrapper('/api/businesses{}',               '/socialfarm/_design/business/_view/all{}'),
'api.business'               : URLWrapper('/api/business/{bid}' ,            '/{bid}'),
'api.business.members'       : URLWrapper('/api/business/{bid}/members' ,    '/{bid}/_design/info/_view/all_members'), 
'api.business.actions'       : URLWrapper('/api/business/{bid}/actions' ,    '/{bid}/_design/info/_view/all_actions'), 
'api.business.jobs'          : URLWrapper('/api/business/{bid}/jobs' ,       '/{bid}/_design/info/_view/all_jobs'), 
'api.business.tasks'         : URLWrapper('/api/business/{bid}/tasks' ,      '/{bid}/_design/info/_view/all_tasks'), 
'api.business.id'            : URLWrapper('/api/business/{bid}/{id}' ,       '/{bid}/{id}'), 
}

""" for /api/
/testbus/_design/info/_view/all_jobs?startkey={key}
/testbus/_design/info/_view/all_tasks?startkey={key}
"""

resources = ['members', 'actions', 'jobs', 'tasks', 'member', 'action', 'job', 'task']

class BaseHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split('/')
        if path[1] == 'api':
            if path[2] == 'businesses':
                map_key = "api.businesses"
            elif path[2] == 'business' and len(path) == 4:
                map_key = 'api.business'
            elif len(path) == 5 and path[4] not in resources:
                map_key = 'api.business.id'
            else:
                map_key = 'api.business.%s' % path[4]
        
        elif path[1] == 'business':
            print path
            if len(path) == 3:
                map_key = 'business'
            else:
                map_key = path[3]

        elif path[1] == 'businesses':
            map_key = 'businesses'
        else:
            print "invalid uri: %s" % self.path
            x = 9000/0

        if map_key in wrappers.keys(): 
            wrappers[map_key].get(self)
        else:
            print "invalid key: %s" % map_key
            x = 9000/0
                   
    def do_PUT(self):
        body =  self.rfile.read()
        """
        self.send_response(http_code)
        self.send_header('Content-type', content_type)
        self.end_headers()
        self.wfile.write(page) 
        """


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




