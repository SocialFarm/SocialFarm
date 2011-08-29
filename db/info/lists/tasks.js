function (head, req) {   
	var Potato = require( "js/common/potato" );
	send( Potato.list( this.html, head, req ) ) ;   
} 
