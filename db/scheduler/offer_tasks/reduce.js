function(keys, values, rereduce) { 
   if (!rereduce) {
      var busy_people = {} 
      var people = [] ;  
      var jobs = [] ;
      var prevskill = null ;
      var persons_to_jobs = [] ; 
      for( var i = 0; i < keys.length; i++ ) {
         skill = keys[i][0].shift() ;
         rating = keys[i][0].shift() ; 

         //log( [ "v s r" , values[i], skill, rating ] ) ; 

         if( prevskill && prevskill != skill ) {
            //log("completing skill = " + skill) ;
            //log("people = " + people.toString() ) ;  
            //log("jobs = " + jobs.toString() ) ; 

            // if there are people with the given skill
            // set the association from person to job 
            while( (p = people.shift()) && (j = jobs.shift()) ) {
               log( "adding = " + [p,j,skill] ) 
               persons_to_jobs.push( [p,j] ) ; 
               busy_people[p] = 1;
            }
            people = [] ;  
            jobs = [] ;
         }

         // found the person with given skill, who is not yet assigned  
         if (rating != undefined ) { 
            if (!busy_people[values[i]]) 
               people.push( values[i] ) ; 
         } 
        
         // found a job to be done. 
         else
            jobs.push( values[i] ) ;

         prevskill = skill ; 
      }

      while( (p = people.shift()) && (j = jobs.shift()) ) 
         persons_to_jobs.push( [p,j] ) ; 

      return persons_to_jobs;
   }

   // rereduce is true
   else {   
      persons_to_jobs = [] ;
      // notice we have assigned the most skilled workers to outstanding 
      // jobs in each reduce block.  can we at this stage reassign jobs and workers
      // to have a better optimized assignment? at present just append all
      // assignments 
      var busy_people = {} 
      while( assignmentlist = values.shift() )  
         while( ptoj = assignmentlist.shift() ) {
            person = ptoj[0] ; 
            if(busy_people[person])
               continue; 
            persons_to_jobs.push(ptoj) ; 
            busy_people[person] = 1; 
         }
      return persons_to_jobs;
   } 
}
