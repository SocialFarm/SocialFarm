#!/usr/bin/env python 

# clear couchdb for make 

import os, sys, getopt
from pprint import pprint 
from couchdb.client import Database, Server 


def _usage() :
    print 'Usage : %s --help' % sys.argv[0] 
    print 'Usage : %s [-l <username:password>] [-u <couchdburl>] <dbname>' % sys.argv[0]
    print 'WARNING: this script is meant to clear the localhost couchdb, for use with make only!' 
    sys.exit(-1) 



if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:] , 'l:u:h' , ["login" , "url" , "help"])
    except getopt.GetoptError, err:
        print str(err) 
        _usage()

    url = 'http://socialfarm.iriscouch.com'
    for o, a in opts:
        if o in ("--login" , "-l") :
            username, password = a.split(':') 
        if o in ("--url" , "-u") :
            url = a
        if o in ("--help" , "-h" ) :
            _usage() 
    
    if 'SF_CRED' in os.environ.keys():
        username = os.environ['SF_USERNAME']
        password = os.environ['SF_PASSWORD']
    else:
        if username == None or password == None:
            raise Exception("Invalid CREDENTIALS!")


    server = Server(url)
    if username: 
        server.resource.credentials = (username, password)
    
    if args[0] in server: 
        del server[args[0]]
  
 


