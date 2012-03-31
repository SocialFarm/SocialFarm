#!/usr/bin/env python 

# Manage attachments associated with a document in couchdb 


import os, sys, getopt, os.path 
from pprint import pprint 
from couchdb.client import Database, Server 
import mimetypes 


def _usage() :
    print 'Usage : %s --help' % sys.argv[0] 
    print 'Usage : %s [-l <username:password>] [-u <couchdburl>] <dbname> <docid> <attachmentname> [<contentfilename>]' % sys.argv[0]
    print 'without contentfile, the command will download the attachment and save it in the localdirectory' 
    print 'with the contentfile name provided, the contents of the file will be uploaded into the given attachment' 
    sys.exit(-1) 




if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:] , 'l:u:h' , ["login" , "url" , "help"])
    except getopt.GetoptError, err:
        print str(err) 
        _usage()
   
    # TODO : This code is common with the update field script.  move to common script? 
    
    url = 'http://localhost:5984/'
    for o, a in opts:
        if o in ("--login" , "-l") :
            username, password = a.split(':') 
        if o in ("--url" , "-u") :
            url = a
        if o in ("--help" , "-h" ) :
            _usage() 

    if 'SF_USERNAME' in os.environ.keys():
        username = os.environ['SF_USERNAME']
        password = os.environ['SF_PASSWORD']
    else:
        if username == None or password == None:
            raise Exception("Invalid CREDENTIALS!")
   

    server = Server(url)
    if username: 
        server.resource.credentials = (username, password)


    dbname = args[0]
    docid  = args[1]
    attachmentname = args[2]
    db = server[dbname]
    assert docid in db 
    doc = db[docid] 
    if len(args) == 4: 
        # puttig attachment 
        # TODO : use codecs.EncodedFile( fd, ... , errors = "ignore" ) 
        data = open(args[3]).read()
        db.put_attachment( doc, data, attachmentname, content_type=mimetypes.guess_type(attachmentname)[0] )
    else :
        if os.path.isfile(attachmentname) : 
            # error if file exists 
            raise Exception( 'file %s exists' % attachmentname ) 
        wfd = open( attachmentname , "w" ) 
        rfd = db.get_attachment(doc, attachmentname)
        if rfd is not None: 
            wfd.write( rfd.read() ) 
        else: 
            raise Exception( 'document %s doesnt have attachment %s ' % (docid, attachmentname) )
        


