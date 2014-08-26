

// 
// nearby jobs 


function(doc) {
    if(doc.type == "offer" && 
       doc.state == "ready" ) {
        emit( doc.dest_geocode, [doc._id,doc.customer,doc.source,doc.destination,doc.date,doc.time] ) ;
    }
}
