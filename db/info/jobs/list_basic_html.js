function (head, req) {   

    var Mustache = require( "common/js/mustache" );
    var page_template = this.common.html.jobs.list_basic_html ; 
    var row_template = this.common.html.jobs.list_basic_html_row ; 

    // set the content header through the call back 
    start({"headers": {"Content-Type": "text/html"}});

    html_rows = String() ; 
    while( (row = getRow()) ) { 
        html_rows += Mustache.to_html( row_template, row.value );
        //log( " html : " + html_rows ) ; 
    }

    doc = Object() ; 
    doc.numrows = head.total_rows ;
    doc.offset = head.offset ; 
    doc.html_rows = html_rows ; 
    send( Mustache.to_html( page_template, doc ) ) ;
} 
