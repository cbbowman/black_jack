$(document).ready(function(){
    const csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

    console.log(csrftoken);

    $("#reset").click(function(){
        $.post("/test/reset/", {csrfmiddlewaretoken : csrftoken}, function(result){
            $("#game_table").html(result);
        });
    });
    $("#new_game").click(function(){
        $.post("/test/new_game/", {csrfmiddlewaretoken : csrftoken}, function(result){
            $("#game_table").html(result);
        });
    });
    $("#hit").click(function(){
        $.post("/test/hit/", {csrfmiddlewaretoken : csrftoken}, function(result){
            $("#game_table").html(result);
        });
    });
    $("#stand").click(function(){
        $.post("/test/stand/", {csrfmiddlewaretoken : csrftoken}, function(result){
            $("#game_table").html(result);
        });
    });
    $("#double_down").click(function(){
        $.post("/test/double_down/", {csrfmiddlewaretoken : csrftoken}, function(result){
            $("#game_table").html(result);
        });
    });
    $("#split").click(function(){
        $.post("/test/split/", {csrfmiddlewaretoken : csrftoken}, function(result){
            $("#game_table").html(result);
        });
    });
    $("#insurance_yes").click(function(){
        $.post("/test/take_insurance/", {csrfmiddlewaretoken : csrftoken}, function(result){
            $("#game_table").html(result);
        });
    });
    $("#insurance_no").click(function(){
        $.post("/test/setup_game/", {csrfmiddlewaretoken : csrftoken}, function(result){
            $("#game_table").html(result);
        });
    });
});