//facebook_footer.js 
//facebook js code for socialfarm.org
var user = null;

function LOG(msg) { 
    console.log(msg) ; 
}
    
(function() {
    var e = document.createElement('script');
    e.type = 'text/javascript';
    e.src = document.location.protocol + '//connect.facebook.net/en_US/all.js';
    e.async = true;
    document.getElementById('fb-root').appendChild(e);
}());

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

/*
function sf_login(response, info){
    
	if (user == null && response.authResponse) {
        user = info;
		
        add_user_to_socialfarm();
		
	} else {
        //console.log('2nd call');
    }
}

*/

function login_prompt(){
    FB.login(function(response) {
        update(response);
    }, {scope:'email,user_birthday,status_update,publish_stream,user_about_me'});  	
}

function update(response){
    LOG('update called');
    if (response.authResponse) {
        FB.api('/me', function(info) {
        user = info;
        FBOnLoad();	
    });    
    } else {
     //user cancelled login or did not grant authorization

    }

}

window.fbAsyncInit = function() {
	FB.init({ appId: '234690403213067', 
		status: true, 
		cookie: true,
		xfbml: false,
		oauth: true});
    
    FB.getLoginStatus(update);
    FB.Event.subscribe('auth.statusChange', update);
    
    if (user == null){
        set_login_button();
    }

	/* On login, make the button say logout */
	FB.Event.subscribe('auth.login', function(response) {
        sf_login();
		set_logout_button(); 
	});

	/* opposite of above */ 
	FB.Event.subscribe('auth.logout', function(response) {
        sf_logout();
        set_login_button(); 
	});
};

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







