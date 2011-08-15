#!/usr/bin/env python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from templatemapper import templatemapper
import httplib2, urllib, json, sys, getopt

patterns = {
'businesses'             : templatemapper('/businesses{}',                   '/socialfarm/_design/business/_list/basic_html/all{}'),
'business'               : templatemapper('/business/{bid}' ,                '/socialfarm/_design/business/_show/basic_html/{bid}'), 

'business.members'       : templatemapper('/business/{bid}/members' ,        '/{bid}/_design/info/_list/members_basic_html/all_members'), 
'business.member'        : templatemapper('/business/{bid}/member/{mid}' ,   '/{bid}/_design/info/_show/member_basic_html/{mid}'), 

'business.actions'       : templatemapper('/business/{bid}/actions' ,        '/{bid}/_design/info/_list/actions_basic_html/all_actions'), 
'business.action'        : templatemapper('/business/{bid}/action/{aid}' ,   '/{bid}/_design/info/_show/action_basic_html/{aid}'), 

'business.jobs'          : templatemapper('/business/{bid}/jobs' ,           '/{bid}/_design/info/_list/jobs_basic_html/all_jobs'), 
'business.job'           : templatemapper('/business/{bid}/job/{jid}' ,      '/{bid}/_design/info/_show/job_basic_html/{jid}'), 

'business.tasks'         : templatemapper('/business/{bid}/tasks' ,          '/{bid}/_design/info/_list/tasks_basic_html/all_tasks'), 
'business.task'          : templatemapper('/business/{bid}/task/{tid}' ,     '/{bid}/_design/info/_show/task_basic_html/{tid}'), 
'business.tasks'         : templatemapper('/business/{bid}/tasks/{mid}',     '/{bid}/_design/info/_list/tasks_basic_html/all_tasks?key="{mid}"'),

'api.businesses'         : templatemapper('/api/businesses{}',               '/socialfarm/_design/business/_view/all{}'),
'api.business'           : templatemapper('/api/business/{bid}' ,            '/socialfarm/{bid}'),
'api.business.members'   : templatemapper('/api/business/{bid}/members' ,    '/{bid}/_design/info/_view/all_members'), 
'api.business.actions'   : templatemapper('/api/business/{bid}/actions' ,    '/{bid}/_design/info/_view/all_actions'), 
'api.business.jobs'      : templatemapper('/api/business/{bid}/jobs' ,       '/{bid}/_design/info/_view/all_jobs'), 
'api.business.tasks'     : templatemapper('/api/business/{bid}/tasks' ,      '/{bid}/_design/info/_view/all_tasks'), 
'api.business.id'        : templatemapper('/api/{bid}/{id}' ,                '/{bid}/{id}'), 

'my_businessses'         : templatemapper('/my_businesses/{mid}',           '/socialfarm/_design/business/_show/my_businesses/{mid}'), 
'business.join'          : templatemapper('/business/{bid}/join',            '/socialfarm/_design/business/_show/join_business/{bid}'), 

'facebook'        		 : templatemapper('/facebook/{}',          		     '/socialfarm/_design/business/_list/facebook_canvas/all_businesses{}'),
''        		 		 : templatemapper('/{}',          		     		 '/socialfarm/_design/business/_list/facebook_canvas/all_businesses{}'),

}

reserved = ['my_businessses', 'api', 'join', 'static', 'channel', 'facebook', 'businesses', 'business', 'members', 'member', 'actions', 'action', 'jobs', 'job', 'tasks', 'task' ]

#function strips a path to a dotted string of the reserved words it contained
def path_to_key(path):
	parts = filter(lambda x: x in reserved, path.split('/'))
	key = ".".join(parts)
	return key if key != 'api' else 'api.business.id'


class Adapter(BaseHTTPRequestHandler) :  
     
    def do_GET(self):
        key = path_to_key(self.path)
        url = 'http://%s:%s' % dst_server + patterns[key].replace(self.path) 
        response, content = httplib2.Http().request(url, "GET")
        self.write_response(response, content)

    def do_PUT(self):
        key = path_to_key(self.path)
        url = 'http://%s:%s' % dst_server + patterns[key].replace(self.path) 
        headers = { "content-type": "application/json" }
        data =  self.rfile.read((int(self.headers['content-length'])))
        response, content = httplib2.Http().request(url, "PUT", body = data, headers = headers)
        self.write_response(response, content)

    def do_POST(self):
        key = path_to_key(self.path)
        url = 'http://%s:%s' % dst_server + patterns[key].replace(self.path) 
        headers = { "content-type": "application/json" }
        data =  self.rfile.read((int(self.headers['content-length'])))

        response, content = httplib2.Http().request(url, "GET")

        record = json.loads(content)
        fields = json.loads(data)

        for k in fields.keys():
            record[k] = fields[k] if record[k] != fields[k] else record[k]

        response, content = httplib2.Http().request(url, "PUT", body = data, headers = headers)
        self.write_response(response, content)

    def write_response(self, response, content):
        self.send_response(int(response['status']))
        self.send_header('content-type', response['content-type'])
        self.end_headers()
        self.wfile.write(content)

def _usage() :
    print 'Usage : %s --help' % sys.argv[0] 
    print 'Usage : %s [-s <host:port>] [-d <host:port>]' % sys.argv[0]
    sys.exit(-1) 
      
if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:] , 's:d:h' , ["source" , "destination" , "help"])
    except getopt.GetoptError, err:
        print str(err) 
        _usage()

    src_server = ('', 80)
    dst_server = ('127.0.0.1', 5984)

    for o, a in opts:
        if o in ("--source" , "-s") :
            src_server = (a.split(':')[0], int(a.split(':')[1]))
        if o in ("--destination" , "-d") :
            dst_server = (a.split(':')[0], int(a.split(':')[1]))
        if o in ("--help" , "-h" ) :
            _usage() 
    try:
        server = HTTPServer(src_server, Adapter)
        print 'started httpserver at %s:%s' % src_server
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

   


