$(document).ready(() => {
    let socket = io.connect("http://localhost:5000");

    function insertMessage(data)
    {
        let messageBlock = `<div class="row message">
                            <div><p class="message-sent"></p></div>
                            </div>`
        let message = $(messageBlock);
        message.find(".message-sent").text(data.message);
        $("#messages").append(message);
    }

    socket.on("connect", () =>
    {
        console.log("connected");
    });

    socket.on("message", (data) =>
    {
        insertMessage(data)
    });

    $("#btnSend").on("click", () =>
    {
        // Use #message to select the message input field
        socket.emit("message_sent", $("#inputMessage").val());
        $("#inputMessage").val("");  // Clear the message input field after sending
    });
});
