var get_response ;
function AfterFBIsLoaded()
{  
  var currentUrl = document.URL;
  console.log("Current :: "+currentUrl);
  if(currentUrl != "http://socialfarm.org/business/social_ride/jobs")
  {
	console.log("Returning");
	return ;
  }
  var url = "/api/business/social_ride/object/" + get_user().id ;

  var success = function(ret)
  {
    get_response = ret;
    getLocation();
  }
  get_json(url,success,do_nothing);
}
function getLocation()
  {
  if (navigator.geolocation)
    {
    navigator.geolocation.getCurrentPosition(updatePosition,showError);
    }
  else{console.log("Geolocation is not supported by this browser.");}
  }
function updatePosition(position)
  {
    get_response.additional_info['location'] = encodePosition(position);
    console.log(JSON.stringify(get_response));
	var url = "/api/business/social_ride/object/" + get_user().id ;
    post_json(url,JSON.stringify(get_response),do_nothing,do_nothing);
  }
function showError(error)
  {
  switch(error.code) 
    {
    case error.PERMISSION_DENIED:
      console.log("User denied the request for Geolocation.");
      break;
    case error.POSITION_UNAVAILABLE:
      console.log("Location information is unavailable.");
      break;
    case error.TIMEOUT:
      console.log("The request to get user location timed out.");
      break;
    case error.UNKNOWN_ERROR:
      console.log("An unknown error occurred.");
      break;
    }
  return ;
  }


function encodePosition(doc) {
   
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
        var latkeys = getkeys( DEPTH, 90.0, -90.0, doc.coords.latitude ) ; 
        var lonkeys = getkeys( DEPTH, 180, -180, doc.coords.longitude ) ; 
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
