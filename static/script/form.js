$(document).ready(function() {

    $("input[name='exampleRadios']").click(function(){
        const property = $(this).prop("value")
        if(property === 'option1'){
            $("#selectSensor,#sensorLoc,#minThresh,#maxThresh").show();
            $(":input").show();
            $("#submitBtn").prop("value","Modify Device");

        }
        else if(property === 'option2'){
            $("#selectSensor,#sensorLoc,#minThresh,#maxThresh").hide();
            $("#submitBtn").prop("value","Delete Device");
        }
    });
    $("#submitBtn").click(()=>{
    if($('#submitBtn').prop("value") === "Modify Device"){
    alert("Device Modified successfully!");
    }
    else if($("#submitBtn").prop("value") === "Delete Device"){
    alert("Device Deleted successfully!");
    }
    });
  });
