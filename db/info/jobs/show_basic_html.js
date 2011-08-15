function(doc, req) { 
	var Mustache = require( "common/js/mustache" );
	var page_template = this.common.html.jobs.show_basic_html ;  
	var default_css = this.common.html.default_css ; 
	var navigation_template = this.facebook.html.navigation ;
	var facebook_footer = this.facebook.html.facebook_footer ;

	nav = Object() ;
	nav.bid = String(req['path']).split(',')[0] ;
	nav.jobs_class = 'active' ;

	doc.navigation = Mustache.to_html( navigation_template, nav ) ;
	doc.default_css = default_css ;
	doc.facebook_footer = facebook_footer ;
	return Mustache.to_html( page_template, doc ) ; 
} 


