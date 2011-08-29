//facebook_footer.js 
//facebook js code for socialfarm.org
//relies on base.js

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
    if (!menu) {
        add_user_to_socialfarm();
        menu = true;
        var html = 	'<li id = "info" >' + 
		         	'<img src="https://graph.facebook.com/' + get_user().id + '/picture" alt="' + user.id + '">' + 
		           	'<span class="user_name">' + get_user().name + '</span>' + 
			        '</li>';

        $('.user ul').prepend(html);

        $('#navigation ul.my').prepend('<li id = "wfe"><a class="fbtab" href ="/static/html/wfe.html">Workflow Editor</a></li>');
        $('#navigation ul.my').prepend('<li id = "my_tasks" ><a class="fbtab" href="/my_tasks/' + get_user().id + '">My Tasks</a></li>');
        $('#navigation ul.my').prepend('<li id = "my_businesses" ><a class="fbtab" href="/my_businesses/' + get_user().id + '">My Businesses</a></li>');
 
        if (typeof(SFOnLoad) != "undefined"){
	        SFOnLoad();
        }
    }
}

function sf_login(){
    LOG('sf_login');
	FB.login(function(response) {
		if (response.authResponse) {
            FB.api('/me', function(person) {
                set_user(person);
            });	
		    set_user_access_token(response.authResponse.accessToken); 
            FBOnLoad();
		} else {
		//user cancelled login or did not grant authorization
		}
	}, {scope:'email'});  
	set_logout_button();
}

function sf_logout(){
    LOG('sf_logout');
	FB.logout();

	$('.user #info').remove();
	$('#navigation ul.my #my_businesses, #my_tasks, #wfe').remove();

	set_user(null);
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
        FB.api('/me', function(person) {
            set_user(person);
        });	
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








