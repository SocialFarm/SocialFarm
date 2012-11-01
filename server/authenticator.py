#!/usr/bin/env python

import urllib 
import json
import time 
from pprint import pprint


MAX_CACHE_STALE_SECS = 10 * 60 




class Authenticator : 

    
    __auth_cache = dict ()     



    def __validateAccessToken(self, fbid, accesstoken) : 
        token, ts = Authenticator.__auth_cache.get( fbid, (None, None) ) 
        if token :
            if (time.time() - ts) < MAX_CACHE_STALE_SECS and token == accesstoken : 
                #print 'cache hit' 
                return True
        try : 
            obj = json.loads(urllib.urlopen( 'https://graph.facebook.com/me?access_token=%s' % accesstoken).read()) 
            #pprint(obj) 
            if fbid == obj['id'] :
                Authenticator.__auth_cache[fbid] = ( accesstoken, time.time() ) 
                return True 
        except KeyError: 
            pass 
        return False 
        




    def canAccess(self, localurl, fbid, accesstoken) : 
        ''' determine if the access to the given socialfarm couchdb url 
        should be allowed and if yes validate the user with facebook graph api ''' 
        # trivial accesses allowed
        if localurl[-3:] == '.js' : 
            return True 
        if localurl[-4:] == '.css' :
            return True 
        if localurl == "/" : 
            return True
        # user allowed to access the object ? 
        return self.__validateAccessToken(fbid, accesstoken) 







if __name__ == '__main__':
    ''' test case ''' 
    auth = Authenticator() 
    print auth.canAccess ( "XXX" , 
                           "100000007289310" , 
                           "ACCESS_TOKEN" )

