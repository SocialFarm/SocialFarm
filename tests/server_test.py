import unittest
import httplib2, urllib2, urllib, json
from couchdb import json as j
from datetime import datetime

server = '127.0.0.1:8080'
bus = 'testbus'
member = 'osteele'
action = 'C'
job = 'pope.1311187292'
task = 'pope.1311187292.task.D'

gets = [
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
'http://%s/api/businesses'              % (server),
'http://%s/api/business/%s'             % (server, bus),
'http://%s/api/business/%s/members'     % (server, bus),
'http://%s/api/business/%s/actions'     % (server, bus),
'http://%s/api/business/%s/jobs'        % (server, bus),
'http://%s/api/business/%s/tasks'       % (server, bus),
#broken because of pattern
#'http://%s/api/business/%s/%s'   % (server, bus, member),
#'http://%s/api/business/%s/%s'   % (server, bus, action),
]

jobs = [
'http://%s/api/testbus/pope.1311187292' % server, 
# broken space in id
#'http://%s/api/testbus/dalai lama.1311187292' % server,
]

bus = [
'http://%s/api/business/testbus' % server, 
'http://%s/api/business/testbus2' % server, 
]

class TestServer(unittest.TestCase):
    def setUp(self):
        self.gets = gets
        self.jobs = jobs
        self.bus = bus

    def test_gets(self):
        print "\ntesting gets...\n"
        for url in self.gets:
            response, content = httplib2.Http().request(url, "GET")
            print "\t[%s] GET %s" % (response['status'], url)
            self.assertEqual(response['status'], '200')
        """
    def test_puts(self):
        print "\ntesting PUT for jobs...\n"
        for url in self.jobs:
            data = urllib.urlopen(url).read()
            data = json.loads(data.strip())
            data['price'] = float(data['price']) + .01
            data = j.encode(data).encode('utf-8')
            headers = { "content-type": "application/json", 'content-length': str(len(data))}
            response, content = httplib2.Http().request(url, "PUT", body = data, headers = headers)

            print "\t[%s] GET %s" % (response['status'], url)
            self.assertEqual(response['status'], '201')
    
        print "\ntesting PUT for businesses...\n"
        for url in self.bus:
            data = urllib.urlopen(url).read()
            data = json.loads(data.strip())
            data['total_profit'] = float(data['total_profit']) + .01
            data = j.encode(data).encode('utf-8')
            headers = { "content-type": "application/json", 'content-length': str(len(data))}
            response, content = httplib2.Http().request(url, "PUT", body = data, headers = headers)

            print "\t[%s] GET %s" % (response['status'], url)
            self.assertEqual(response['status'], '201')
        """

    def test_posts(self):
        print "\ntesting POST...\n"
        for url in self.bus:
            data = urllib.urlopen(url).read()
            data = json.loads(data.strip())
            for k in data.keys():
                if k == 'description':
                    data['description'] = 'todays business was created %s' % datetime.today()
                elif k != '_id' and k != '_rev':
                    del data[k]
            data = j.encode(data).encode('utf-8')
            print "POST data = %s" % data
            headers = { "content-type": "application/x-www-form-urlencoded", 'content-length': str(len(data))}
            response, content = httplib2.Http().request(url, "POST", body = data, headers = headers)
            print "\t[%s] POST %s" % (response['status'], url)
            self.assertEqual(response['status'], '201')
    
      
   
if __name__ == '__main__':
    unittest.main()
    
   

