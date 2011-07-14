import couchdb, simplejson

from pyramid import request, renderers 
from pyramid.httpexceptions import HTTPFound
from pyramid.url import route_url

from pyramid_handlers import action

from social_farm.handlers.base import BaseHandler
from social_farm.lib.SocialFarmHelper import SocialFarm, BusinessDirector
from social_farm.lib import facebook

class FacebookHandler(BaseHandler):
 
    def __init__(self, request):
        super(FacebookHandler, self).__init__(request)
        self.c.user = None
        if request.params.has_key('session'):
            access_token = simplejson.loads(request.params['session'])['access_token']
            graph = facebook.GraphAPI(access_token)
            self.c.user = graph.get_object("me")
        self.template_vars['title'] = 'FacebookHandler'
        self.template_vars['FACEBOOK_APP_ID']       = '234690403213067'
        self.template_vars['FACEBOOK_API_KEY']      = '7165704a80616d58e50629512349a8c1'
        self.template_vars['FACEBOOK_APi_SECRET']   = '14a74c4bcf2537f42d714c5cd8324c6e'
        self.template_vars['FACEBOOK_CALLBACK_URL'] = 'http://apps.facebook.com/social_farm/'

    @action(renderer="facebook/oauth_redirect.mak")
    def login(self):
        if not self.c.user:
            return self.template_vars
        return HTTPFound(location = route_url('facebook', self.request, action="index", id=None))

    @action(renderer="facebook/facebook.mak")
    def index(self):
        return self.template_vars

    @action(renderer="facebook/facebook.mak")
    def create(self):
        return self.template_vars


""" #be sure port forwarding is working
    @action(renderer="facebook.mak")
    def test(self):
        username = 'socialfarm'
        password = 'success'
        sf = SocialFarm(username, password)
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
                'A' : [ 's1' ] , 
                'B' : [ 's3' ] , 
                'C' : [ 's4' ] , 
                'D' : [ 's2' ] 
                } , 
            'description' : 'This business will find out your true reputation for a small fee!' 
            }
        sf.deleteBusiness( 'testbus' ) 
        sf.createBusiness( 'testbus' , busdef ) 

        
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

        return self.template_vars
"""

