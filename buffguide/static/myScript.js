$(document).ready(function(){

    $("#se1").change(function(){
    $("#se2").css("visibility","visible");
    });

    $("#se2").change(function(){
        var level = $('#se2').val();
        var dept = $('#se1').val();
        $.ajax({
            url: '/'+dept+'/'+level,
            type:'POST',
            success: function(response){
                $("#se3").empty();
                $("#se3").append('<option>Select Class</option>');
                response.forEach(function(classItem){
                    $('#se3').append('<option id = '+classItem.classID+'>'+classItem.classCourseNum+'-'+classItem.classTitle+'</option>');
                    console.log('logged');
                });
                $('#se3').css("visibility","visible");
            },
            error: function(error){
            console.log(error);}
        });
    });

    $("#submitClass").click(function(){
        var classInfo = $("#se3").val();
        var classID = $("#se3").children("option:selected").attr("id");
        $.ajax({
            url:'/add/'+classInfo+'/'+classID,
            type:'POST',
            success: function(response){
            $("#classesTable").append('<tr><td>'+response['classInfo']+'</td></tr>');
            },
            error:function(error){
            console.log(error);}
        });
    });

});


