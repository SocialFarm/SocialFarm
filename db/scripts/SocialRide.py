#TODO Keeping it for future use
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

    members = {
        "Rona_Burgundy" : {
            "skills": ['driving']
        },
        "Briana_Fantana" : {
            "skills": ['driving']
        },
    }

    busdef = {
        'author': 'Prerak_Jain',
        'list_of_partners' : [p for p in members.keys() if 'editing' in members[p]['skills'] ] ,
        'activity_graph' : {'Pick-Up' : ['Drop'] , 'Drop' : [] } , 
        'activity_dataitems' : {
            'Pick-Up' : [ 'pickUp', 'Date','Time','Destination','Gender','Language'] , 
            'Drop' : [ 'Destination', 'Duration'] ,  
            } , 
        'activity_skills' : { 
            'Pick-Up' : [ 'driving' ] ,
			'Drop' : [],
            } ,
        'additional_info' : ['has_a_car', 'gender', 'smocking','car_capicity'], 
        'description' : 'social_ride ' 
        }
    sf.deleteBusiness( 'social_ride' ) 
    sf.createBusiness( 'social_ride' , busdef ) 

    
    bd = BusinessDirector('social_ride' , username, password ) 


    data_items = {
        'pickUp' : 'Airport' , 
        'Date' : '12-Aug-2012',
        'Time' : '21:00',
        'Destination' : 'Railway Station',
        'Gender' : 'Male',
        'Language' : 'English, Hindi',
    }

    bd.createJob( 'Prerak' , 1 , data_items ) 


    
    for m in members.keys():
        sf.addPerson(m)
        bd.addWorker(m,members[m]['skills']) 



