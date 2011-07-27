function(doc) {
    if (doc.type == "business" ) {
        emit( doc._id, doc )
    }
}

