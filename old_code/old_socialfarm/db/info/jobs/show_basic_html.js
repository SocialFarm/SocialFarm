function(doc, req) { 
	var Mustache = require( "common/js/mustache" );
	var page_template = this.common.html.jobs.show_basic_html ;  
	var navigation_template = this.facebook.html.navigation ;

	nav = Object() ;
	nav.bid = String(req['path']).split(',')[0] ;
	nav.jobs_class = 'active' ;
    nav.common = Mustache.to_html(this.common.html.navigation, nav );

	doc.navigation = Mustache.to_html( navigation_template, nav ) ;
	doc.default_css = this.common.html.default_css ; 
    doc.default_js = this.common.html.default_js ; 
	doc.facebook_footer = this.facebook.html.facebook_footer ;
	return Mustache.to_html( page_template, doc ) ; 
} 


