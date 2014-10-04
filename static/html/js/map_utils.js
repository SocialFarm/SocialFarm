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
function encodeGeoPosition(lat,lng) {
 
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

    if( MIGRATING > 0 ) {
        var latkeys = getkeys( DEPTH, 90.0, -90.0, lat ) ; 
        var lonkeys = getkeys( DEPTH, 180, -180, lng ) ; 
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

        //LOG(str);
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
    var url = "http://socialfarm.org/couchdb/social_ride/user."+ get_user().id ;

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
    };
  }
     var success = function(response){
         LOG('person is already in the datebase: ' + JSON.stringify(response));
         updateCurrentLocation(url,response);
    };
     get_json(url, success, failure);
}

//TODO :: pjain :: add code to accept ride
function acceptRide(id)
{
  alert("Accepted "+ id);
}

function appendNearByRideInfoTable(data,divId) {
  /* Array description
    0 -> ride id
    1 -> user name
    2 -> source
    3 -> destination
    4 -> date
    5 -> time 
    6 -> friend */
    
    var html = '<tr id="'+data[0]+'">' +
                '<td class="when">'+data[4]+'</td>'+
                '<td class="sd"><span>'+data[2] + '-' + data[3] + '</span></td>'+
                '<td class="lug">'+data[1]+'</td>' +
                '<td class="stopver">'+data[5]+'</td>'+
                '<td class="friends">2</td>'+
                '<td> <button id = "accept" onclick=acceptRide("'+data[0]+'")>Accept</button> </td>'+
                '</tr>';
        
    $('#'+divId).append(html);
}

function fillNearByRideInfo(type,curLocGeoCode) {
    var viewUrl;
    var divId;
// TODO :: Change the below url to nearby view url
    if( type === "request"){
        viewUrl = "http://socialfarm.org/couchdb/social_ride/_design/info/_view/nearby_request";
        divId = "tab_request";
    }
    else {
        viewUrl = "http://socialfarm.org/couchdb/social_ride/_design/info/_view/nearby_offer";
        divId = "tab_offer";
    }
    
    get_json(viewUrl,function(data){
        $(data.rows).each(function (i, row){
            $(row).each(function (j, col) {
                appendNearByRideInfoTable(col.value,divId);
            });
        });
    },do_nothing);
 }

function appendMyRideInfoTable(data,divId) {
  /* Array description
    0 -> ride id
    1 -> source
    2 -> destination
    3 -> date
    4 -> time 
    5 -> friend 
    6 -> status */
    
    var html = '<tr id="'+data[0]+'">' +
                '<td class="when">'+data[3]+'</td>'+
                '<td class="sd"><span>'+data[1] + '-' + data[2] + '</span></td>'+
                '<td class="stopver">'+data[4]+'</td>'+
                '<td class="friends">2</td>'+
                '<td class="friends">'+data[5]+'</td>'+
                '<td> <button id = "rate">Rate</button> </td>'+
                '</tr>';
        
    $('#'+divId).append(html);
}
function fillMyRideInfo(type,userId) {
    var viewUrl;
    var divId;

    if( type === "request"){
        viewUrl = 'http://socialfarm.org/couchdb/social_ride/_design/info/_view/my_request?key=%22user.'+userId+'%22';
        //viewUrl = "http://socialfarm.org/couchdb/social_ride/_design/test/_view/temp"
        divId = "tab_my_req";
    }
    else {
        viewUrl = 'http://socialfarm.org/couchdb/social_ride/_design/info/_view/my_offer?key=%22user.'+userId+'%22';
        //viewUrl = "http://socialfarm.org/couchdb/social_ride/_design/test/_view/temp"
        divId = "tab_my_offer";
    }
    get_json(viewUrl,function(data){
        $(data.rows).each(function (i, row){
            $(row).each(function (j, col) {
                appendMyRideInfoTable(col.value,divId);
            });
        });
    },do_nothing);
}
var tmp = 0;
function updateCurrentLocation(url,user)
{
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function savePosition(position) {
            var loc = encodeGeoPosition(position.coords.latitude ,position.coords.longitude);
            user['curLocation']=loc;
            var data = JSON.stringify(user);
            if(tmp == 0){
            // to prevent calling put_json twice with the same rev_id
            put_json(url,data,do_nothing,do_nothing);tmp++;}
        });
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}
