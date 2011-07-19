function(doc, req) { 

    function show(classname) { 
        return "<p class=\"" + classname + ">" + doc[classname] + "</p>" ; 
    } ; 

    return {
        body : "<!DOCTYPE HTML> <HTML><HEAD> <TITLE> Business </TITLE> </HEAD><BODY>" + show( "author" ) + 
            show( "description" ) +
            show( "total_rating" ) +
            show( "started_since" ) + 
            show( "total_profit" )  + "</BODY></HTML>" , 

        headers: { 
            "Content-Type" : "text/html",
        }
    }
} 
