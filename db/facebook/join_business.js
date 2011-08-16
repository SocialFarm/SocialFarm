function(doc, req) { 
	var Mustache = require( "common/js/mustache" );
	var page_template = this.facebook.html.join_business_html ;  
	var default_css = this.common.html.default_css ; 
    var default_js = this.common.html.default_js ; 
	var navigation_template = this.facebook.html.navigation ;

	var facebook_footer = this.facebook.html.facebook_footer ;
	//var FBOnLoad = this.facebook.html.FBOnLoad ;	

	nav = Object() ;
	nav.bid = doc._id ;
	nav.business_class = 'active' ;

	doc.navigation = Mustache.to_html( navigation_template, nav ) ;
	doc.default_css = default_css ;
    doc.default_js = default_js + '<script>' + this.common.js.socialfarm + '</script>' ;
	doc.facebook_footer = facebook_footer ;
	//doc.FBOnLoad = FBOnLoad ;
	return Mustache.to_html( page_template, doc ) ; 
} 

