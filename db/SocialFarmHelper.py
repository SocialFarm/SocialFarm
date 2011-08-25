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
import couchdb 
from couchdb.client import Database, Server





class SocialFarm : 
    
    def __init__(self, username, password, url ='http://localhost:5984/'): 
        self.server = Server(url)
        if username is not None and password is not None: 
            self.server.resource.credentials = (username, password) 
        self.db = self.server[SOCIALFARM_PUBLIC_DB] 


    def listids(self): 
        return [ row.key for row in self.db.view('_all_docs') ] 

    
    def addPerson(self, pid, datadict = {}, overwrite = False ): 
        now = time.time() 
        if overwrite : 
            del self.db[pid] 
        #else:
            #workerdef = self.db[ pid ]
        workerdef = {}
        workerdef[ 'type' ] = 'person'
        workerdef[ 'added' ] = now  
        for k in datadict: 
            workerdef[ k ] = datadict[ k ] 
        self.db[ pid ] = workerdef 
        

    def getBusiness(self, businessname): 
        self.busdef = self.db[ businessname ] 
        self.__process_business(self.busdef) 
        return self.busdef 


    def updateBusiness(self, businessname, busdef ): 
        self.db[ businessname ] = busdef  
        self.__process_business(self.busdef) 
        self.busdef = busdef 


    def deleteBusiness(self, businessname) :
        if businessname in self.db:
            del self.db[ businessname ] 
        if businessname in self.server:
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
        self.businessname = businessname
        self.sf = SocialFarm(username, password) 
        self.server = Server(url)
        if username is not None and password is not None: 
            self.server.resource.credentials = (username, password) 
        self.db = self.server[businessname]         
        for row in self.db.view( 'info/get_start_action' ): 
            self.start_action = row.value 
        #pprint(self.start_action) 



    def createJob(self, customer, price, data_items) : 
        print "Creating job!!" 
        ''' create new records for the job and the 
        first task of the job; add them to db in the 
        ready state, to be picked up by scheduler '''
        now = time.time() 
        jobdef = { 
            'type' : 'job' ,
            'started_since' : now , 
            'customer' : customer , 
            'price' : price , 
            'total_rating' : 0 , 
            'data_items' : data_items , 
            'state' : 'ready'
            } 
        jobid = "job." + md5( '%s.%d' % (customer, int(now) ) ).hexdigest() 
   
        for k in self.start_action['data_items']: 
            assert k in data_items 

        (taskid, taskdef) = self.__getTask( jobid, 
                                            self.start_action, 
                                            data_items ) 
        self.db[ jobid ] = jobdef 
        self.db[ taskid ] = taskdef 
        


    def __getTask(self, jobid, activity, data_items): 
        activityid = activity['_id']  
        activity_data_items = {} 

        for k in activity['data_items']: 
            activity_data_items[k] = None 

        for k in data_items:
            activity_data_items[k] = data_items[k] 

        taskdef = { 
            'type' : 'task' , 
            'jobid' : jobid , 
            'activityid' : activityid ,
            'data_items' : activity_data_items, 
            'worker' : None, 
            'state' : 'ready', 
            'successors' : activity["successors"] , 
            'skills_required' : activity['skills_required'],
            'choice' : None 
            }
        taskid = 'task.%s.%s' % (activityid, jobid)
        return (taskid,  taskdef) 




    def addWorker(self, name, skills, role = 'worker', looking = True) : 
        looking_for_work = 'no' 
        if looking : 
            looking_for_work = 'yes' 
        assert role is "worker" or role is "partner" 

        now = time.time() 
        workerdef = {
            'type' : 'person' , 
            'role' : role, 
            'skills' : skills, 
            'ratings' : [ 0.0 for s in skills ] , 
            'looking_for_work' : looking_for_work , 
            'working_since' : now 
            } 
        self.db[ name ] = workerdef 
        
        persondef = self.sf.db[name] 
        if 'businesses' not in persondef : 
            persondef[ 'businesses' ] = [ self.businessname ] 
        else :
            persondef[ 'businesses' ].append( self.businessname ) 
        self.sf.db[name] = persondef
        

    def delWorker(self, name): 
        del self.db[ name ]
        persondef = self.sf.db[name] 
        persondef[ 'businesses' ].remove( self.businessname ) 
        self.sf.db[name] = persondef
        



    def taskOffers(self): 
        for row in self.db.view( 'scheduler/offer_tasks' ) : 
            return row.value 


    def handleCompletion(self): 
        newtasks = [] 

        for row in self.db.view( 'scheduler/pending_jobs_tasks' ) : 
            jobs_tasks = row.value 
            break

        for (jobid, tasklist) in jobs_tasks:
            #pprint ( jobid ) 
            #pprint ( [ t['_id'] for t in tasklist ] ) 
            if not jobid : # job is marked finished , todo: cleanup its tasks 
                continue   
            
            completed = {} 
            ongoing = None 
            for t in tasklist: 
                if t['state'] == 'finished' : 
                    completed[ t['activityid'] ] = t 
                elif t['state'] == 'running' or t['state'] == 'ready':
                    ongoing = t 
                    break 
            if ongoing:  # some task runs, nothing to do
                continue 

            aid = self.start_action["_id"] 
            # first job is niether started nor finished 
            if aid not in completed: 
                (taskid, taskdef) = self.__getTask( jobid, 
                                                    self.start_action, 
                                                    self.db[jobid]['data_items'] ) 
                self.db[ taskid ] = taskdef 
                newtasks.append( taskid ) 
                continue 
                
            while True: 
                # reached end , job is complete ! 
                if len(completed[aid]['successors']) == 0: 
                    jobdef = self.db[jobid] 
                    jobdef[ 'state' ] = 'finished' 
                    for k in completed[aid]['data_items'].keys() : 
                        if jobdef[ 'data_items' ].has_key(k): 
                            jobdef[ 'data_items' ][k] = completed[aid]['data_items'][k]
                    self.db[jobid] = jobdef
                    break 

                if len(completed[aid]['successors']) == 1:
                    nextaid = completed[aid]['successors'][0] 
                        
                elif completed[aid].has_key('choice') : 
                    nextaid = completed[aid]['choice'] 

                else: 
                    raise Exception( 'many successors and no choice! %s:%s' % (jobid, aid) )

                # found next action that has to be run 
                if nextaid not in completed: 
                    activitydef = self.db[nextaid] 
                    (taskid, taskdef) = self.__getTask( jobid, 
                                                        activitydef, 
                                                        completed[aid]['data_items'] ) 
                    self.db[ taskid ] = taskdef 
                    newtasks.append( taskid ) 
                    break 

                aid = nextaid 

        return newtasks 


                        


            
                
                
            
        



if __name__ == "__main__": 
    import sys 
    
    if len(sys.argv) == 1:
        print "Usage : %s <user> <pwd> [<couchdb url>]"
        sys.exit(-2) 

    username = sys.argv[1] 
    password = sys.argv[2] 
    if len(sys.argv) == 3: 
        sf = SocialFarm(username, password)
    else: 
        sf = SocialFarm(username, password, sys.argv[3] )

    print 'created social farm object' 

    print 'added persons to social farm db ' 
    sf.addPerson( 'osteele' ) 
    sf.addPerson( 'vpathak' ) 


    print 'creating business testbus2' 
    busdef = {
        'author': 'vpathak',
        'list_of_partners' : [ 'vpathak'  ] ,
        'activity_graph' : {'A' : ['B'] , 'B' : ['C'], 'C' : [] } , 
        'activity_dataitems' : {
            'A' : [ 'name' , 'profession' ] , 
            'B' : [ 'name' , 'profession' , 'level' ] , 
            'C' : [ 'name' , 'colleagues' ] 
            } , 
        'activity_skills' : { 
            'A' : [ 's1' ] , 
            'B' : [ 's3' ] , 
            'C' : [ 's1' ] 
            } , 
        'description' : 'This business is a test ' 
        }
    sf.deleteBusiness( 'testbus2' ) 
    sf.createBusiness( 'testbus2' , busdef ) 


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
            'A' : [ 's1' ] , 
            'B' : [ 's3' ] , 
            'C' : [ 's4' ] , 
            'D' : [ 's2' ] 
            } , 
        'description' : 'This business will find out your true reputation for a small fee!' 
        }
    sf.deleteBusiness( 'testbus' ) 
    sf.createBusiness( 'testbus' , busdef ) 

    bd = BusinessDirector( 'testbus2' , username, password ) 
    bd.createJob( 'dalai lama' , 1.00 , {
	        'name' : 'vivek pathak' , 
	        'profession' : 'professor; technologist' 
	        } ) 
    bd.createJob( 'pope' , 1.10 , {
	        'name' : 'osteele' , 
	        'profession' : 'student; technologist' 
	        } ) 
    bd.addWorker('vpathak', ['s1','s3','s4'] , 'partner' ) 
    bd.addWorker('osteele', ['s1','s2','s4'] )  


    bd = BusinessDirector( 'testbus' , username, password ) 
    bd.createJob( 'dalai lama' , 1.00 , {
	        'name' : 'vivek pathak' , 
	        'profession' : 'professor; technologist' 
	        } ) 
    bd.createJob( 'pope' , 1.10 , {
	        'name' : 'osteele' , 
	        'profession' : 'student; technologist' 
	        } ) 
    bd.addWorker('vpathak', ['s1','s3','s4'] , 'partner' ) 
    bd.addWorker('osteele', ['s1','s2','s4'] )  
  

    print 'calculating task offers' 

    
    # at this stage a real business would allow workers to 
    # accept the task.  the task would get the worker and 
    # and state changed to running, and the worker would be 
    # not looking for work for a while (until task completes). 
    # here we just complete the task immediately 
    for i in range(1,10): 
        for (workerid, taskid) in bd.taskOffers() :
            print 'offer' , workerid , taskid 
            tdef = bd.db[ taskid ] 
            tdef[ 'worker' ] = workerid
            tdef[ 'state' ] = 'finished' 
            bd.db[ taskid ] = tdef 
    
        print 'check completion, spawn new if needed'
        try:
            print 'new tasks : ' , repr( bd.handleCompletion() ) 
        except couchdb.http.ResourceConflict : 
            bd.db.commit() 



