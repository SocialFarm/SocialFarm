function(doc) {
    // return the members of business
    if (doc.type == "business" ) {
        emit( doc._id, doc )
    }
}

