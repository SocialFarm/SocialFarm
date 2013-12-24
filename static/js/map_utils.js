// This file contains utility function for social ride

var map = null;

function read_html_form_data(form_id) {
    var form ;
    var member = Object();
    form = $("#"+form_id).serializeArray();
    
    $.each(form, function (item) {
                    member[form[item].name] = form[item].value;
                    });
    return member;
}

//Init google maps
function init_map() {
   
    //geocoder = new google.maps.Geocoder();
    var latlng = new google.maps.LatLng(12.9715987,77.59456269 );
    var mapOptions = {
        zoom: 8,
        center: latlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
        }
    map = new google.maps.Map(document.getElementById('map_canvas'), mapOptions);
}

// This function will map all available positions for the address on map
// type= source/address
function map_address_on_map( address, type, success, failure)
{
  //init_map();
  geocoder = new google.maps.Geocoder();
  var geolocation = {};
  geocoder.geocode( { 'address': address}, function(results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      map.setCenter(results[0].geometry.location);
      for(var i=0 ; i < results.length ; i++ ) {
        var marker = new google.maps.Marker({
          map: map,
          //TODO :: get images for source and destination.
          //icon: image
          position: results[i].geometry.location,
          draggable: true,
          title: type
        });
        marker.setTitle(results[i].formatted_address);
        attachMessage(results[i].formatted_address ,results[i].geometry.location, marker,type );
      }
      //set initial position in DB
      geolocation['address'] = results[0].formatted_address ;
      geolocation['latlong'] = results[0].geometry.location ;
      success(results[0].formatted_address ,results[0].geometry.location,type);
    }else {
      alert('Geocode was not successful for the following reason: ' + status);
      failure(address);
    }
 });
}

function attachMessage(address,geoLocation,marker,type)
{
  var infowindow = new google.maps.InfoWindow({
    content: address,
    size: new google.maps.Size(50,50)
  });

  google.maps.event.addListener(marker, 'click', function() {
    infowindow.open(map,marker);
    change_location(address, geoLocation, type);
  });
}

//TODO :: Add code to get the new location after dragging the map marker

// function to encode the geolocation to a special format.
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

function setHeader(xhr) {
    if (user != null){
        xhr.setRequestHeader('accesstoken', user.AccessToken);
        xhr.setRequestHeader('fbid', user.FBID);
    }
}

function put_json(url, data, successcb, failurecb){
        //if (url in revision_cache && data == revision_cache[url]){
            // trying to put the same object 
        //    LOG('trying to put the same object...');
        //} else {
        $.ajax({
            url: url,
            type: 'PUT',
            dataType: 'json',
            data : data,
            success: function (response){ 
                LOG('PUT response: ' + JSON.stringify(response));
                //should update cache rev
                //revision_cache[url] = response; 
                successcb(); 
            },
            error: failurecb,
            beforeSend: setHeader
        });
    //}
}

function get_json(url, successcb, failurecb){
    //caching not working >:(
    //if (! url in revision_cache) {
        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json',
            success: function (response){
                LOG('GET response: ' + JSON.stringify(response));
                //revision_cache[url] = JSON.stringify(response);
                successcb(response);
            },
            error: failurecb
            //beforeSend: setHeader
        });
    /*
    } else {
        LOG('returning cached data...');
        successcb(revision_cache[url]);
    }   */
}

function do_nothing()
{}
function add_user_to_socialride() {
  var userInfo = get_user();
  if (userInfo != null){
    var url = "http://socialfarm.org/couchdb/social_ride/user1."+ get_user().id ;

    var failure = function(){
    var person = Object();
    person.type = 'person';
    person.name = userInfo.name;
    person.id = userInfo.id;
    person.gender = userInfo.gender;

    var data = JSON.stringify(person) ;
    //add person to socialfarm db
   /* code snippet for caching, which is currently disabled
      var update_id = function (response){
      LOG('add user response: ' + response);
      revision_cache[url].rev = response.rev;
       };*/
     put_json(url, data, do_nothing, do_nothing);
  }}
     var success = function(response){
         LOG('person is already in the datebase: ' + JSON.stringify(response));
    }
     get_json(url, success, failure);
    }

