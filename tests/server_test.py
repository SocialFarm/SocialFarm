import unittest
import httplib2, urllib2, urllib,  json


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

puts = [




]

""" broken becuase of version conflic

http://%s/api/testbus/d73889570eebd5ded5a223dd3819bdf6 ||| 
{
    "_rev":"1-e88fa41e5d5bde4c41ae6eedc189d7d7",
    "skills_required":["s2"],
    "name":null,
    "state":"ready",
    "jobid":"job-003",
    "activityid":"B",
    "prevtid":"3e722b1597f32eab203d82db332f75ae",
    "address":"somerset, nj" ,
    "type":"task"
} % server

http://%s/api/business/b22222 ||| { 
    "_rev":"1-160fb33733e61d6f3d98da5a2798d8bd",
    "type":"business",
    "author":"vpathak",
    "description":"this business aims to do nothing",
    "list_of_partners":["iftode","vpathak","smaldone","osteele"],
    "started_since":"7-7-2011","list_of_roles":["role0"],
    "total_rating":0.0,
    "total_profit":0.1
} % server,

"""


class TestServer(unittest.TestCase):
    def setUp(self):
        self.gets = gets
        self.puts = puts

    def test_gets(self):
        print "\ntesting gets...\n"
        for url in self.gets:
            response, content = httplib2.Http().request(url, "GET")
            print "\t[%s] GET %s" % (response['status'], url)
            self.assertEqual(response['status'], '200')
        print "DONE"

    def test_puts(self):
        print "\ntesting puts...\n"
        for p in self.puts:
            (url, data) = p.split('|||')
            data = json.loads(data.strip())
            data = urllib.urlencode(data)
            headers = { "content-type": "application/json", 'content-length': str(len(data)) }
       
            response, content = httplib2.Http().request(url, "PUT", body = data, headers = headers)

            print response
            print "\t[%s] GET %s" % (response['status'], url)
            self.assertEqual(response['status'], '200')
        print "DONE"





if __name__ == '__main__':
    unittest.main()
    
   

