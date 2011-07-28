import unittest
import urllib

views = [
'http://localhost:5984/socialfarm/_design/business/_view/all',
'http://127.0.0.1:5984/testbus/_design/info/_view/all_members',
'http://127.0.0.1:5984/testbus/_design/info/_view/all_actions',
'http://127.0.0.1:5984/testbus/_design/info/_view/all_jobs',
'http://127.0.0.1:5984/testbus/_design/info/_view/all_jobs?startkey=%22dalai%20lama%22',
'http://127.0.0.1:5984/testbus/_design/info/_view/all_tasks',
'http://127.0.0.1:5984/testbus/_design/info/_view/all_tasks?startkey=%22dalai%20lama.1311810672%22'
]

shows = [
'http://localhost:5984/socialfarm/_design/business/_show/basic_html/testbus',
'http://localhost:5984/testbus/_design/info/_show/member_basic_html/osteele',
'http://localhost:5984/testbus/_design/info/_show/action_basic_html/C',
'http://localhost:5984/testbus/_design/info/_show/job_basic_html/pope.1311187292',
'http://localhost:5984/testbus/_design/info/_show/task_basic_html/pope.1311187292.task.D'
]
lists = [
'http://localhost:5984/socialfarm/_design/business/_list/basic_html/all',
'http://localhost:5984/testbus/_design/info/_list/members_basic_html/all_members',
'http://localhost:5984/testbus/_design/info/_list/actions_basic_html/all_actions',
'http://localhost:5984/testbus/_design/info/_list/jobs_basic_html/all_jobs',
'http://localhost:5984/testbus/_design/info/_list/tasks_basic_html/all_tasks'
]


#self.assertTrue(element in self.seq)

class TestGET(unittest.TestCase):
    def setUp(self):
        self.views = views
        self.shows = shows
        self.lists = lists

    def test_gets(self):
        print "testing views..."
        for v in self.views:
            code = urllib.urlopen(v).getcode()
            print "\t[%s] GET %s" % (code, v)
            self.assertEqual(code, 200)

        print "\ntesting shows..."
        for s in self.shows:
            code = urllib.urlopen(s).getcode()
            print "\t[%s] GET %s" % (code, s)
            self.assertEqual(code, 200)

        print "\ntesting shows..."
        for l in self.lists:
            code = urllib.urlopen(l).getcode()
            print "\t[%s] GET %s" % (code, l)
            self.assertEqual(code, 200)

if __name__ == '__main__':
    unittest.main()

