//facebook_footer.js 
//facebook js code for socialfarm.org
//relies on base.js
var user = null;
function set_user(val) { 
	user = val; 
}

function get_user(){
	return user;
}

function LOG(msg) { 
    console.log(msg) ; 
}
    
function set_login_button(){
    $('button#login').text('Login');
    $('button#login').click(function() {
        sf_login();
    });
}

function set_logout_button(){
    $('button#login').text('Logout');
    $('button#login').click(function() {
        sf_logout();
    });
}

function AfterFacebookIsLoaded() {
		render_member_info();
    load_user_info();
}

//fix me :: put the correct html code to get proper indentation on html page
function render_member_info(){

	var html= '<div id="name">   Name : ' + get_user().name + '</div>';
    $('#userinfo').append(html);
}

function get_facebook_user(response){
	FB.api('/me', function(data) {
		set_user(data);
        set_auth_token(response);
        add_user_to_socialride();
        /*  this allows for clientside code which is only called when the user is logged in
            simply define the function in a script tag, and call other functions from it
        */

        if(typeof AfterFacebookIsLoaded == 'function') {

            AfterFacebookIsLoaded();
            //to make sure this is only ever called once
            window['AfterFacebookIsLoaded'] = null;
        }
	});	
}



function set_auth_token(response){
    user.AccessToken = response.authResponse.accessToken;
	user.FBID = response.authResponse.userID;
    LOG('Facebook User ID : ' + response.authResponse.userID);    
    LOG('Facebook Access Token : ' + response.authResponse.accessToken);
}

function sf_login(){
    LOG('sf_login');
	if (get_user() == null) {
		FB.login(function(response) {
			if (response.authResponse) {
		  		get_facebook_user(response);
			} else {
			//user cancelled login or did not grant authorization
			}
		}, {scope:'email'});  
		set_logout_button();
	}
}

function sf_logout(){
    LOG('sf_logout');
	if (get_user() != null){
    	FB.logout();
		//$('#user_profile ul #info').remove();
		//$('#user_navigation ul #my_businesses, #my_tasks, #wfe').remove();
		set_user(null);
	}
    set_login_button();
}

window.fbAsyncInit = function() {
	FB.init({ appId: '234690403213067', 
		status: true, 
		cookie: true,
		xfbml: false,
		oauth: true});

    function updateButton(response) {

        if (response.authResponse) {
            //user is already logged in and connected
            get_facebook_user(response);
            set_logout_button();
        } else {
            //user is not connected to your app or logged out
            set_login_button();
        }
    }

  // run once with current status and whenever the status changes
  FB.getLoginStatus(updateButton);
  FB.Event.subscribe('auth.statusChange', updateButton);	
};
	
(function() {
    var e = document.createElement('script'); e.async = true;
    e.src = document.location.protocol + '//connect.facebook.net/en_US/all.js';
    document.getElementById('fb-root').appendChild(e);
}());
