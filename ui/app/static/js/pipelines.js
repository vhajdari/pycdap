$(document).ready(function () {
    function getPipelines(){
        $("#getPipelinesBtn").click(function(){
            $.ajax({
                type: "POST",
                url: "/",
                data: $("#pipelines").serialize(),
                success: function(response){
//                    $("#pipeline").modal('hide'); //hide popup
                    console.log(response);
//                    $(location).attr('href', '/');
                },
                error: function(){
                    errorAlert()
                }
            });
        });
    }

    getPipelines()
});