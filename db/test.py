#!/usr/bin/env python 

from couchdb.client import Database, Server 

server = Server()
server.resource.credentials = ('socialfarm', 'success')

db = server['socialfarm_public'] 
db.resource.credentials = ('socialfarm', 'success')

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
            'predecessors' : [ 'start' ] , 
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
            'successors' :  [ 'end' ] , 
            'skills_required' :  [] } 




db["iftode"] = { "type" : "person" , 
                 "role" : "partner" , 
                 "name" : "iftode" ,
                 "skills" : [ 's1' , 's2' ] , 
                 "ratings" : [ 0, 1 ] , 
                 'looking_for_work' : 'yes' , 
                 'working_since' : '1-1-2001' 
} 


db["smaldone"] = { "type" : "person" , 
                 "role" : "partner" , 
                 "name" : "smaldone" ,
                 "skills" : [ 's3' , 's2' ] , 
                 "ratings" : [ 0, 1 ] , 
                 'looking_for_work' : 'yes' , 
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
                 'looking_for_work' : 'no' , 
                 'working_since' : '1-1-2001' 
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

#state = start | running | finished | error 
#tasks = ids of tasks
 
# list all the activities in the business
map_fun = '''
function(doc) {
   if (doc.type == "activity" ) { 
      emit(doc._id, null) 
   }
} ''' 
for row in db.query(map_fun):
    print row.key
    row['type'] = 'task' 
    row['state'] = 'start' 
    row['job'] = row.key
    row['_id'] = 'job-001-%s' % row.key 
    print ' added ' , db.copy(row, 'job-001-%s' % row.key ) 



# list all the tasks in the business
map_fun = '''
function(doc) {
   if (doc.type == "task" ) { 
      emit(doc._id, null) 
   }
} ''' 
for row in db.query(map_fun):
    print db[ row.key ] 
