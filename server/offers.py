#!/usr/bin/env python 
import sys, os, couchdb, time
from couchdb.client import Database, Server




##### IMPORT SocialFarm Helper from DB #######
path = os.path.dirname(os.path.abspath(__file__))
path = path[:len(path) - len('server/')] + '/db/scripts/'
print path
if path not in sys.path:
    sys.path.insert(0, path)

import SocialFarmHelper
from SocialFarmHelper import SocialFarm, BusinessDirector




#number of seconds to sleep
SLEEP = 300
    
if len(sys.argv) == 1:
    print "Usage : %s <user> <pwd> [<couchdb url>]"
    sys.exit(-2) 

username = sys.argv[1] 
password = sys.argv[2]
 
if len(sys.argv) == 3: 
    sf = SocialFarm(username, password)
else: 
    sf = SocialFarm(username, password, sys.argv[3] )

while (True):
    for b in sf.db.view('business/all_businesses'):
            print "%s task offers:" % b.id
            bd = BusinessDirector(b.id, username, password)
            for (workerid, taskid) in bd.taskOffers() :
                print '\toffer' , workerid , taskid 
                tdef = bd.db[ taskid ] 
                tdef[ 'worker' ] = workerid
                bd.db[ taskid ] = tdef  
    
    time.sleep(SLEEP)       
