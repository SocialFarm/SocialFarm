function(doc) {
    // return the members of business
    if (doc.type == "person" ) {
        emit( doc._id, doc )
    }
}

