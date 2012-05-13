/*  Potato.js 
    Written by Orie Steele

    Purpose: to leverage template inheritance using mustache in order to standardize 
    the process of rendering shows and lists, reducing the number of edits required
    for major changes.

    Called by a number of js from within couchdb.  This code takes in the html provided
    to the rendering functions (the html was stored in various shows and lists in couchdb) 
    and the fields of the document are expanded through templating.  For usage example 
    do grep -R Potato * from db directory 

    Usefull for debugging:
        JSON.stringify(data)
*/

var Mustache = require( "js/common/mustache" );

function json_to_key_value(obj){
    var items = Array();
    for (k in obj){
        items.push({"key":k, "value": obj[k]});
    }
    return items
}

function mustachify_obj(obj){
    for (k in obj){
        if (typeof obj[k] === 'object'){
            obj[k] = json_to_key_value(obj[k]);
        }
    }
}

var Potato = function() {
    var Renderer = function() {};
    Renderer.prototype = {
        show: function(html, doc, req) {
            var path = String(req['path']).split(',');
            var show = path[path.length -2];
		    var content = html[show];
	
		    nav = Object();
            nav[doc.type] = 'active';

            //set bid for ease of use
            if (doc.type == 'business'){
		        nav.bid = doc._id;
                doc.bid = doc._id;
            } else {
                nav.bid = path[0];
                doc.bid = path[0];
            }

			if (doc.started_since != null){
				var date = new Date();
				date.setTime(doc.started_since*1000);
				doc.started_since = date.toUTCString();
			}
			if (doc.working_since != null){
				var date = new Date();
				date.setTime(doc.working_since*1000);
				doc.working_since = date.toUTCString();
			}
            
            mustachify_obj(doc); 
			  
    
		    head = Object();
		    head.user_navigation = Mustache.to_html(html.common.user_navigation, nav);
		    head.business_navigation = Mustache.to_html(html.common.business_navigation, nav);
        
            if (show == 'my_businesses' || show == 'my_tasks'){
                head.business_navigation = null;
            }

		    header = Mustache.to_html(html.common.header, head);		

		    base = Object();
		    base.title = doc._id;

		    base.meta_description = html.meta_description;
		    base.meta_author = html.common.meta_author;

		    base.default_css = html.common.default_css;
		    base.default_js = html.common.default_js;
		    base.header = header;
		    base.content = Mustache.to_html(content, doc);
		    base.footer = Mustache.to_html(html.common.footer, doc);

		    return Mustache.to_html(html.common.base, base);
        },  
        list: function(html, head, req) {
            var path = String(req['path']).split(',');
            var view = path[path.length -2];
		    var content = html[view] ; 
       		var content_row = html[view +'_row'] ;

		    //no business nav so nav is empty for now
        	nav = Object();
            nav.bid = path[0];
		    nav.user_navigation = Mustache.to_html(html.common.user_navigation, nav);
 			nav.business_navigation = Mustache.to_html(html.common.business_navigation, nav);

			if (nav.bid == 'socialfarm'){
                nav.business_navigation = null;
            }

		    header = Mustache.to_html(html.common.header, nav);		
		    start({"headers": {"Content-Type": "text/html"}});

		    html_rows = String() ; 
		    while( (row = getRow()) ) { 
                row.value.bid = path[0];
				if (row.value.started_since != null){
					var date = new Date();
					date.setTime(row.value.started_since*1000);
					row.value.started_since = date.toUTCString();
				}
				if (row.value.working_since != null){
					var date = new Date();
					date.setTime(row.value.working_since*1000);
					row.value.working_since = date.toUTCString();
				}
				if (row.value.activity_skills != null){
					row.value.activity_skills = json_to_key_value(row.value.activity_skills);
				}
				if (row.value.data_items != null){
                    // data_items shows objects in activities and strings in jobs because of different data structure 
                    // activities should not be shown or their data_items should have the same data structure 
                    // log( "row.value.data_items=" + row.value.data_items + JSON.stringify(row.value.data_items));
					row.value.data_items = json_to_key_value(row.value.data_items);
				}
		        html_rows += Mustache.to_html( content_row, row.value );
		    }
            
            head.numrows = head.total_rows ;
		    head.offset = head.offset ; 
		    head.html_rows = html_rows ;
	
		    base = Object();

            base.title = path[0] + " > " + path[path.length -1];

		    base.meta_description = html.common.meta_description;
		    base.meta_author = html.common.meta_author;

		    base.default_css = html.common.default_css;
		    base.default_js = html.common.default_js;
		    base.header = header;
		    base.content = Mustache.to_html(content, head);
		    base.footer = Mustache.to_html(html.common.footer, head);
		    return Mustache.to_html(html.common.base, base);
        }
    };

    return({
        name: "potato.js",
        version: "0.0",

        show: function(html, doc, req) {
            var renderer = new Renderer();
            return renderer.show(html, doc, req);
        },
        list: function(html, head, req) {
            var renderer = new Renderer();
            return renderer.list(html, head, req);
        }
    });
}();

exports.show = Potato.show; 
exports.list = Potato.list; 
