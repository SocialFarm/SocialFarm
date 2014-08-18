function(doc) {
    if(doc.type == "offer") {
        emit( doc.customerId, [doc._id,doc.customer,doc.source,doc.destination,doc.date,doc.time] ) ;
    }
}

