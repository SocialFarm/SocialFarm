
/**
 * Purpose of this function is to validate changes to various type of 
 * objects in the social farm business databases.  It is currently used only 
 * for validating updates to business databases - this is done by 
 * populating this in the business_template database which is used
 * as source for creating new databases  
 *
 * TODO / NOTES 
 *
 * Idea for refactoring (code directory organization) 
 * 1 Perhaps the validation should be closer to 
 * the business and objects.  
 *
 * 2 As it is done now, gives a top down approach 
 * for validation.  Whenever a new fld is added to say activity or task or 
 * job or person, this file will always change - creating a maintainenace
 * problem (but can couchdb support multiple valids? Check) 
 */  

function( newdoc, olddoc, uxt ) 
{ 
    // helper functions 
    function belongs( myitem, listofitems ) { 
        if( listofitems.indexOf(myitem) < 0 ) 
            return false; 
        return true; 
    }; 

    function require(field, message) {
        message = message || "Document must have a : " + field;
        if (!newdoc[field]) throw({forbidden : message});
    };

    function unchanged(field) {
        if (olddoc && toJSON(olddoc[field]) != toJSON(newdoc[field]))
            throw({forbidden : "Field can't be changed : " + field});
    }

    
    // actual validation begins here  
    require( "type" ) ;

    if( ! belongs( newdoc.type , [ "activity" , "job" , "template" , "task" , "person" ] ) ) 
        throw ( {forbidden : "type not allowed : " +  newdoc.type } ) ; 
  

    unchanged( "type" ) ; 


    if( newdoc.type == 'task' ) 
    { 
        if ( !belongs( newdoc.state , [ "ready" , "running", "finished" , "error" ] ) ) 
            throw ( {forbidden : "state not allowed : " +  newdoc.state } ) ; 

        require( "jobid" ) ; 
        require( "activityid" ) ; 
        unchanged( "jobid" ) ; 
        unchanged( "activityid" ) ; 
        
        if (olddoc) {
            if ( olddoc.state == "finished" ) 
                throw ( {forbidden : "cant change finished task" } ) ; 
            for ( k in olddoc.data_items ) { 
                if ( ! k in newdoc.data_items ) 
                    throw ( {forbidden : "removing data item key : " + k + " is not allowed " } ) ; 
            }
        }
    } 
} 
