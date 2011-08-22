//facebook_footer.js 
//facebook js code for socialfarm.org
var user = null;
var fbresponse = null; 


function LOG(mesg) { 
    console.log(mesg) ; 
}
    

(function() {
    var e = document.createElement('script');
    e.type = 'text/javascript';
    e.src = document.location.protocol +
        '//connect.facebook.net/en_US/all.js';
    e.async = true;
    document.getElementById('fb-root').appendChild(e);
}());



window.fbAsyncInit = function() {
	FB.init({ appId: '234690403213067', 
		status: true, 
		cookie: true,
		xfbml: false,
		oauth: true});

	/* Get permission for the app */ 
	FB.login(function(response) {
		if (response.authResponse) {
		    console.log('Welcome!  Fetching your information.... ');
		    FB.api('/me', function(response) {
			    console.log('Good to see you, ' + response.name + '.');
			    FB.logout(function(response) {
				    console.log('Logged out.');
				});
			});
		} else {
		    console.log('User cancelled login or did not fully authorize.');
		}
	    }, {scope: 'email'});


	/* On login, make the button say logout */
	FB.Event.subscribe('auth.login', function(response) {
		LOG( "Got auth.login" ) ; 
		$('button#login').text('Logout');
		$('button#login').click(function() {
			FB.logout(function(response) { logout(response); });
		    });
		login() ; 
	    });

	/* opposite of above */ 
	FB.Event.subscribe('auth.logout', function(response) {
		LOG( "Got auth.logout" ) ;
		$('button#login').text('Login');
		$('button#login').click(function() {
			login_prompt();
		    });
	    });

	LOG( "Calling get login status" ) ; 
	FB.getLoginStatus(function(response) {
		alert("Hi in get loginstatus");
		fbresponse = response; 
		if (response.session) {
		    // logged in and connected user, someone you know
		    login();
		}
	    });
	LOG( "FB response is " + fbresponse ) ; 



   function updateButton(response) {
       alert("Hi there");
       LOG( "Inside update button" ) ; 
       if (response.authResponse) {
	   fbresponse = response ; 
	   //user is already logged in and connected
	   FB.api('/me', function(info) {
		   login(response, info);
	       });

	   $('button#login').text('Logout');
	   $('button#login').click(function() {
		   FB.logout(function(response) { logout(response); });
	       });  
		    
       } else {
	   LOG('user not connected, and about to assign call back on click'); 
	   //user is not connected to your app or logged out
	   $('button#login').text('Login');
	   $('button#login').click(function() {
		   login_prompt();
	       });
		        
       }
   }


    function login_prompt(){
        FB.login(function(response) {
            if (response.authResponse) {
                FB.api('/me', function(info) {
                    login(response, info);
		    fbresponse = response; 
                });    
            } else {
                //user cancelled login or did not grant authorization
                
            }
        }, {scope:'email,user_birthday,status_update,publish_stream,user_about_me'});  	
    }

	// run once with current status and whenever the status changes
	//LOG( "about to call get login status" ) ; 
	//FB.getLoginStatus(updateButton);
	//LOG( "FB Response is " + fbresponse ) ; 
	//FB.Event.subscribe('auth.statusChange', updateButton);	
};
(function() {
	var e = document.createElement('script'); e.async = true;
	e.src = document.location.protocol + '//connect.facebook.net/en_US/all.js';
	document.getElementById('fb-root').appendChild(e);
}());

//login is getting called twice...
function login(response, info){
    
	if (user == null && response.authResponse) {
        user = info;
		user.accessToken = response.authResponse.accessToken ;
        add_user_to_socialfarm();
		FBOnLoad();	
	} else {
        //console.log('2nd call');
    }
}

function logout(response){
	$('.user #info').remove();
    $('#navigation ul.my #my_businesses, #my_tasks, #wfe').remove();
    user = null;

    $('button#login').text('Login');
    $('button#login').click(function() {
        login_prompt()();
    });
}

function FBOnLoad(){

var html = 	'<li id = "info" >' + 
		 	'<img src="https://graph.facebook.com/' + user.id + '/picture" alt="' + user.id + '">' + 
		   	'<span class="user_name">' + user.name + '</span>' + 
			'</li>';

$('.user ul').prepend(html);

$('#navigation ul.my').prepend('<li id = "wfe"><a class="fbtab" href ="/static/html/wfe.html">Workflow Editor</a></li>');
$('#navigation ul.my').prepend('<li id = "my_tasks" ><a class="fbtab" href="/my_tasks/' + user.id + '">My Tasks</a></li>');
$('#navigation ul.my').prepend('<li id = "my_businesses" ><a class="fbtab" href="/my_businesses/' + user.id + '">My Businesses</a></li>');


if (typeof(SFOnLoad) != "undefined"){
	SFOnLoad();
}	
}






