var source = new EventSource(urls.events);

function createMessage(text) {
    var message = document.createElement("div");
    var text = document.createTextNode(text);

    message.appendChild(text);
    message.classList.add("flash", "message");

    setTimeout(function() {
        message.classList.remove("flash");
    }, 2000);

    return message;
}

source.onmessage = function(event) {
    var messageList = document.getElementById("messageList");
    messageList.appendChild(createMessage(event.data));
};

function send(message) {
    var request = new XMLHttpRequest();

    request.open("POST", urls.message, true);
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    request.send("message=" + encodeURIComponent(message));

    var newMessage = document.getElementById('newMessage');
    newMessage.value = "";
    newMessage.focus();
}
