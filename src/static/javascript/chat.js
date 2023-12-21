$(document).ready(() => {
    let socket = io.connect("http://localhost:5000");
    let username = "";

    function insertMessage(data, received = false)
    {
        let messageBlock = `<div class="row message">
                            <div><p class="message-sent"></p></div>
                            </div>`
        let message = $(messageBlock);
        message.find(".message-sent").text(data.message);
        // if the message is not sent but received
        if (received)
        {
            message.find(".message-sent").removeClass("message-sent").addClass("message-recived");
        }
        $("#messages").append(message);
    }

    socket.on("connect", () =>
    {
        //socket.send("Connection successful: 200");
        console.log("connected");
    });

    socket.on("login", (data) =>
    {
        username = data;
    });

    socket.on("message", (data) =>
    {
        console.log(username)
        if (data.user === username) {
            insertMessage(data);
        } else {
            insertMessage(data, true);
        }
    });

    $("#btnSend").on("click", () =>
    {
        // Use #message to select the message input field
        socket.emit("message_sent", $("#inputMessage").val());
        $("#inputMessage").val("");  // Clear the message input field after sending
    });
});
