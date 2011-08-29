
// emit all the activities that 
// make up this business 

function(doc) {
    if (doc.type == "activity" ) { 
        if ( doc.predecessors.length == 0 ) 
            emit(doc._id, doc) ; 
    }
}

