

// 
// nearby jobs 


function(doc) {
    if(doc.type == "request" && 
       doc.state == "ready" ) {
        emit( doc.dest_geocode, [doc._id,doc.customer,doc.source,doc.destination,doc.date,doc.time] ) ;
    }
}
