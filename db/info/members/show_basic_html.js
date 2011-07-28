function(doc, req) { 
   var Mustache = require( "common/js/mustache" );
   var html = this.common.html.members.show_basic_html ;
   return Mustache.to_html( html, doc ) ; 
} 


