function(doc, req) { 
	var Mustache = require( "common/js/mustache" );
	var page_template = this.common.html.actions.show_basic_html ;  
	var navigation_template = this.facebook.html.navigation ;
	var facebook_footer = this.facebook.html.facebook_footer ;

	nav = Object() ;
	nav.bid = String(req['path']).split(',')[0] ;
	nav.actions_class = 'active' ;
    nav.common = Mustache.to_html(this.common.html.navigation, nav );

    if (doc._attachments){
        var docs = Array();
        for (a in doc._attachments){
            
            docs.push({"name":a});
        }
        doc._attachments = docs;
    }

    doc.bid = nav.bid ;
	doc.navigation = Mustache.to_html( navigation_template, nav ) ;
	doc.default_css = this.common.html.default_css ; 
    doc.default_js = this.common.html.default_js ; 
	doc.facebook_footer = facebook_footer ;
	return Mustache.to_html( page_template, doc ) ; 
} 


