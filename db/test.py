#!/usr/bin/env python 

from couchdb.client import Database, Server 
import sys


server = Server()
server.resource.credentials = ('socialfarm', 'success')

db = server['socialfarm_public'] 
db.resource.credentials = ('socialfarm', 'success')



def process_new_jobs() : 
    # assume that number of activities per job is 
    # small enough to be written to a string, but 
    # the total number of new jobs is potentially extremely large 

    # get all activities that need to be done for a job
    newjobs = [] 
    # get the jobids 
    map_jobs = '''
function(doc) { 
   if (doc.type == "job" && 
      doc.state != "finished" && doc.state != "error" ) {
      emit(doc._id, doc)
   }
} 
'''
    for row in db.query( map_jobs ) :
        #print 'got job' , row.key 
        newjobs.append( row.key ) 

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
        del data['_id'] 
        
        for job in newjobs: 
            taskid = 'job-%s-%s' % (job, key)
            data['job'] = key
            db[taskid] = data 
            #print ' added ' , db.get(taskid) 








def schedule() : 
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
            //log(people) ;  
            //log(jobs) ; 
            // if there are people with the given skill
            // set the association from person to job 
            while( (p = people.shift()) && (j = jobs.shift()) ) {
               persons_to_jobs.push( [p,j,skill] ) ; 
               busy_people[p] = 1;
            }
            people = [] ;  
            jobs = [] ;
         }

         // found the person with given skill, who is not yet assigned  
         if (rating != undefined && (!busy_people[values[i]]) ) 
            people.push( values[i] ) ; 

        
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
            'skills_required' :  [ 's1' ] } 

db["B"] = { 'type':'activity', 
            'name' : 'Activity B',
            'predecessors' : [ 'A' ] , 
            'successors' :  [ 'C' ] , 
            'skills_required' :  [ 's2'] } 

db["C"] = { 'type':'activity', 
            'name' : 'Activity C',
            'predecessors' : [ 'B' ] , 
            'successors' :  [ ] , 
            'skills_required' :  [] } 




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
                  "total_rating" : 0.00 } 

db['job-002'] = { "type" : "job" , 
                  "started_since" : "7-7-2011", 
                  "customer" :  "cust 2" , 
                  "state" : "start" , 
                  "price" : 1.50 , 
                  "total_rating" : 0.00 } 

db['job-003'] = { "type" : "job" , 
                  "started_since" : "7-7-2011", 
                  "customer" :  "cust 3" , 
                  "state" : "start" , 
                  "price" : 1.20 , 
                  "total_rating" : 0.00 } 


#state = start | running | finished | error 
#tasks = ids of tasks
process_new_jobs()





print '''create design doc i.e. program for selecting workers''' 



assignment = schedule() 
print 'Created work assignment from map reduce\n' , assignment 






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
