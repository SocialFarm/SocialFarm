

// 
// nearby jobs 


function(doc) {
    if(doc.type == "task" && 
       doc.state == "ready" ) {
        emit( doc.data_items["destinationGeoKeyStr"], doc ) ; 
    }
}
