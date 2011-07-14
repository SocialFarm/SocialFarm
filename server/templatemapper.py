#!/usr/bin/env python 

from pprint import pprint 
import re 


class templatemapper: 

    def __init__(self, src, tgt): 
        self.src = src 
        self.tgt = tgt 
        self.srclist = src.split('/') 
        self.tgtlist = tgt.split('/') 
        self.srctemplates = self.__get_templates( self.srclist ) 
        self.tgttemplates = self.__get_templates( self.tgtlist ) 



    def __get_templates(self, pathcomplist) :
        # TODO: It would be best if components could be extracted without
        # assuming that the served url must have at most one template arg per 
        # path component - see ___todo___
        pathtemplates = {} 
        i = 0
        for pathcomp in pathcomplist: 
            if len(pathcomp) > 2 and pathcomp[0] == '{' and pathcomp[-1] == '}' :
                pathtemplates[ pathcomp[1:-1] ] = i 
            i += 1 
        return pathtemplates


    def ___todo___(TODO): 
        self.srctemplates = {} 
        # these should be the boundaries of the components, regardless of 
        # / in the url.  something like this should go in place of split('/')  
        for m in re.finditer(  r'\{(\w*)\}' , src ) : 
            self.srctemplates[ m.group(1) ] = (m.start(), m.end()) 
            
        self.tgttemplates = {} 
        for m in re.finditer(  r'\{(\w*)\}' , tgt ) : 
            self.tgttemplates[ m.group(1) ] = (m.start(), m.end())             



    def replace(self, url): 
        urlcomps = url.split('/') 
        data = {} 
        for key in self.srctemplates:
            data[ key ] = urlcomps[ self.srctemplates[key] ] 

        res = self.tgt
        for key in data: 
            res = res.replace( '{%s}' % key, data[ key ] ) 
        return res 
            
     
    def matches(self): 
        return True 


if __name__ == '__main__':
    t = templatemapper( '/allbusiness/{startkey}/{count}' , 
                        '/socialfarm/_all_docs/?start_key={startkey}&count={count}' ) 

    print t.replace( '/allbusiness/A/30' ) 

    
            
            
