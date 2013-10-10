//facebook_footer.js 
//facebook js code for socialfarm.org
//relies on base.js
function LOG(msg) {
    console.log(msg) ;
}

function get_facebook_user(response){
    FB.api('/me', function(data) {
        set_user(data);
        set_auth_token(response);
        /*  this allows for clientside code which is only called when the user is logged in
            simply define the function in a script tag, and call other functions from it
        */
        if(typeof AfterFacebookIsLoaded == 'function') {
            //to make sure this is only ever called once
            window['AfterFacebookIsLoaded'] = null;
        }
    });
}

function set_auth_token(response){
    user.AccessToken = response.authResponse.accessToken;
    user.FBID = response.authResponse.userID;
    LOG('PRERAK Facebook User ID : ' + response.authResponse.userID);
    LOG('PRERAK Facebook Access Token : ' + response.authResponse.accessToken);
}

window.fbAsyncInit = function() {
    LOG("TRYING");
    FB.init({ appId: '234690403213067',
        status: true,
        cookie: true,
        xfbml: false,
        oauth: true});
    LOG('PRERAK chk2');
    function updateButton(response) {

        if (response.authResponse) {
            //user is already logged in and connected
            get_facebook_user(response);
            LOG('PRERAK logged in');
      } else {
            //user is not connected to your app or logged out
            LOG('PRERAK logged out');
        }
    }

  // run once with current status and whenever the status changes
  FB.getLoginStatus(updateButton);
  FB.Event.subscribe('auth.statusChange', updateButton);
};

(function() {
    LOG('Start');
    var e = document.createElement('script'); e.async = true;
    e.src = document.location.protocol + '//connect.facebook.net/en_US/all.js';
    document.getElementById('fb-root').appendChild(e);
    LOG('PRERAK ckh 1');
}());

