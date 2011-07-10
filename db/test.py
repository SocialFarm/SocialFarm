#!/usr/bin/env python 

from hashlib import md5 
from couchdb.client import Database, Server 
import json 
import sys


server = Server()
server.resource.credentials = ('socialfarm', 'success')
db = server['socialfarm_public'] 




def schedule_tasks() : 
    # assume that number of activities per job is 
    # small enough to be written to a string, but 
    # the total number of new jobs is potentially extremely large 
    # requiring distributed process on map reduce 
    map_fun = '''
function(doc) {
   if (doc.type == "activity" ) { 
      emit(doc._id, doc) 
   }
} ''' 
    startingjob = None 
    predecessors = {} 
    successors = {} 
    skills_required = {} 
    data_items = {} 
    for row in db.query(map_fun): 
        predecessors[ row.key ] = row.value["predecessors"] 
        if predecessors[ row.key ] == [] : 
            startingjob = row.key 
        successors[ row.key ] = row.value["successors"] 
        skills_required[ row.key ] = row.value[ 'skills_required' ] 
        data_items[ row.key ] = row.value[ "data_items" ] 

    map_fun = '''
function(doc) { 
   if (doc.type == "job" && doc.state != "finished" && doc.state != "error" ) {
      emit(doc._id, { "type" : "job" , "rev" : doc._rev } )
   }
   if (doc.type == "task") { 
      emit(doc.jobid, doc) 
   }                             
}                 
'''

    reduce_fun = '''
function(keys, values, rereduce) { 

   function find_successor_task(tasklist) {
      //log ( "start tasklist" ) ; 
      //for ( var i = 0; i < tasklist.length; i++ ) 
      //   log ( "tasklist : " + tasklist[i].activityid + " " + tasklist[i]._id + " " + tasklist[i].jobid) ; 
      //log ( "done tasklist" ) ; 

      successors = %s ; 

      // no tasks with this job, i.e. it is a new job, schedule its first task   
      if (tasklist.length == 0) 
         return [ null, null, "%s" ] ; 

      // ignore jobs that have ongoing or about to run tasks 
      for ( var i = 0; i < tasklist.length; i++ ) {
         task = tasklist[i] ; 
         if ( task.state == "running" ||  task.state == "ready" ) 
            return [ null, null, null ] ; 
      } 

      // the job has only finished tasks, find the new activity that must create task   
      done_tasks = {} 
      for ( var i = 0; i < tasklist.length; i++ ) 
         done_tasks[ tasklist[i].activityid ] = 1 ; 

      for ( var i = 0; i < tasklist.length; i++ ) {
         last_one = 1; 
         for( var succ in successors[tasklist[i].activityid] ) 
            if ( done_tasks[ succ ] )
               last_one = 0; 

         if(last_one) { 
            task = tasklist[i] 
            //log( " last task : " + task.activityid + " " + task._id + " " + task.jobid) ; 
            if ( task.choice ) { 
               return [ task._id, task._rev, task.choice ] ; 
            }
            nsucc = successors[task.activityid].length ;
            if ( nsucc == 1 ) {
               return [ task._id, task._rev, successors[task.activityid][0] ] ; 
            } 
            if ( nsucc == 0 ) {
               return [ task._id, task._rev, null]; 
            }
            else 
               throw( {"Error" : "multiple successor tasks but choice not set" } ) ;
         }
      } 
   }

   if( !rereduce ) {
      currjobrev = null; 
      currjobid = null; 
      prevjobid = null; 
      tasks = [] ;
      new_tasks = [] ;
      for( var i = 0; i < keys.length; i++ ) {
         jobid = keys[i][0] ;        
         doc = values[i] ;
         //log( "jobid = " + jobid ) 

         // do whats needed with this job now 
         if ( prevjobid != undefined && prevjobid != jobid ) { 
            [tid, trev, newactivity] = find_successor_task( tasks ) ;
            if( currjobid != undefined && (newactivity || tid ) )  
               new_tasks.push( [currjobid, currjobrev, tid, trev, newactivity ] ) ;
            tasks = [] 
         } 

         if ( doc.type == "job" ) {
            currjobid = jobid ;
            currjobrev = doc.rev ; 
         } 

         if( doc.type == "task" ) 
            tasks.push( doc ) ; 

         prevjobid = jobid ; 
      }
      [tid, trev, newactivity] = find_successor_task( tasks ) ;
      if( currjobid != undefined && (newactivity || tid ) ) 
         new_tasks.push( [currjobid, currjobrev, tid, trev, newactivity ] ) ; 
      return new_tasks ; 
   }
   else {
      new_tasks = []; 
      while( tasks = values.shift() )  
         new_tasks = new_tasks.concat(tasks) ;
      return new_tasks ; 
   } 
}
''' % (json.dumps(successors) , startingjob) 

    for row in db.query(map_fun, reduce_fun):
        for (jobid, jobrev, prevtid, prevtrev, activityid) in row.value: 
            print jobid, jobrev, prevtid, prevtrev, activityid 
            job = db[jobid] 
               
            if activityid is not None: 
                newtask = { 
                    "type" : "task", 
                    "jobid" : jobid, 
                    "prevtid" : prevtid, 
                    "activityid" : activityid, 
                    "skills_required" : skills_required[activityid] , 
                    "state" : "ready" } 
                taskid = md5( 'task-%s-%s' % (jobid, activityid) ).hexdigest() 
                # first task of new job, gets data items from job
                if prevtid is None: 
                    for f in job[ "data_items" ] : 
                        newtask[f] = job.get( f, None ) 
                else:
                    prev = db[prevtid] 
                    for f in data_items[prev["activityid"]] : 
                        newtask[f] = prev.get( f, None ) 
                db[taskid] = newtask

            if activityid is not None: 
                job[ "state" ] = "running" 
                job[ "taskid" ] = taskid
            else: 
                job[ "state" ] = "finished" 
                job[ "taskid" ] = None 
                
            db[jobid] = job 












def assign_tasks() : 
    map_fun = '''
function(doc) {
   if (doc.type == "task" && doc.state == "ready" ) { 
      for( i = 0 ; i < doc.skills_required.length ; i++ ) {
         emit( [doc.skills_required[i]] , doc._id ) 
      }
   }
   if (doc.type == "person" && doc.looking_for_work == "yes") {
      for( i = 0 ; i < doc.skills.length ; i++ ) {      
         emit( [doc.skills[i], -doc.ratings[i]] , doc._id)
      }
   }
} ''' 

    reduce_fun = '''
function(keys, values, rereduce) { 
   if (!rereduce) {
      var busy_people = {} 
      var people = [] ;  
      var jobs = [] ;
      var prevskill = null ;
      var persons_to_jobs = [] ; 
      for( var i = 0; i < keys.length; i++ ) {
         skill = keys[i][0].shift() ;
         rating = keys[i][0].shift() ; 

         //log( [ "v s r" , values[i], skill, rating ] ) ; 

         if( prevskill && prevskill != skill ) {
            //log("completing skill = " + skill) ;
            //log("people = " + people.toString() ) ;  
            //log("jobs = " + jobs.toString() ) ; 

            // if there are people with the given skill
            // set the association from person to job 
            while( (p = people.shift()) && (j = jobs.shift()) ) {
               log( "adding = " + [p,j,skill] ) 
               persons_to_jobs.push( [p,j,skill] ) ; 
               busy_people[p] = 1;
            }
            people = [] ;  
            jobs = [] ;
         }

         // found the person with given skill, who is not yet assigned  
         if (rating != undefined ) { 
            if (!busy_people[values[i]]) 
               people.push( values[i] ) ; 
         } 
        
         // found a job to be done. 
         else
            jobs.push( values[i] ) ;

         prevskill = skill ; 
      }

      while( (p = people.shift()) && (j = jobs.shift()) ) 
         persons_to_jobs.push( [p,j,skill] ) ; 

      return persons_to_jobs;
   }

   // rereduce is true
   else {   
      persons_to_jobs = [] ;
      // notice we have assigned the most skilled workers to outstanding 
      // jobs in each reduce block.  can we at this stage reassign jobs and workers
      // to have a better optimized assignment? at present just append all
      // assignments 
      var busy_people = {} 
      while( assignmentlist = values.shift() )  
         while( ptoj = assignmentlist.shift() ) {
            person = ptoj[0] ; 
            if(busy_people[person])
               continue; 
            persons_to_jobs.push(ptoj) ; 
            busy_people[person] = 1; 
         }
      return persons_to_jobs;
   } 
}
'''
    assignment = [] 
    for row in db.query(map_fun, reduce_fun):
        assignment += row.value 
    return assignment




# general info on db 
print db.info() 


# list all the ids in the db 
map_fun = '''
function(doc) {
   emit(doc._id, null) 
} ''' 
for row in db.query(map_fun):
    print row.key
    print db.get(row.key) 


# temp test 
del server['socialfarm_private'] 

server.create('socialfarm_private')

db = server['socialfarm_private'] 


# tasks with some dependencies 
db["A"] = { 'type':'activity', 
            'name' : 'Activity A',
            'predecessors' : [ ] , 
            'successors' :  [ 'B' ] , 
            'skills_required' :  [ 's1' ] , 
            'data_items' : [ "name" , "address" ] 
            } 

db["B"] = { 'type':'activity', 
            'name' : 'Activity B',
            'predecessors' : [ 'A' ] , 
            'successors' :  [ 'C' ] , 
            'skills_required' :  [ 's2'] , 
            'data_items' : [ "name" , "height" ] 
            } 

db["C"] = { 'type':'activity', 
            'name' : 'Activity C',
            'predecessors' : [ 'B' ] , 
            'successors' :  [ ] , 
            'skills_required' :  [ 's3' ] , 
            'data_items' : [ "name" , "height" , "weight" ]  } 




db["iftode"] = { "type" : "person" , 
                 "role" : "partner" , 
                 "name" : "iftode" ,
                 "skills" : [ 's1' , 's2' ] , 
                 "ratings" : [ 0, 1 ] , 
                 'looking_for_work' : 'no' , 
                 'working_since' : '1-1-2001' 
} 


db["smaldone"] = { "type" : "person" , 
                 "role" : "partner" , 
                 "name" : "smaldone" ,
                 "skills" : [ 's3' , 's2' ] , 
                 "ratings" : [ 0, 1 ] , 
                 'looking_for_work' : 'no' , 
                 'working_since' : '1-1-2001' 
} 

 

db["vpathak"] = { "type" : "person" , 
                 "role" : "partner" , 
                 "name" : "vpathak" ,
                 "skills" : [ 's1' , 's3' ] , 
                 "ratings" : [ 0, 1 ] , 
                 'looking_for_work' : 'no' , 
                 'working_since' : '1-1-2001' 
} 



db["osteele"] = { "type" : "person" , 
                 "role" : "partner" , 
                 "name" : "osteele" ,
                 "skills" : [ 's1' , 's4' ] , 
                 "ratings" : [ 0, 1 ] , 
                 'looking_for_work' : 'yes' , 
                 'working_since' : '1-1-2011' 
} 





db["guest"] = { "type" : "person" , 
                 "role" : "worker" , 
                 "name" : "guest" ,
                 "skills" : [ 's1' , 's2' , 's3'] , 
                 "ratings" : [ 1, 2, 3 ] , 
                 'looking_for_work' : 'yes' , 
                 'working_since' : '1-1-2001' 
} 




# At this point we have persons, and a business definition (still 
# need to do profit and repo distr though 


db['job-001'] = { "type" : "job" , 
                  "started_since" : "7-7-2011", 
                  "customer" :  "dalai lama" , 
                  "state" : "start" , 
                  "price" : 1.00 , 
                  "total_rating" : 0.00 , 
                  'data_items' : [ "name" ,  "address" , "height" , "weight" ] } 

db['job-002'] = { "type" : "job" , 
                  "started_since" : "7-7-2011", 
                  "customer" :  "cust 2" , 
                  "state" : "start" , 
                  "price" : 1.50 , 
                  "total_rating" : 0.00 , 
                  'data_items' :  [ "name" , "address" , "height" , "weight" ] } 

db['job-003'] = { "type" : "job" , 
                  "started_since" : "7-7-2011", 
                  "customer" :  "cust 3" , 
                  "state" : "start" , 
                  "price" : 1.20 , 
                  "total_rating" : 0.00 , 
                  'data_items' :  [ "name" , "address" , "height" , "weight" ] } 



while True: 
    schedule_tasks()
    assignment = assign_tasks() 
    print 'Created work assignment from map reduce\n' , assignment
    for (worker, task, skill) in assignment: 
        # in real run, here the worker should get the message saying 
        # task is available.  if he accepts, he become unavailable by 
        # the field looking for work and the task gets the worker field 
        # assigned.   
        # Q : what happens if he rejects or does not accept for a while 
        # remember the task is still ready and perhaps another worker 
        # will pick it up 
        print worker, task, skill 
        # simulatign worker did the task 
        t = db[task] 
        t["state"] = "finished" 
        db[task] = t 
     







sys.exit()




 
print '''list all the activities in the business''' 
map_fun = '''
function(doc) {
   if (doc.type == "activity" ) { 
      emit(doc._id, null) 
   }
} ''' 
for row in db.query(map_fun):
    key = row.key
    data = db[key] 
    data['type'] = 'task' 
    if data['predecessors'] == [] : 
        data['state'] = 'ready' 
    else:
        data['state'] = 'waiting' 
        
    data['job'] = key
    del data['_id'] 
    db[ 'job-001-%s' % key ] = data 
    print ' added ' , db.get(  'job-001-%s' % key ) 
    #print ' added ' , db.copy(data, 'job-001-%s' % row.key ) 






print '''list all the tasks in the business''' 

map_fun = '''
function(doc) {
   if (doc.type == "task" ) { 
      emit(doc._id, null) 
   }
} ''' 
for row in db.query(map_fun):
    print db[ row.key ] 
