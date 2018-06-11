function json_callback(data) {
    var name=data.name;
    var surname = data.surname;

    $("#jsondata").html("Json je vrnil " +  name + " " + surname)
}



$(document).ready(function() {

    $(".answer_input").blur(function() {
        var wid, answer;
        answer = $(this).val();
        wid = $(this).attr("id");
        $.get('/words/check_answer/', {"word_id": wid, "answer" : answer},
            function(data){
                var correct_answer = data.correct_answer;
                $("." + wid).html(correct_answer);
        });
    })

    $("#jsonbutton").blur( function() {
        $.getJSON("/words/check_json/",json_callback);
    })

    $("#names").change(function()
        {
            var singer;
            singer = $(this).val();
            url = "/words/get_singer_details/"
            params = {"singer": singer};

            function show_singer_details(data) {
                $(".details p").html(data.description);
                $(".details h2").html(data.singer);
            }

            $.get(url,params,show_singer_details);

            /*$.get("/words/get_singer_details/",params,
            function(data) {
              $(".details").html(data.description);
            });*/
        }
    )
})




