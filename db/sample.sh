#!/bin/bash 



# create a few businesses 
# note that id should be computed by the program through md5 of 
# identifying data, here we use small numbers just to show 

curl --user socialfarm:success -X PUT http://127.0.0.1:5984/socialfarm_public/b11111 -d '{ "type":"business", "author":"vpathak", "description" : "this business aims to start new businesses" , "list_of_partners": ["iftode","vpathak","smaldone","osteele"], "started_since":"7-7-2011", "list_of_roles": ["role1", "role2", "role3"], "total_rating":0.0, "total_profit":0.0}' 


curl --user socialfarm:success -X PUT http://127.0.0.1:5984/socialfarm_public/b22222 -d '{ "type":"business", "author":"vpathak", "description" : "this business aims to do nothing" , "list_of_partners": ["iftode","vpathak","smaldone","osteele"], "started_since":"7-7-2011", "list_of_roles": ["role0"], "total_rating":0.0, "total_profit":0.0}' 


# display all the businesses we have 
curl -X GET http://127.0.0.1:5984/socialfarm_public/_all_docs



# get a list of scheduled actions from scheduler 
curl --user socialfarm:success -X GET http://127.0.0.1:5984/socialfarm_private/_design/scheduler
