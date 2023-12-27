$(document).ready(() => {
    let socket = io.connect("http://localhost:5000");
    let target;  // target username to start a chat
    let currentUsername;
    $('#inputMessage').prop('disabled', true);

    function insertMessage(data)
    {
        let messageBlock = `
        <div class="row message">
            <h6 class="message-title"></h6>
            <div><p class="message-sent"></p></div>
        </div>`;
        let message = $(messageBlock);
        message.find(".message-title").text(data.username);
        message.find(".message-sent").text(data.message);
        $("#messages").append(message);
    }

    function startChat(targetUsername)
    {
        // Emit an event to the server to start a chat with the selected username
        $('#inputMessage').prop('disabled', false);
        socket.emit('start_chat', {target_username: targetUsername });
    }

    function sendMessage(targetUsername, message)
    {
        // Emit an event to the server to send a message in the chat
        socket.emit('send_message', {target_username: targetUsername, message });
        $('#inputMessage').val('');  // Clear the message input field after sending
    }

    function leaveChat(targetUsername)
    {
        $("#messages").html("");
        $('#inputMessage').prop('disabled', true);
        // Emit an event to the server to leave the chat
        socket.emit('leave_chat', {target_username: targetUsername });
    }

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

    // PREDEFINED:
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
    $("#start-chat3").on("click", () =>
    {
        if (target)
        {
            leaveChat(target)
        }
        target = $("#start-chat__name3").text().trim()
        startChat(target);
    });
    $("#start-chat4").on("click", () =>
    {
        if (target)
        {
            leaveChat(target)
        }
        target = $("#start-chat__name4").text().trim()
        startChat(target);
    });
    $("#start-chat5").on("click", () =>
    {
        if (target)
        {
            leaveChat(target)
        }
        target = $("#start-chat__name5").text().trim()
        startChat(target);
    });
    $("#start-chat6").on("click", () =>
    {
        if (target)
        {
            leaveChat(target)
        }
        target = $("#start-chat__name6").text().trim()
        startChat(target);
    });
    $("#start-chat7").on("click", () =>
    {
        if (target)
        {
            leaveChat(target)
        }
        target = $("#start-chat__name7").text().trim()
        startChat(target);
    });
    $("#start-chat8").on("click", () =>
    {
        if (target)
        {
            leaveChat(target)
        }
        target = $("#start-chat__name8").text().trim()
        startChat(target);
    });
    $("#start-chat9").on("click", () =>
    {
        if (target)
        {
            leaveChat(target)
        }
        target = $("#start-chat__name9").text().trim()
        startChat(target);
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
