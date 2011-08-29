function( newdoc, olddoc, uxt ) 
{ 
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

    
    require( "type" ) ;

    if( ! belongs( newdoc.type , [ "activity" , "job" , "task" , "person" ] ) ) 
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
