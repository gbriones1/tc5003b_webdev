var urlParams = new URLSearchParams(window.location.search);
let next = urlParams.get('next')

$(document).on('submit', 'form', function(e){
    e.preventDefault();
    let data = $('form').serialize()
    console.log(data)
    $.ajax({
        type: "POST",
        url: "/token",
        data: data,
        success: function (data){
            console.log("Success");
            console.log(data);
            localStorage.setItem('access_token', data.access_token);
            window.location.href = next || '/devices_list/'
        },
        error: function (data) {
            console.log('An error occurred.');
            console.log(data.responseJSON);
        },
    });
})