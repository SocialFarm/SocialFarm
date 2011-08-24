//facebook_footer.js 
//facebook js code for socialfarm.org
var user = null;
var menu = false;

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

function FBOnLoad(){
    if (!menu && user != null) {
        add_user_to_socialfarm();
        menu = true;
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
}

function get_facebook_user(){
	FB.api('/me', function(response) {
		user = response;
		FBOnLoad();
	});	
}

function sf_login(){
    LOG('sf_login');
	if (user == null) {
		FB.login(function(response) {
			if (response.authResponse) {
		  		get_facebook_user();
				if (user != null)
					user.AccessToken = response.authResponse.accessToken; 
			} else {
			//user cancelled login or did not grant authorization
			}
		}, {scope:'email'});  
		set_logout_button();
	}
}

function sf_logout(){
    LOG('sf_logout');
	if (user != null){
    	FB.logout();
		$('.user #info').remove();
		$('#navigation ul.my #my_businesses, #my_tasks, #wfe').remove();
		user = null;
	}
    set_login_button();
}

window.fbAsyncInit = function() {
	FB.init({ appId: '234690403213067', 
		status: true, 
		cookie: true,
		xfbml: false,
		oauth: true});

    //set_login_button();

  function updateButton(response) {
	
    if (response.authResponse) {
      //user is already logged in and connected
      get_facebook_user();
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








