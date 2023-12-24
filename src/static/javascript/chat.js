$(document).ready(() => {
    let socket = io.connect("http://localhost:5000");
    let target;  // target username to start a chat
    let currentUsername;

    function insertMessage(data)
    {
        let messageBlock = `
        <div class="row message">
            <h6 class="message-title"></h6>
            <div><p class="message-sent"></p></div>
        </div>`;
        let message = $(messageBlock);
        message.find(".message-title").text(data.user);
        message.find(".message-sent").text(data.message);
        $("#messages").append(message);
    }

    function startChat(targetUsername)
    {
        // Emit an event to the server to start a chat with the selected username
        socket.emit('start_chat', {target_username: targetUsername });
    }

    function sendMessage(targetUsername, message)
    {
        // Emit an event to the server to send a message in the chat
        socket.emit('send_message', {target_username: targetUsername, message });
        $("#inputMessage").val("");  // Clear the message input field after sending
    }

    function leaveChat(targetUsername)
    {
        // Emit an event to the server to leave the chat
        //TO-DO CLEAN CHAT AFTER LEAVING
        $('#messages').innerHTML = '';
        socket.emit('leave_chat', {target_username: targetUsername });
    }

    // Event listener for receiving chat messages
    socket.on('chat_message', (data) =>
    {
        console.log(data.message);
        // Handle the received message, e.g., display it in the UI
        insertMessage(data)
    });

    // Start a chat when a button is clicked
    $("#start-chat").on("click", () =>
    {
        if (target)
        {
            leaveChat(target)
        }
        target = $("#start-chat__name").text().trim()
        startChat(target);
    });
    $("#start-chat2").on("click", () =>
    {
        if (target)
        {
            leaveChat(target)
        }
        target = $("#start-chat__name2").text().trim()
        startChat(target);
    });

    // Send a message when a button is clicked
    $("#btnSend").on("click", () =>
    {
        if ($("#inputMessage").val() != "")
        {
            sendMessage(target, $("#inputMessage").val());
        }
    });

    // Leave the chat when a button is clicked
    $("#leaveChatBtn").on("click", () =>
    {
        leaveChat(target);
    });

//    socket.on("connect", () =>
//    {
//        console.log("connected");
//    });
//
//    socket.on("message", (data) =>
//    {
//        insertMessage(data)
//    });
//
//    $("#btnSend").on("click", () =>
//    {
//        // Use #message to select the message input field
//        socket.emit("message_sent", $("#inputMessage").val());
//        $("#inputMessage").val("");  // Clear the message input field after sending
//    });
});
