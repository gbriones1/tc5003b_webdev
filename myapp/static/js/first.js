$(document).on('submit', 'form', function(e){
    e.preventDefault();
    let data = JSON.stringify({"name":$('form').serializeArray()[0].value})
    console.log(data)
    $.ajax({
        type: "POST",
        url: "/device_type",
        data: data,
        success: function (){
            console.log("Success")
            window.location.reload()
        },
        contentType: "application/json",
        dataType: "json"
        });
})