$(document).ready(() => {
    let socket = io.connect("http://localhost:5000");
    let username = "";

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
            $("#messages").append($("<p class='txtMessageSent'>").text(data.message));
        } else {
            $("#messages").append($("<p class='txtMessageReceived'>").text(data.message));
        }
    });

    $("#btnSend").on("click", () =>
    {
        // Use #message to select the message input field
        socket.emit("message_sent", $("#inputMessage").val());
        $("#inputMessage").val("");  // Clear the message input field after sending
    });
});
