<!doctype html>  
<html lang="en">
    <head>  
        <meta charset="utf-8">  
        <title>${title}</title>  
        <meta name="description" content="...">  
        <meta name="author" content="Social Farm">  
        ${self.css()}
        ${self.js()}
    </head>  
    <body>
        ${self.header()}
        ${self.content()}
        ${self.footer()}
        ${self.async_js()}
    </body>
</html>

<%def name="title()"></%def>
<%def name="css()"></%def>
<%def name="js()"></%def>
<%def name="header()"></%def>
<%def name="content()"></%def>
<%def name="footer()"></%def>
<%def name="async_js()"></%def>
