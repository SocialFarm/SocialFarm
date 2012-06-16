#!/usr/bin/env python 


# Bridge from cgi to socialfarm couch db database

import urllib2 
import cgi 
import cgitb
cgitb.enable()
# cgitb.enable(display=0, logdir="/tmp")



# Reading material 
# http://www.tutorialspoint.com/python/python_cgi_programming.htm 
# may need on linux : 
#    setsebool -P httpd_can_network_connect 1
 

form = cgi.FieldStorage() 
couchurl = first_name = form.getvalue('curl')



couchurl = 'http://127.0.0.1:5984/social_news/_design/info/_list/members/all_members' 

print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers

fd = urllib2.urlopen(couchurl)
print fd.read() 

