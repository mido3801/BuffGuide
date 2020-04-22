var classCount=0;
var clickedList = [];
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
        var classID = $("#se3").children("option:selected").attr("id");
        $.ajax({
            url:'/add/'+classID,
            type:'POST',
            success: function(response){
            console.log(response['classBuilding']);
            $("#classesTable").append('<tr class="classRow" id='+response['classBuilding']+'><td>'+response['classNum']+response['classTitle']+'</td><td>'+response['classBuilding']+response['classRoom']+'</td><td><button id="rcbutton">X</button></td></tr>');
            },
            error:function(error){
            console.log(error);}
        });
    });

    $(document).on("click","#rcbutton",(function(){
        var row = $(this).closest('tr');
        var classID = row.attr('id');
        row.remove();
        $.ajax({
            url:'/remove/'+classID,
            type:"POST",
            success: function(response){
            console.log('class deleted');},
            error:function(error){
            console.log(error);}
            });
            })
    );

    $(document).on("click",".classRow",function(){
            console.log(classCount);
            if ($(this).hasClass("tanRow")){
                $(this).removeClass("tanRow");
                $(this).toggleClass("whiteRow");
                var index = clickedList.indexOf($(this).attr("id"));
                clickedList.splice(index,1);
                console.log(clickedList);
            }
            else{
            if (classCount==0){
                $(this).removeClass("whiteRow");
                $(this).toggleClass("tanRow");
                classCount++;
                clickedList.push($(this).attr('id'));
            }
            else if (classCount==1){
                $(this).toggleClass("tanRow");
                $(this).removeClass("whiteRow");
                clickedList.push($(this).attr('id'));
                console.log(clickedList);
                classCount++;
            }
            else if (classCount==2){
                console.log("got here");
                toRemoveID = clickedList[0];
                clickedList.shift();
                console.log(toRemoveID);
                $("#"+toRemoveID).toggleClass("whiteRow");
                $('#'+toRemoveID).removeClass("tanRow");
                clickedList.push($(this).attr('id'));
                console.log(clickedList);
                $(this).toggleClass("tanRow");
                classCount--;
            }
        }
    });

    $("#directionsButton").click(function(){

        if (clickedList.length==2){
        $.ajax({
            url:'/direct/'+clickedList[0]+'/'+clickedList[1],
            type:'POST',
            success:function(response){
            console.log("success");
            console.log(response);

            var path_route = new google.maps.Polyline({
                path:response,
                geodesic:true,
                strokeColor:'#550FFF',
                map:map
            });

            },
            error:function(error){
            console.log(error);}
        });
        }
        else{
            console.log("not enough classes");
        }
    });


    });




