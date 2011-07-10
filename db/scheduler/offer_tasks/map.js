function(doc) {
   if (doc.type == "task" && doc.state == "ready" ) { 
      for( i = 0 ; i < doc.skills_required.length ; i++ ) {
         emit( [doc.skills_required[i]] , doc._id ) 
      }
   }
   if (doc.type == "person" && doc.looking_for_work == "yes") {
      for( i = 0 ; i < doc.skills.length ; i++ ) {      
         emit( [doc.skills[i], -doc.ratings[i]] , doc._id)
      }
   }
}
