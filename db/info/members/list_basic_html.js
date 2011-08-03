function (head, req) {   

    var Mustache = require( "common/js/mustache" );
    var page_template = this.common.html.members.list_basic_html ; 
    var row_template = this.common.html.members.list_basic_html_row ; 
	var navigation_template = this.common.html.navigation ;
    var default_css = this.common.html.default_css ;

	nav = Object() ;
	nav.bid = String(req['path']).split(',')[0] ;
	nav.members_class = 'active'

	navigation = Mustache.to_html( navigation_template, nav )

    // set the content header through the call back 
    start({"headers": {"Content-Type": "text/html"}});

    html_rows = String() ; 
    while( (row = getRow()) ) { 
        html_rows += Mustache.to_html( row_template, row.value );
        //log( " html : " + html_rows ) ; 
    }

    doc = Object() ;
	doc.bid = nav.bid
	doc.navigation = navigation ;
    doc.default_css = default_css ; 
    doc.numrows = head.total_rows ;
    doc.offset = head.offset ; 
    doc.html_rows = html_rows ; 
    send( Mustache.to_html( page_template, doc ) ) ;
} 
