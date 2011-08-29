function(doc) { 
   if (doc.type == "job" && doc.state != "finished" && doc.state != "error" ) {
      emit(doc._id, { "type" : "job" , "rev" : doc._rev } )
   }
   if (doc.type == "task") { 
      emit(doc.jobid, doc) 
   }                             
}     
