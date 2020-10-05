var server = "http://127.0.0.1:5000";
var send_msg = {'name':""};

function update_var()
{
    var name = String($("#name").val());
    send_msg['name']=name;
    console.log("update var")
}

function send_button()
{
    var appdir="/";
    update_var();
    console.log(send_msg)
    $.ajax({
            type: "POST",
            url:server + appdir,
            data: JSON.stringify(send_msg),
            dataType: 'json',
            contentType: 'application/json',
        }).done(function(data) {
            $('#Response').html(data['message']);
        });

}
