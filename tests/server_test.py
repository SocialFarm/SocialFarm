import unittest
import urllib, httplib

server = '127.0.0.1:8080'
bus = 'testbus'
member = 'osteele'
action = 'C'
job = 'pope.1311187292'
task = 'pope.1311187292.task.D'

pages = [
'http://%s/businesses'              % (server),
'http://%s/business/%s'             % (server, bus),
'http://%s/business/%s/members'     % (server, bus),
'http://%s/business/%s/actions'     % (server, bus),
'http://%s/business/%s/jobs'        % (server, bus),
'http://%s/business/%s/tasks'       % (server, bus),
'http://%s/business/%s/member/%s'   % (server, bus, member),
'http://%s/business/%s/action/%s'   % (server, bus, action),
# broken becuase of '.' in id
#'http://%s/business/%s/job/%s'      % (server, bus, job),
#'http://%s/business/%s/task/%s'     % (server, bus, task),
]

api_calls = [
'http://%s/api/businesses'              % (server),
'http://%s/api/business/%s'             % (server, bus),
'http://%s/api/business/%s/members'     % (server, bus),
'http://%s/api/business/%s/actions'     % (server, bus),
'http://%s/api/business/%s/jobs'        % (server, bus),
'http://%s/api/business/%s/tasks'       % (server, bus),
'http://%s/api/business/%s/%s'   % (server, bus, member),
'http://%s/api/business/%s/%s'   % (server, bus, action),
]

puts = {
'http://%s/socialfarm/b22222' % server: """{"_rev":"1-160fb33733e61d6f3d98da5a2798d8bd","type":"business","author":"vpathak","description":"this business aims to do nothing","list_of_partners":["iftode","vpathak","smaldone","osteele"],"started_since":"7-7-2011","list_of_roles":["role0"],"total_rating":0.0,"total_profit":0.1}"""
}

"""
class TestGET(unittest.TestCase):
    def setUp(self):
        self.pages = pages
        self.api_calls = api_calls

    def test_api(self):
        print "\ntesting api...\n"
        for url in self.api_calls:
            code = urllib.urlopen(url).getcode()
            print "\t[%s] GET %s" % (code, url)
            self.assertEqual(code, 200)
        print "DONE"
      
    def test_templates(self):
        print "\ntesting templates...\n"
        for url in self.pages:
            code = urllib.urlopen(url).getcode()
            print "\t[%s] GET %s" % (code, url)
            self.assertEqual(code, 200)
        print "DONE"
"""

class TestPUT(unittest.TestCase):
    def setUp(self):
        self.puts = puts

    def test_puts(self):
        print "\ntesting puts...\n"
        for p in self.puts:
            opener = urllib2.build_opener(urllib2.HTTPHandler)
            request = urllib2.Request(p.split('|||')[0], data=p.split('|||')[1])
            request.add_header('Content-Type', 'application/json')
            request.get_method = lambda: 'PUT'
            url = opener.open(request)
            print url
        print "DONE"
      
  



if __name__ == '__main__':
    #unittest.main()
    
    connection =  httplib.HTTPConnection('127.0.0.1:8080')
    body_content = puts['http://127.0.0.1:8080/socialfarm/b22222']
    connection.request('PUT', '/socialfarm/b22222', body_content)
    result = connection.getresponse()
    print result.__dict__

