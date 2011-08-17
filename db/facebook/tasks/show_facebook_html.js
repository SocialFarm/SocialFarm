function(doc, req) { 
	var Mustache = require( "common/js/mustache" );
	var page_template = this.common.html.tasks.show_basic_html ;  
	var navigation_template = this.facebook.html.navigation ;
    var dform = this.common.js.dform ;

    doc.task = task

	nav = Object() ;
	nav.bid = String(req['path']).split(',')[0] ;
	nav.tasks_class = 'active' ;

    if (doc._attachments){
        var docs = Array();
        for (a in doc._attachments){
            
            docs.push({"name":a});
        }
        doc._attachments = docs;
    }

    doc.bid = nav.bid ;

    doc.dform = '<script>' + dform + '</script>' ;
	doc.navigation = Mustache.to_html( navigation_template, nav ) ;
	doc.default_css = this.common.html.default_css ; 
    doc.default_js = this.common.html.default_js ; 
	doc.facebook_footer = this.facebook.html.facebook_footer ;
	return Mustache.to_html( page_template, doc ) ; 
} 


