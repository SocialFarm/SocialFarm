function(doc, req) {
        var Potato = require( "js/common/potato" );
        return Potato.show(this.html, doc, req);
}

