/*
  socialfarm.js - Javascript wrapper for REST Interface to socialfarm.org 

*/

function get_my_tasks(id){

     $.getJSON("/api/person/" + id, function(person) {
        var data = Array();
    
        for (b in person.businesses){
            $.getJSON("/api/" + person.businesses[b] + "/tasks/" + id, function(tasks) {
               console.log(tasks);
            });
        }
    });

}

function add_person_to_socialfarm(id){

    $.ajax({
        type: "PUT",
        url: "/api/person/" + id,
        data: JSON.stringify({"type":"person", "businesses": Array()}),
        success: function(msg){
        //do nothing 
        }
    });

}

function add_member_to_business(member, bid){
    
    add_person_to_socialfarm(member.id);

    $.getJSON("/api/person/" + member.id, function(person) {

        person.businesses.push(bid);

        $.ajax({
                type: "PUT",
                url: "/api/person/" + member.id,
                data: JSON.stringify(person),
                success: function(msg){
                    //updated person in socialfarm db
                }
        });

        $.ajax({
            type: "PUT",
            url: "/api/" + bid + "/" + member.id,
            data: JSON.stringify(member),
            success: function(msg){
                //add person to business (bid) db
            }
        });
    });   
}



