$(document).ready(() => {
    let socket = io.connect("http://127.0.0.1:5000");

    socket.on("connect", () => {
        socket.send("Connection successful: 200");
    });

    socket.on("message", (data) => {
        $("#messages").append($("<p>").text(data));
    });

    $("#btnSend").on("click", () => {
        // Use #message to select the message input field
        socket.send("user:" + $("#inputMessage").val());
        $("#inputMessage").val("");  // Clear the message input field after sending
    });
});
