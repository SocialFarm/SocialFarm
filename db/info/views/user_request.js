/* Return the requests created by a user */

function(doc) {
    if(doc.type == "request") {
        emit( doc.customerId, [doc._id,doc.source,doc.destination,doc.date,doc.time,doc.state] )
    }
}
