//maps.js

function generateGeoPositionKey(address,success)
{
    var geocoder;
    console.log(address);
    geocoder = new google.maps.Geocoder();
    geocoder.geocode( { 'address': address}, function(results, status) {
    console.log(status);
    if (status == google.maps.GeocoderStatus.OK) {
        loc = results[0].formatted_address ;
        sourceGeoLocation = results[0].geometry.location ;
        LOG(loc);
        LOG(sourceGeoLocation); 
        var key;
        key = encodeGeoPosition(sourceGeoLocation);
        success(key);
        }
    else{ console.log("error");}
    });
}
    
function encodeGeoPosition(doc) {
   
    // each deg is 111km ~= 10^2 km
    // 1km = 0.01 deg 
    // 10m = 0.0001 deg
    // var RESOLUTION = 0.0001; // used to lead to 46 bytes key 
    var DEPTH = 24 ;  
    var MIGRATING = 1;  // temp while we have v2 clients 

    function getkeys(depth, max, min, value) {
        var result = new Array();
        for( var i = 0; i < depth; i++ ) {   // while( (max - min) > delta ) { 
            mid = ( min + max ) / 2.0 ; 
            // log( "max, min, value = " + max + " " + min + " " + value ) ; 
            if( value <= mid ) { 
                result.push( -1 ) ; 
                max = mid ; 
            }
            else if( value > mid ) {
                result.push( +1 ) ; 
                min = mid ; 
            }
        }
        // log( " computed " + result ) ; 
        return result ;   
    }


    function getchoice(value, posvalue, negvalue, zerovalue) { 
        if( value < 0 ) 
            return negvalue; 
        if( value > 0 )
            return posvalue; 
        else
            return zerovalue;
    } 

    if( MIGRATING > 0 || doc.type == "profile" ) {
        var latkeys = getkeys( DEPTH, 90.0, -90.0, doc.lat() ) ; 
        var lonkeys = getkeys( DEPTH, 180, -180, doc.lng() ) ; 
        // log( "length of keys = " + latkeys.length + " , " + lonkeys.length ) ; 

        var maxlen = latkeys.length <  lonkeys.length ? 
             lonkeys.length : latkeys.length ; 
        var kdkeys = new Array() ; 
        for( var i = 0; i < maxlen; i++ ) { 
            var value = 0; 
            if( latkeys.length ) 
                value = latkeys.shift() ; 
            kdkeys.push( getchoice( value, 'n' , 's' , '_' ) ) ; 

            value = 0; 
            if( lonkeys.length ) 
                value = lonkeys.shift() ; 
            kdkeys.push( getchoice( value, 'e' , 'w' , '_' ) ) ; 
        }

        var str = "" ;
        while( ch = kdkeys.shift() ) 
            str += ch ;  

        LOG(str);
        return str;
    }
}
