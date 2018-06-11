/**
 * Created by blazko on 5.6.2015.
 */
function f() {
    $("#answer").text("You are so buetiful");
    }


function g() {
    $("#description").val("You are so ugly");
    }



function lookup() {
    $("#description").val("Lookup");
}

function translate(event){
    var slovene;
    slovene = $("#code").val();

    function show_deutsch(data) {
         $('#description').val(data.deutsch);
        };

    $.get('/lab/ajax_request/', {"slovene": slovene}, show_deutsch);
};



$(document).ready(function() {
    $('button').click(function(){
        var slovene;
        s = $("#code").val();
        $.get('/lab/ajax_request/', {slovene: s}, function(data){
               $('#description').val(data.deutsch);
           });
    });

    $("#code").blur(translate)

});


