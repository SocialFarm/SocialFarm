

// 
// nearby jobs 


function(doc) {
    if(doc.type == "offer" && 
       doc.state == "ready" ) {
        emit( doc.dest_geocode, doc ) ; 
    }
}
