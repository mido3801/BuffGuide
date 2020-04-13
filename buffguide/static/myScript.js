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
                console.log('success');
                $("#se3").empty();
                $("#se3").append('<option>Select Class</option>');
                response.forEach(function(classItem){
                    $('#se3').append('<option>'+classItem.classCourseNum+'-'+classItem.classTitle+'</option>');
                    console.log('logged');
                });
                $('#se3').css("visibility","visible");
            },
            error: function(error){
            console.log(error);}
        });
    });

});


