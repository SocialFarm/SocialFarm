function(doc) {
    if (doc.type == "business" ) {
        emit( doc.list_of_partners, doc )
    }
}

