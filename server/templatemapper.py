#!/usr/bin/env python 


from pprint import pprint 
from collections import namedtuple 
import re 


Literal = namedtuple( 'Literal' , 'path' ) 
Variable = namedtuple( 'Variable' , 'name' ) 


class templatemapper: 


    def __init__(self, src, tgt): 
        self.src = src 
        self.tgt = tgt 
        (_, self.tgttemplate)  = self.__get_templates( self.tgt ) 
        (self.srcregexstr, self.srctemplate) = self.__get_templates( self.src ) 
        self.srcregex = re.compile(self.srcregexstr)  


    def __get_templates(self, path) :
        boundaries = [] 
        for m in re.finditer(  r'\{(\w*)\}' , path ) : 
            boundaries.append( (m.start(), m.end(), m.group(1)) ) 

        regex = '^'         
        template = [] 
        prevend = 0
        for (start, end, varname) in boundaries: 
            if start != end: 
                template.append( Literal( path[prevend:start] ) )  
                template.append( Variable( varname ) )
                regex += re.escape( path[prevend:start] )  
                regex += '(\w*)' 
                prevend = end
        
        if prevend != len(path): 
            template.append( Literal( path[prevend:len(path)] ) ) 
            regex += re.escape( path[prevend:start] )       
        
        regex += '$' 

        return (regex, template) 




    def replace(self, url): 
        m = self.srcregex.match(url)
        if m is None:
            raise Exception( '%s does not match pattern %s' % (url, self.src) ) 

        # get the matches for each variable according to regex match
        i = 1
        matches = {} 
        for obj in self.srctemplate: 
            if type(obj) is Variable:
                matches [ obj[0] ] = m.group(i) 
                i += 1


        reslist = []
        for obj in self.tgttemplate: 
            if type(obj) is Literal: 
                reslist.append( obj[0] )
            else:
                reslist.append( matches[ obj[0] ] ) 

        return ''.join(reslist) 


     
    def matches(self, url): 
        if self.srcregex.match(url) :
            return True 
        return False




if __name__ == '__main__':
    t = templatemapper( '/allbusiness/{startkey}/{count}' , 
                        '/socialfarm/_all_docs/?start_key={startkey}&count={count}' ) 

    print t.replace( '/allbusiness/A/30' ) 

    
            
            
