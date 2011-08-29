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
        "Ron_Burgundy" : {
            "skills": ['writing', 'researching']
        },
        "Brian_Fantana" : {
            "skills": ['writing']
        },
        "Veronica_Corningstone" : {
            "skills": ['writing', 'editing', 'researching']
        },
        "Brick_Tamland" : {
            "skills": []
        },
        "Champ_Kind" : {
            "skills": ['writing', 'researching']
        },
        "Ed_Harkin" : {
            "skills": ['editing']
        },
        "Garth_Holiday" : {
            "skills": ['writing']
        },
    }

    busdef = {
        'author': 'Ron_Burgundy',
        'list_of_partners' : [p for p in members.keys() if 'editing' in members[p]['skills'] ] ,
        'activity_graph' : {'Research' : ['Write'] , 'Write' : ['Edit'], 'Edit' : [] } , 
        'activity_dataitems' : {
            'Research' : [ 'title', 'request_description', 'primary_sources'] , 
            'Write' : [ 'title', 'request_description',  'primary_sources' , 'article_content' ] , 
            'Edit' : [ 'title', 'request_description',  'primary_sources' , 'article_content'  ] , 
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

    
    bd = BusinessDirector('social_news' , username, password ) 

    """ potenial primary source
    http://www.nydailynews.com/lifestyle/pets/galleries/whos_the_cutest_in_the_animal_kingdom/whos_the_cutest_in_the_animal_kingdom.html

    """
    data_items = {
        'title' : 'The Cutest Pets in San Diego' , 
        'request_description' : 'Write us an aritcle about cute pets, we will pay you $1.',
        "primary_sources" : "",
    }

    bd.createJob( 'Network_News' , 1 , data_items ) 


    
    for m in members.keys():
        sf.addPerson(m)
        bd.addWorker(m,members[m]['skills']) 



