/*
  base.js - Javascript wrapper for REST Interface to socialfarm.org and other js that should probably go elsewhere

*/

var revision_cache = {}; 
var do_nothing = function(){};
var user = null;
var menu = false;

function get_user() { 
    if (user != null){ 
        return user
    } else {
        sf_login();
    }
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
	console.log(task);
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
            success: function (response){ revision_cache[url] = reponse; successcb();},
            error: failurecb,
            beforeSend: setHeader
        });
    } else {
        return revision_cache[url];
    }   
}

function put_json(url, data, successcb, failurecb){
    if (url in revision_cache){
        if (data != revision_cache[url]){
            $.ajax({
                url: url,
                type: 'PUT',
                dataType: 'json',
                data : data,
                success: function (response){ revision_cache[url] = data; successcb();},
                error: failurecb,
                beforeSend: setHeader
            });
        }
    }
}

function post_json(url, data, successcb, failurecb){
     if (url in revision_cache){
        if (data != revision_cache[url]){
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
}

function load_my_tasks(){
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

function add_user_to_socialfarm(){

    var url = "/api/person/" + user.id
    var data = JSON.stringify({"type":"person", "businesses": Array()}) ;
    var success = function(data){/*do nothing*/} ;
    var failure = function(data){/*do nothing*/} ;

    //add person to socialfarm db
    put_json(url, data, success, failure);
  
}

function add_user_to_business(bid){

    var bid = $('#_id').text() ;
    var url = "/api/person/" + user.id ;
    var data;

    var success = function(person) {

        person.businesses.push(bid);

        data = JSON.stringify(person) ;

        //update person in business (bid) db
        put_json(url, data, do_nothing, do_nothing) ;
      
        url =  "/api/business/" + bid + "/object/" + user.id
        data = JSON.stringify(user) ;

        //update person in business (bid) db
        put_json(url, data, do_nothing, do_nothing) ;
       
    };
    get_json(url, success, do_nothing);  
}
