

// 
// nearby jobs 


function(doc) {
    if(doc.type == "ride" && 
       doc.state == "ready" ) {
        emit( doc.data_items["destinationGeoKeyStr"], doc ) ; 
    }
}
