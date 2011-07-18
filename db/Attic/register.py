#!/usr/bin/env python 

from couchdb.client import Database, Server 
from couchdb.design import ViewDefinition

if __name__ == "__main__":
    import sys 
    if len(sys.argv) < 6: 
        print "Usage : %s  <user> <pwd> <designname> <viewname> <map.js> [<reduce.js>] " 
        sys.exit(-1) 

    server = Server()
    server.resource.credentials = (sys.argv[1] , sys.argv[2])
    if 'socialfarm_business_template' not in server: 
        server.create( 'socialfarm_business_template' ) 

    db = server['socialfarm_business_template'] 

    mapfn = open(sys.argv[5]).read()
    reducefn = None 
    if len(sys.argv) == 7: 
        reducefn = open(sys.argv[6]).read()  
    
    view = ViewDefinition( sys.argv[3] , 
                           sys.argv[4] , 
                           mapfn, reducefn ) 
    view.sync( db ) 

    print 'registered view %s:%s' % ( sys.argv[3] , sys.argv[4] ) 
