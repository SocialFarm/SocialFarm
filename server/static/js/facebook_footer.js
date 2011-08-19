//facebook_footer.js 
//facebook js code for socialfarm.org
var user = null;

window.fbAsyncInit = function() {
	FB.init({ appId: '234690403213067', 
		status: true, 
		cookie: true,
		xfbml: true,
		oauth: true});

   function updateButton(response) {
		
		if (response.authResponse) {
			
		    //user is already logged in and connected
		    FB.api('/me', function(info) {
		        login(response, info);
		    });

            $('button#login').text('Logout');
            $('button#login').click(function() {
                FB.logout(function(response) { logout(response); });
            });  
		    
		} else {
		    //user is not connected to your app or logged out
		    $('button#login').text('Login');
		    $('button#login').click(function() {
                login_prompt(response);
            });
		        
		}
	}

    function login_prompt(response){
        FB.login(function(response) {
            if (response.authResponse) {
                FB.api('/me', function(info) {
                    login(response, info);
                });    
            } else {
                //user cancelled login or did not grant authorization
                
            }
        }, {scope:'email,user_birthday,status_update,publish_stream,user_about_me'});  	

    }

	// run once with current status and whenever the status changes
	FB.getLoginStatus(updateButton);
	FB.Event.subscribe('auth.statusChange', updateButton);	
    $('button#login').text('Login');
    $('button#login').click(function() {
        login_prompt(response);
    });
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
}

function FBOnLoad(){

var html = 	'<li id = "info" >' + 
		 	'<img src="https://graph.facebook.com/' + user.id + '/picture" alt="' + user.id + '">' + 
		   	'<span class="user_name">' + user.name + '</span>' + 
			'</li>';

$('.user ul').prepend(html);

$('#navigation ul.my').prepend('<li id = "my_tasks" ><a class="fbtab" href="/my_tasks/' + user.id + '">My Tasks</a></li>');
$('#navigation ul.my').prepend('<li id = "my_businesses" ><a class="fbtab" href="/my_businesses/' + user.id + '">My Businesses</a></li>');
$('#navigation ul.my').prepend('<li id = "wfe"><a class="fbtab" href ="/static/html/wfe.html">Workflow Editor</a></li>');

if (typeof(SFOnLoad) != "undefined"){
	SFOnLoad();
}	
}






