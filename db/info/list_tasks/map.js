
// emit all the jobs for this business 

function(doc) {
    if (doc.type == "task" ) { 
        emit(doc._id, doc) 
    }
}

