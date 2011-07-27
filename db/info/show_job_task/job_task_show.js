function(doc, req) { 

   var Mustache = require( "common/js/mustache" );
   var html = this.common.html.job_show ;

   if (doc.type == 'task') 
      html = this.common.html.task_show ;
   
   return Mustache.to_html( html, doc ) ; 
} 


