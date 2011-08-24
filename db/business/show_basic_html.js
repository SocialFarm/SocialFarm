function(doc, req) { 
	var Mustache = require( "common/js/mustache" );
	var page_template = this.common.html.show_basic_html ;  
	var navigation_template = this.facebook.html.navigation ;

	nav = Object() ;
	nav.bid = doc._id ;
	nav.business_class = 'active' ;
    nav.common = this.common.html.navigation;

	doc.navigation = Mustache.to_html( navigation_template, nav ) ;
	doc.default_css = this.common.html.default_css ; 
    doc.default_js = this.common.html.default_js ; 
	doc.facebook_footer = this.facebook.html.facebook_footer ;
	return Mustache.to_html( page_template, doc ) ; 
} 


