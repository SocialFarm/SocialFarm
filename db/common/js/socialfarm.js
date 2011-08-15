/*
  socialfarm.js - Javascript wrapper for REST Interface to socialfarm.org 

*/

function add_person_to_socialfarm(id){

    $.ajax({
        type: "PUT",
        url: "/api/person/" + id,
        data: JSON.stringify({"type":"person", "businesses": Array()}),
        success: function(msg){

        }
    });

}

function add_member_to_business(member, bid){
    
    add_person_to_socialfarm(member.id);

    $.get("/api/person/" + member.id, function(data) {
        $('.result').html(data);
        data['businesses'].push(bid)

        $.ajax({
        type: "PUT",
        url: "/api/person/" + member.id,
        data: JSON.stringify(data),
        success: function(msg){
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
        });
    });

    
}


