
// emit all the activities that 
// make up this business 

function(doc) {
    if (doc.type == "activity" ) { 
        emit(doc._id, doc) 
    }
}

