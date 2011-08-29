function(keys, values, rereduce) { 

    if( !rereduce ) {
        currjobrev = null; 
        currjobid = null; 
        prevjobid = null; 
        tasks = [] ;
        tasks_from_jobs = [] ;
        for( var i = 0; i < keys.length; i++ ) {
            jobid = keys[i][0] ;        
            doc = values[i] ;
            //log( "jobid = " + jobid ) 

            // do whats needed with this job now 
            if ( prevjobid != undefined && prevjobid != jobid ) { 
                tasks_from_jobs.push( [currjobid, tasks] ) 
                tasks = [] 
            } 

            if ( doc.type == "job" ) {
                currjobid = jobid ;
                currjobrev = doc.rev ; 
            } 

            if( doc.type == "task" ) 
                tasks.push( doc ) ; 

            prevjobid = jobid ; 
        }

        if( tasks.length > 0 ) 
            tasks_from_jobs.push( [currjobid, tasks] ) 
        
        return tasks_from_jobs ; 
   }
   else {
      new_tasks = []; 
      while( tasks = values.shift() )  
         new_tasks = new_tasks.concat(tasks) ;
      return new_tasks ; 
   } 
}
