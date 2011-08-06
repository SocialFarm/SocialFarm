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

    print 'creating business social_news' 
    busdef = {
        'author': '1479360134',
        'list_of_partners' : [ 'vpathak' , '1479360134' ] ,
        'activity_graph' : {'Research' : ['Write'] , 'Write' : ['Edit'], 'Edit' : [] } , 
        'activity_dataitems' : {
            'Research' : [ 'name' , 'sources' ] , 
            'Write' : [ 'name' , 'sources' , 'article' ] , 
            'Edit' : [ 'name' , 'sources' , 'article'  ] , 
            } , 
        'activity_skills' : { 
            'Research' : [ 'researching' ] , 
            'Write' : [ 'writing' ] , 
            'Edit' : [ 'editing' ] , 
            } , 
        'description' : 'social_news is a virtual new business designed to showcase the social farm platform.' 
        }
    sf.deleteBusiness( 'social_news' ) 
    sf.createBusiness( 'social_news' , busdef ) 

    
    bd = BusinessDirector( 'social_news' , username, password ) 

    bd.createJob( 'customer_x' , 1.0 , {
            'name' : '1479360134' , 
            'profession' : 'student; technologist' 
            } ) 
    bd.addWorker('vpathak', ['researching','writing','editing'] , 'partner' ) 
    bd.addWorker('1479360134', ['writing','researching'] )    

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



