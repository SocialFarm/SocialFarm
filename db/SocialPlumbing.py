#!/usr/bin/env python

from SocialFarmHelper import SocialFarm, BusinessDirector

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

    print 'creating business social_plumbing' 

    members = {
        "Orie_Steele" : {
            "skills": ['designing', 'researching', 'implementing']
        },
    }

    busdef = {
        'author': 'Orie_Steele',
        'list_of_partners' : [p for p in members.keys() if 'editing' in members[p]['skills'] ] ,
        'activity_graph' : {'Implement' : ['Publish'] , 'Publish' : [] } , 
        'activity_dataitems' : {
            'Implement' : [ 'title', 'request_description', 'feeds', 'pipe_url'] , 
            'Publish' : [ 'title', 'request_description', 'feeds', 'pipe_url' ,
            } , 
        'activity_skills' : { 
            'Implement' : [ 'designing', 'researching' ] , 
            'Publish' : [ 'implementing' ] , 
            } , 
        'description' : 'social_plumbing is a virtual new business designed to for building yahoo pipes.' 
        }
    sf.deleteBusiness( 'social_plumbing' ) 
    sf.createBusiness( 'social_plumbing' , busdef ) 

    
    bd = BusinessDirector('social_plumbing' , username, password ) 

    data_items = {
        'title' : 'Apartment Near Something' , 
        'request_description' : 'I would like to be able to find apartments near something',
        "pipe_url" : "http://pipes.yahoo.com/pipes/pipe.info?_id=1mrlkB232xGjJDdwXqIxGw",
    }

    bd.createJob( 'Confused_Plumber' , 0 , data_items ) 


    
    for m in members.keys():
        sf.addPerson(m)
        bd.addWorker(m,members[m]['skills']) 



