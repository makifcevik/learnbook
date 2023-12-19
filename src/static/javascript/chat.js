$(document).ready(() => {
    let socket = io.connect("http://localhost:5000");

    socket.on("connect", () => {
        //socket.send("Connection successful: 200");
    });

    socket.on("message", (data) => {
        $("#messages").append($("<p class='txtMessage'>").text(data));
    });

    $("#btnSend").on("click", () => {
        // Use #message to select the message input field
        socket.send($("#inputMessage").val());
        $("#inputMessage").val("");  // Clear the message input field after sending
    });
});
