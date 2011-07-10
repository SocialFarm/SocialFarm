#!/usr/bin/env python 
# Helper application for managing documents in the 
# social farm database.  Documents should be created 
# through this class in order to enforce the integrity 
# of the database 


SOCIALFARM_PUBLIC_DB = 'socialfarm'
SOCIALFARM_BUSINESS_TEMPLATE_DB = 'socialfarm_business_template'

import json 
import time 
from hashlib import md5 
from pprint import pprint 
from couchdb.client import Database, Server 
from couchdb.mapping import TextField, IntegerField, DateField, FloatField 




class SocialFarm : 
    
    def __init__(self, username, password, url ='http://localhost:5984/'): 
        self.server = Server(url)
        if username is not None and password is not None: 
            self.server.resource.credentials = (username, password) 
        self.db = self.server[SOCIALFARM_PUBLIC_DB] 


    def listids(self): 
        return [ row.key for row in self.db.view('_all_docs') ] 
            
        
    def getBusiness(self, businessname): 
        self.busdef = self.db[ businessname ] 
        self.__process_business(self.busdef) 
        return self.busdef 


    def updateBusiness(self, businessname, busdef ): 
        self.db[ businessname ] = busdef  
        self.__process_business(self.busdef) 
        self.busdef = busdef 


    def deleteBusiness(self, businessname) :
        del self.db[ businessname ] 
        del self.server[ businessname ] 


    def createBusiness(self, businessname, busdef):  
        if businessname != businessname.lower(): 
            raise Exception( 'businessname must be lower case with no spaces' ) 
        if businessname in self.server : 
            raise Exception( 'businessname already taken' ) 

        for k in [ 'author',
                   'list_of_partners',
                   'activity_graph' , 
                   'activity_dataitems' , 
                   'activity_skills' , 
                   'description' ] : 
            assert k in busdef

        busdef[ 'type' ] = 'business' 
        busdef[ 'started_since' ] = time.time() 
        busdef[ 'total_rating' ] = 0 
        busdef[ 'total_profit' ] = 0

        self.__process_business(busdef) 
        self.db[ businessname ] = busdef  
        self.busdef = busdef 
        
        # created new database for business info 
        busdb = self.server.create(businessname)
        
        # copy the application code from template db 
        self.server.replicate( SOCIALFARM_BUSINESS_TEMPLATE_DB, 
                               businessname ) 

        # write activity documents that are used as template for 
        # tasks within jobs 
        for task in self.alltasks: 
            activitydef = {} 
            activitydef[ 'type' ] = 'activity' 
            activitydef[ 'name' ] = task 
            activitydef[ 'data_items'] = self.busdef['activity_dataitems'][task]
            activitydef[ 'predecessors' ] = self.predecessors[task] 
            activitydef[ 'successors' ] = self.successors[task] 
            activitydef[ 'skills_required' ] = self.busdef[ 'activity_skills' ][task] 
            busdb[ task ] = activitydef



        

    def __process_business(self, busdef) :
        alltasks = [] 
        successors = {} 
        predecessors = {} 
        for task in busdef['activity_graph'].keys() :
            alltasks.append( task ) 
            successors[task] = busdef['activity_graph'][task] 
            predecessors[task] = [] 
        #pprint( alltasks ) 
        #pprint( successors ) 

        for task in busdef['activity_graph'].keys() :
            for succ in successors[task]: 
                predecessors[succ].append(task) 
        #pprint( predecessors ) 
    
        # validate the task definition
        # only one task is starting task with no predecessors 
        numstart = 0         
        for task in busdef['activity_graph'].keys() :
            if len(predecessors[task]) == 0 : 
                numstart += 1 
        assert( numstart == 1 )
 
        self.successors = successors
        self.predecessors = predecessors
        self.alltasks = alltasks 

        




class BusinessDirector : 

    def __init__(self, businessname, username, password, url ='http://localhost:5984/'): 
        self.server = Server(url)
        if username is not None and password is not None: 
            self.server.resource.credentials = (username, password) 
        self.db = self.server[businessname]         


    def createJob(self, customer, price, data_items) : 
        ### TODO ### 
        jobdef = { 
            'type' : 'job' ,
            'started_since' : time.time() , 
            'customer' : customer , 
            'price' : price , 
            'total_rating' : 0 , 
            'data_items' : data_items 
            } 
        





if __name__ == "__main__": 
    import sys 
    
    if len(sys.argv) == 0:
        print "Usage : %s <user> <pwd> [<couchdb url>]"
        sys.exit(-2) 

    username = sys.argv[1] 
    password = sys.argv[2] 
    if len(sys.argv) == 3: 
        sf = SocialFarm(username, password)
    else: 
        sf = SocialFarm(username, password, sys.argv[3] )

    print 'created social farm object' 

    print 'creating business testbus' 

    busdef = {
        'author': 'vpathak',
        'list_of_partners' : [ 'vpathak' , 'osteele' ] ,
        'activity_graph' : {'A' : ['B'] , 'B' : ['C'], 'C' : ['D'] , 'D' : [] } , 
        'activity_dataitems' : {
            'A' : [ 'name' , 'profession' ] , 
            'B' : [ 'name' , 'profession' , 'level' ] , 
            'C' : [ 'name' , 'colleagues' ] , 
            'D' : [ 'name' , 'colleagues' , 'reputation' ] 
            } , 
        'activity_skills' : { 
            'A' : [ 's1' , 's2' ] , 
            'B' : [ 's3' ] , 
            'C' : [ 's3' ] , 
            'D' : [ 's1' , 's3' ] 
            } , 
        'description' : 'This business will find out your true reputation for a small fee!' 
        }
    sf.deleteBusiness( 'testbus' ) 
    sf.createBusiness( 'testbus' , busdef ) 

    
