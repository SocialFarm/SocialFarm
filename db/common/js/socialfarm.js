/*
  socialfarm.js - Javascript wrapper for REST Interface to socialfarm.org 

*/

function add_member_to_business(member, bid){
    $.ajax({
        type: "PUT",
        url: "/api/business/" + bid,
        data: JSON.stringify(member),
        success: function(msg){
            alert(msg);
        }
    });
}


