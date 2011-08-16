function(doc, req) { 
	var Mustache = require( "common/js/mustache" );
	var page_template = this.facebook.html.my_tasks_html ;  
	var default_css = this.common.html.default_css ; 
    var default_js = this.common.html.default_js ; 
	var navigation_template = this.facebook.html.navigation ;
	var facebook_footer = this.facebook.html.facebook_footer ;

	nav = Object() ;
	nav.bid = null ;
	nav.tasks_class = 'active' ;

	doc.navigation = Mustache.to_html( navigation_template, nav ) ;

    var my_tasks = Array()

    for (b in doc.businesses){

        $.getJSON("/" + doc.businesses[b] + "/_design/info/_list/tasks_basic_html/all_tasks?key=" + doc._id, function(tasks) {
            my_tasks.push(tasks);
        });
   

        
    }
        
    doc.tasks = my_tasks
	doc.default_css = default_css ;
    doc.default_js = default_js ;
	doc.facebook_footer = facebook_footer ;
	return Mustache.to_html( page_template, doc ) ; 
} 


