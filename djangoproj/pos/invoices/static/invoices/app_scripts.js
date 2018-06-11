/**
 * Created by blazko on 12.6.2015.
 */

function likes(event) {
    $.get('/invoice/like_click/',{},function(data) {
        $("#clicks").text(data.clicks);
    });
}

function lookup_artikel() {
    q = $("#txt_lookup").val();
    $.get('/invoice/lookup_names/', {"q": q}, function(data) {
        $("#lookup_artikles").html(data);
    });
}


function choose_artikel(event) {
    var id_artikla = this.getAttribute("data-artikel_id");
    $.get("/invoice/artikel_details/", {"q":id_artikla}, function(data) {
        $("#txt_lookup").val(data.sifra);
        $("#txt_lookup_result").val(data.naziv);
        $("#txt_lookup_result").focus();
        $('#lookup_artikles').collapse('toggle');
    });
}



    


function dlgOk() { 
    $("#txt_lookup_result").val($("#inputname").val());
}

function dlgCancel() {
    alert("Your change your mind");
}


$(document).ready(function() {
    $("#btn_count").click(likes);
    $("#pb_lookup").click(lookup_artikel);
    $("#myModal").on("shown.bs.modal", function(e) {
        }
    );


    $("#myModal").on("hide.bs.modal", function(e) {
        }
    );

    $("#dlg_btnok").click(dlgOk);
    $("#dlg_btnclose").click(dlgCancel);
});




