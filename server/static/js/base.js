/*
  base.js - Javascript wrapper for REST Interface to socialfarm.org and other js that should probably go elsewhere

*/


var revision_cache = {}; 
var do_nothing = function(){};
var user = null;
var DEBUG = true;


function LOG(msg) { 
    if (DEBUG) 
        console.log(msg);
}

//needs to be fixed, currently returning a global var
function get_user() {  
    return user
} 

function set_user(val) { 
    user = val; 
} 

function set_user_access_token(token) { 
    if (user != null){
        user.AccessToken = token; 
    } else {
        sf_login();
    }
} 

function warn(msg){ 
    $('#alert_content').text(msg);
    $('#alert').show();
    $('#alert').focus();
}

function build_readonly_li(label, for_attr, name_attr, type_attr, value_attr){
    return '<li>' +
           '<label for="' + for_attr + '">' + label + '</label>' +
           '<input type="' + type_attr + '" name="' + name_attr + '" id="' + for_attr + '" value = "' + value_attr + '"readonly/>' + 
           '</li>';
}

function build_task_json(){
	var task = Object(); 
	var data_items = Object(); 

	$.each($('#task_form #data_items li'), function(item) { 
		$.each(this.children, function (child) {
			if (! $(this).is('label') && (! $(this).is('button')) ){
				data_items[jQuery.trim(''+this.id)] = jQuery.trim(''+ this.value) ;
			}
		});
	});

	$.each($('#task_form #task_info li'), function(item) { 
		$.each(this.children, function (child) {
			if (! $(this).is('label') && (! $(this).is('button')) ){
				task[jQuery.trim(''+this.id)] = jQuery.trim(''+ this.value) ;
			}
		});
	});
	task.data_items = data_items;
	LOG(task);
	return task;

}

function save_task(){
	var task = build_task_json();
	var url = $('#task_form').attr("action")
	var data = JSON.stringify(task);
	post_json(url, data, null, null);
}

function forward_task(){
	var task = build_task_json();
	var url = $('#task_form').attr("action");
	task.state = 'finished';
	var data = JSON.stringify(task);
	post_json(url, data, null, null);
}

function setHeader(xhr) {
    if (user != null){
        xhr.setRequestHeader('AccessToken', user.accessToken);
    }
}

function get_json(url, successcb, failurecb){
    if (! url in revision_cache) {
        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json',
            success: function (response){ revision_cache[url] = response; successcb();},
            error: failurecb,
            beforeSend: setHeader
        });
    } else {
        LOG('returning cached data...');
        successcb();
    }   
}

function put_json(url, data, successcb, failurecb){
        if (url in revision_cache && data == revision_cache[url]){
            // trying to put the same object 
        } else {
        $.ajax({
            url: url,
            type: 'PUT',
            dataType: 'json',
            data : data,
            success: function (response){ 
                LOG("put response: "  + response);
                revision_cache[url] = data; 
                successcb();
            },
            error: failurecb,
            beforeSend: setHeader
        });
    }
}

function post_json(url, data, successcb, failurecb){
    if (url in revision_cache && data == revision_cache[url]){
        // trying to post the same object 
    } else {
        $.ajax({
        url: url,
        type: 'POST',
        dataType: 'json',
        data : data,
        success: function (response){ revision_cache[url] = data; successcb();},
        error: failurecb,
        beforeSend: setHeader
        });
    }
}

function load_my_tasks(){
    if (user != null){
        id = user.id

        var business_tasks;
        var success = function(tasks) {
            $.each(tasks.rows, function(task){
                $(business_tasks).append('<li><a href="/business/' + business_tasks.id + '/task/' + this.id + '">' +  this.id + '</a></li>');
            });
        };
        var failure = function(tasks) {};

        //asynchronously load tasks via api
        $.each( $('.business_tasks') , function(index, value) { 
            business_tasks = this;
            var url = "/api/business/" + this.id + "/tasks/" + id ;
            get_json(url, success, failure);
        });
    }
}

function add_user_to_socialfarm(){
    if (get_user() != null){
        var url = "/api/person/" + get_user().id

        var person = Object();
        person.type = 'person';
        person.businesses =  Array()

        var data = JSON.stringify(person) ;

        //add person to socialfarm db
        put_json(url, data, do_nothing, do_nothing);
    }
  
}




