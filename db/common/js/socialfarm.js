/*
  socialfarm.js - Javascript wrapper for REST Interface to socialfarm.org 

*/

function add_member_to_business(member, bid){
    $.ajax({
        type: "PUT",
        url: "/api/" + bid + "/" + member.id,
        data: JSON.stringify(member),
        success: function(msg){
           	alert(bid + " welcomes new member " + member.name);
			//window.location = "/business/" + bid + "/member/" + member.id ;
        }
    });
}


