
// emit all the tasks for this business 

function(doc) {
    if (doc.type == "task" ) { 
        emit(doc.worker, doc) 
    }
}

