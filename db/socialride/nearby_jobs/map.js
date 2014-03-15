

// 
// nearby jobs 


function(doc) {
    if(doc.type == "ride" && 
       doc.state == "ready" ) {
        emit( doc.dest_geocode, doc ) ; 
    }
}
