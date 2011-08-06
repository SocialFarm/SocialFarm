function(doc, req) { 
    var Mustache = require( "common/js/mustache" );
    var page_template = this.common.html.members.show_basic_html ;  
    var default_css = this.common.html.default_css ; 
    var navigation_template = this.common.html.navigation ;

    nav = Object() ;
    nav.members_class = 'active' ;
    nav.bid = String(req['path']).split(',')[0] ;

    doc.bid = nav.bid
    doc.navigation = Mustache.to_html( navigation_template, nav ) ;
    doc.default_css = default_css ;
   
    return Mustache.to_html( page_template, doc ) ; 
} 


