#!/usr/bin/env python 

# Update a single field in the couchdb 
# Can be used to upload design document components 
# Author : vpathak 
# Copyright 2009-2013
# License : Apache (see in repository at https://github.com/SocialFarm/SocialFarm/blob/master/LICENSE.txt)

import os, sys, getopt
from pprint import pprint 
from couchdb.client import Database, Server 


def _usage() :
    print 'Usage : %s --help' % sys.argv[0] 
    print 'Usage : %s [-l <username:password>] [-u <couchdburl>] <dbname> <id> <fldtoupdate> [contentfilename]' % sys.argv[0]
    print 'Format of fldtoupdate: nested keys separated by . , eg: views.listactions.map ' 
    sys.exit(-1) 




def _get_recursive_dict( keylist , data ) :
    if keylist == []: 
        return data 
    else:
        return {keylist[0] : _get_recursive_dict(keylist[1:], data) } 




def _merge_updates(obj, fldkeys, data):
    res = obj
    curr = res
    n = len(fldkeys)
    for i in range(0,n):
        k = fldkeys[i]
        # no key, get the remaining dicts directly 
        if k not in curr:
            curr[k] = _get_recursive_dict( fldkeys[i+1:] , data )
            return res
        # last key, overwrite the data 
        if i == (n-1):
            if len(data) > 0: 
                curr[k] = data
            else:
                del curr[k]
            break
        # another iteration 
        curr = curr[k]
        
    return res







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


    dbname = args[0]
    objid  = args[1]
    fldkeys = args[2].split('.')
    # TODO : use codecs.EncodedFile( fd, ... , errors = "ignore" ) 
    if len(args) == 4: 
        data = open(args[3]).read()
    else :
        data = sys.stdin.read()

    # if the server doesnt have the db, create it
    if dbname not in server: 
        server.create( dbname ) 
    db = server[dbname]

    if objid in db: 
        obj = db[objid]
    else: 
        obj = { }
    
    # create possible objects that we need to insert
    newobj = _merge_updates( obj, fldkeys, data )

    #pprint(newobj)
    #pprint(obj)

    db[objid] = newobj
    


