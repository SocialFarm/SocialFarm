
// emit all the jobs for this business 

function(doc) {
    if (doc.type == "job" ) { 
        emit(doc._id, doc) 
    }
}

