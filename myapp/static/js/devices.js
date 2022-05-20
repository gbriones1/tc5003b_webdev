if (!localStorage.getItem('access_token')){
    window.location.replace('/login/?next=/otra_cosa/')
}
else{
    $.ajaxSetup({
        headers : {   
          'Authorization' : 'Bearer '+localStorage.getItem('access_token')
        }
    });
    $.getJSON('/device_type/', (data) => {
    }).fail(( jqxhr, textStatus, error) => {
        console.log(data)
        var err = textStatus + ", " + error;
        console.log( "Request Failed: " + err );
        if (error === 'Unauthorized'){
            window.location.replace('/login/?next=/devices_list/')
        }
    }).done(function( devices ) {
        console.log( devices );
        for (let index in devices){
            console.log('<li>'+devices[index].name+'</li>')
            $('ul.device-type-list').append('<li>'+devices[index].name+'</li>')
        }
    })
}

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