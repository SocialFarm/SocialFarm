import unittest
import urllib

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
'http://%s/business/%s/job/%s'      % (server, bus, job),
'http://%s/business/%s/task/%s'     % (server, bus, task),
]

class TestGET(unittest.TestCase):
    def setUp(self):
        self.gets = gets
       
    def test_gets(self):
        print "testing gets..."
        for g in self.gets:
            print g
            code = urllib.urlopen(g).getcode()
            print "\t[%s] GET %s" % (code, g)
            self.assertEqual(code, 200)

if __name__ == '__main__':
    unittest.main()

