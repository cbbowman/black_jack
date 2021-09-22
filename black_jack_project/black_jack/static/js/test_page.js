$(document).ready(function(){
    $.get('/test/display/', function(data){
        $('#game_table').html(data);
    });
});