//facebook_footer.js 
//facebook js code for socialfarm.org
var user = null;

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

function sf_login(){
    LOG('sf_login');
    login_prompt();
    set_logout_button();
   
}

function sf_logout(){
    LOG('sf_logout');
    $('.user #info').remove();
    $('#navigation ul.my #my_businesses, #my_tasks, #wfe').remove();
    user = null;
    set_login_button();
}

function login_prompt(){
    FB.login(function(response) {
        updateButton(response);
    }, {scope:'email,user_birthday,status_update,publish_stream,user_about_me'});  	
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
      FB.api('/me', function(response) {
        FBOnLoad();
      });
        set_logout_button();
     
    } else {
        //user is not connected to your app or logged out
        set_login_button();

        $('button#login').click(function() {
            FB.login(function(response) {
                if (response.authResponse) {
                    FB.api('/me', function(response) {
                        FBOnLoad();
                    });	   
                } else {
                    //user cancelled login or did not grant authorization
                }
            }, {scope:'email'});  	
        });
    }
  }

  // run once with current status and whenever the status changes
  FB.getLoginStatus(updateButton);
  FB.Event.subscribe('auth.statusChange', updateButton);	
};
	
(function() {
  var e = document.createElement('script'); e.async = true;
  e.src = document.location.protocol 
    + '//connect.facebook.net/en_US/all.js';
  document.getElementById('fb-root').appendChild(e);
}());








