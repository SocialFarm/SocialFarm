function(doc, req) { 

   var Mustache = require( "common/js/mustache" );
   var html = this.common.html.member_show ;
   
   return Mustache.to_html( html, doc ) ; 
} 


