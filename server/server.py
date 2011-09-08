#!/usr/bin/env python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from templatemapper import templatemapper
import httplib2, urllib, json, sys, getopt, os

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
DEBUG = True

patterns = {
''        		         : templatemapper('/{}',          		             '/socialfarm/_design/business/_list/businesses/all_businesses{}'),
#shows
'my_tasks'               : templatemapper('/my_tasks/{mid}',                        '/socialfarm/_design/business/_show/my_tasks/{mid}'),
'my_businesses'          : templatemapper('/my_businesses/{mid}',                   '/socialfarm/_design/business/_show/my_businesses/{mid}'), 
'business'               : templatemapper('/business/{bid}' ,                '/socialfarm/_design/business/_show/business/{bid}'), 
'business.join'          : templatemapper('/business/{bid}/join',                   '/socialfarm/_design/business/_show/join_business/{bid}'), 
'business.member'        : templatemapper('/business/{bid}/member/{mid}' ,   '/{bid}/_design/info/_show/member/{mid}'), 
'business.activity'      : templatemapper('/business/{bid}/activity/{aid}' , '/{bid}/_design/info/_show/activity/{aid}'),
'business.job'           : templatemapper('/business/{bid}/job/{jid}' ,      '/{bid}/_design/info/_show/job/{jid}'),
'business.task'          : templatemapper('/business/{bid}/task/{tid}' ,     '/{bid}/_design/info/_show/task/{tid}'),
#lists
'businesses'             : templatemapper('/businesses{}',                   '/socialfarm/_design/business/_list/businesses/all_businesses{}'),
'business.members'       : templatemapper('/business/{bid}/members' ,        '/{bid}/_design/info/_list/members/all_members'), 
'business.activities'    : templatemapper('/business/{bid}/activities' ,     '/{bid}/_design/info/_list/activities/all_activities'), 
'business.jobs'          : templatemapper('/business/{bid}/jobs' ,           '/{bid}/_design/info/_list/jobs/all_jobs'), 
'business.tasks'         : templatemapper('/business/{bid}/tasks' ,          '/{bid}/_design/info/_list/tasks/all_tasks'), 
# views
'api.businesses'                    : templatemapper('/api/businesses{}',                                   '/socialfarm/_design/business/_view/all_businesses{}'),
'api.business'                      : templatemapper('/api/business/{bid}' ,                                '/socialfarm/{bid}'),
'api.person'                        : templatemapper('/api/person/{mid}' ,                                  '/socialfarm/{mid}'),
'api.business.members'              : templatemapper('/api/business/{bid}/members' ,                        '/{bid}/_design/info/_view/all_members'), 
'api.business.activities'           : templatemapper('/api/business/{bid}/activities' ,                     '/{bid}/_design/info/_view/all_activities'), 
'api.business.jobs'                 : templatemapper('/api/business/{bid}/jobs' ,                           '/{bid}/_design/info/_view/all_jobs'), 
#'api.business.tasks'               : templatemapper('/api/business/{bid}/tasks' ,                          '/{bid}/_design/info/_view/all_tasks'), 
'api.business.tasks'                : templatemapper('/api/business/{bid}/tasks/{mid}',                     '/{bid}/_design/info/_view/all_tasks?key="{mid}"'),
'api.business.object'               : templatemapper('/api/business/{bid}/object/{id}' ,                    '/{bid}/{id}'), 
'api.business.object.attachment'    : templatemapper('/api/business/{bid}/object/{id}/attachment/{aid}' ,   '/{bid}/{id}/{aid}'), 
}

reserved = ['my_businesses', 'object', 'attachment', 'my_tasks', 'person', 'api', 'join', 'static', 'businesses', 'business', 'members', 'member', 'activities', 'activity', 'jobs', 'job', 'tasks', 'task' ]

#function strips a path to a dotted string of the reserved words it contained
def path_to_key(path):
    parts = filter(lambda x: x in reserved, path.split('/'))
    key = ".".join(parts)
    return key

def authenticate(request):
    if 'AccessToken' in request.headers.keys():
        print "Access Token: ", request.headers['AccessToken']
    else:
        print "Warning! No Access Token provided!"

def serve_static(request):
    path_to_file = os.path.join(SITE_ROOT, request.path[1:])
    content_headers = {
        'html': { 'status': '200', 'content-type': 'text/html; charset=utf-8' },
        'css' : { 'status': '200', 'content-type': 'text/css; charset=utf-8' }, 
        'js'  : { 'status': '200', 'content-type': 'application/x-javascript; charset=utf-8'} , 
        'jar':  { 'status': '200', 'content-type': 'application/java-archive; charset=utf-8'} 
    }
    key = request.path.split('/')[-1].split('.')[-1]
    if os.path.exists( path_to_file ) and os.path.isfile( path_to_file ):
        content = open(path_to_file, 'r').read()
        response = content_headers[key]
        response['content-length'] = str(len(content))
        request.write_response(response, content)
    else:
        not_found(request, request.path)

def not_found(request, path):
    content = "404, invalid url: %s" % path
    response = { 'status': '404', 'content-type': 'text/html; charset=utf-8' }
    response['content-length'] = str(len(content))
    request.write_response(response, content)


def server_error(request, path):
    content = "500, an error occured attempting to access: %s" % path
    response = { 'status': '500', 'content-type': 'text/html; charset=utf-8' }
    response['content-length'] = str(len(content))
    request.write_response(response, content)

def debug(msg):
    if DEBUG:
        print "DEBUG: %s" % msg
        
    
class Adapter(BaseHTTPRequestHandler) :  
     
    def do_GET(self):
        try:
            if self.path.split('/')[1] == 'static':
                serve_static(self)
            else:
                authenticate(self)
                key = path_to_key(self.path)
                if key in patterns:
                    url = 'http://%s:%s' % dst_server + patterns[key].replace(self.path) 
                    response, content = httplib2.Http().request(url, "GET")
                    self.write_response(response, content)
                else:
                    not_found(self, self.path)
        except Exception, e:
            debug(e)
            server_error(self, self.path)
            
            
            

    def do_PUT(self):
        try:
            authenticate(self)
            key = path_to_key(self.path)
            if key in patterns:
                url = 'http://%s:%s' % dst_server + patterns[key].replace(self.path) 
                headers = { "content-type": "application/json" }
                data =  self.rfile.read((int(self.headers['content-length'])))
                response, content = httplib2.Http().request(url, "PUT", body = data, headers = headers)
                self.write_response(response, content)
            else:
                not_found(self, self.path)
        except Exception, e:
            debug(e)
            server_error(self, self.path)

    def do_POST(self):
        try:
            authenticate(self)
            key = path_to_key(self.path)
            if key in patterns:
                url = 'http://%s:%s' % dst_server + patterns[key].replace(self.path) 

                headers = { "content-type": "application/json" }
                data =  self.rfile.read((int(self.headers['content-length'])))
                response, content = httplib2.Http().request(url, "GET")
                
                if self.path != '/':
                    record = json.loads(content)
                    fields = json.loads(data)

                    for k in fields.keys():
                        record[k] = fields[k] if record[k] != fields[k] else record[k]

                    response, content = httplib2.Http().request(url, "PUT", body = data, headers = headers)
                self.write_response(response, content)
            else:
                not_found(self, self.path)
        except Exception, e:
            debug(e)
            server_error(self, self.path)

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

   


