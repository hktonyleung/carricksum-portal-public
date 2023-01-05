console.log("Sanity check from room.js.");

const roomName = JSON.parse(document.getElementById('roomName').textContent);

let chatLog = document.querySelector("#chatLog");
let chat = document.querySelector("#chat");
let chatMessageInput = document.querySelector("#chatMessageInput");
let chatMessageSend = document.querySelector("#chatMessageSend");
let onlineUsersSelector = document.querySelector("#onlineUsersSelector");

let my_username = JSON.parse(document.getElementById("my_username").textContent);;

// adds a new option to 'onlineUsersSelector'
function onlineUsersSelectorAdd(value) {
    if (document.querySelector("option[value='" + value + "']")) return;
    let newOption = document.createElement("option");
    newOption.value = value;
    newOption.innerHTML = value;
    onlineUsersSelector.appendChild(newOption);
}

// removes an option from 'onlineUsersSelector'
function onlineUsersSelectorRemove(value) {
    let oldOption = document.querySelector("option[value='" + value + "']");
    if (oldOption !== null) oldOption.remove();
}

// focus 'chatMessageInput' when user opens the page
chatMessageInput.focus();

// submit if the user presses the enter key
chatMessageInput.onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter key
        chatMessageSend.click();
    }
};

// clear the 'chatMessageInput' and forward the message
chatMessageSend.onclick = function() {
    if (chatMessageInput.value.length === 0) return;
    chatSocket.send(JSON.stringify({
        "message": chatMessageInput.value,
    }));
    chatMessageInput.value = "";
};

let chatSocket = null;

function connect() {
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";

    chatSocket = new WebSocket(ws_scheme + "://" + window.location.host + "/ws/chat/" + roomName + "/");

    chatSocket.onopen = function(e) {
        console.log("Successfully connected to the WebSocket.");
    }

    chatSocket.onclose = function(e) {
        console.log("WebSocket connection closed unexpectedly. Trying to reconnect in 2s...");
        setTimeout(function() {
            console.log("Reconnecting...");
            connect();
        }, 2000);
    };

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        console.log(data);

        switch (data.type) {
            case "chat_message":
                //chatLog.value += data.message + "\n";
                receive_new_message(data);
                break;
            case "online_member_notify":
                user_online(data);
                break;
            case "offline_member_notify":
                user_offline(data);
                break;
            default:
                console.error("Unknown message type!");
                break;
        }

        // scroll 'chatLog' to the bottom
        chat.scrollTop = chat.scrollHeight;
    };

    chatSocket.onerror = function(err) {
        console.log("WebSocket encountered an error: " + err.message);
        console.log("Closing the socket.");
        chatSocket.close();
    }
}
connect();

function user_online(data){
    console.log('user_online: ' + data);
    var user_id = data.user_id;
    var username = data.username;
    var e = document.querySelector('#offline_' + user_id);
    console.log(e);
    if (e !== null && data !== ''){
        e.parentElement.removeChild(e);  
    } 
    e = document.querySelector('#online_' + user_id);
    if (e == null){
        // Add new online user
        //<li class="clearfix" id="online_{{online.user.id}}">
        //<div class="about">
        //    <div class="name">{{online.user.username}}</div>
        //    <div class="status"> <i class="fa fa-circle online"></i> online </div>                                            
        //</div>
        //</li> 
        var new_li = document.createElement('li');
        new_li.className = "clearfix";
        new_li.id = "online_" + user_id;
        new_div = document.createElement('div');
        new_div.className = "about";
        
        new_name_div = document.createElement('div');
        new_name_div.className = "name"
        new_name_div.innerHTML = username;

        new_status_div = document.createElement('div');
        new_status_div.className = "status";
        new_status_div.innerHTML = '<i class="fa fa-circle online"></i> online'

        new_div.append(new_name_div);
        new_div.append(new_status_div);

        new_li.append(new_div);

        document.querySelector('#plist_on_ul').prepend(new_li);

    }


}
function user_offline(data){
    console.log('user_offline: ' + data);
    var user_id = data.user_id;
    var username = data.username;
    var offline_datetime = data.offline_datetime;

    var e = document.querySelector('#online_' + user_id);
    console.log(e);
    if (e !== null && data !== ''){
        e.parentElement.removeChild(e);  
    } 
    e = document.querySelector('#offline_' + user_id);
    if (e == null){
        // Add new offline user
        //<li class="clearfix" id="offline_{{offline.user.id}}">
        //      <div class="about">
        //          <div class="name">{{offline.user.username}}</div>
        //          <div class="status"> <i class="fa fa-circle offline"></i> offline at {{offline.last_offline_time}} </div>                                            
        //      </div>
        //</li> 
        var new_li = document.createElement('li');
        new_li.className = "clearfix";
        new_li.id = "offline_" + user_id;
        new_div = document.createElement('div');
        new_div.className = "about";
        
        new_name_div = document.createElement('div');
        new_name_div.className = "name"
        new_name_div.innerHTML = username;

        new_status_div = document.createElement('div');
        new_status_div.className = "status";
        new_status_div.innerHTML = '<i class="fa fa-circle offline"></i> offline at ' + offline_datetime

        new_div.append(new_name_div);
        new_div.append(new_status_div);

        new_li.append(new_div);

        document.querySelector('#plist_off_ul').prepend(new_li);

    }

    
}


function receive_new_message(data){
/*
From other ppl
<li class="clearfix">
    <div class="message-data">
        <span class="message-data-time">10:12 AM, Today by <b>Tony Leung</b></span>
    </div>
    <div class="message my-message">Are we meeting today?</div>                                    
</li> 
From myself
<li class="clearfix">
    <div class="message-data text-right">
        <span class="message-data-time">10:10 AM, Today</span>
    </div>
    <div class="message other-message float-right"> Hi Aiden, how are you? How is the project coming along? </div>
</li>
*/
    message = data.message;
    username = data.username;
    receive_datetime = data.receive_datetime;

    new_li = document.createElement('li');
    new_li.className = "clearfix";
    
    new_time_div = document.createElement('div');
    //console.log(username);
    if (my_username == username){
        new_time_div.className = "message-data text-end";
    } else {
        new_time_div.className = "message-data";
    }

    new_span = document.createElement('span');
    new_span.className = "message-data-time";
    if (my_username == username){
        new_span.innerHTML = receive_datetime;
    } else {
        new_span.innerHTML = receive_datetime + " by <b>" + username + "</b>";
    }
    new_time_div.appendChild(new_span);
    new_message_div = document.createElement('div');

    if (my_username == username){
        new_message_div.className = "message my-message float-right"
        
    } else {
        new_message_div.className = "message other-message"
    }
    new_message_div.innerHTML = message;
    
    new_li.appendChild(new_time_div);
    new_li.appendChild(new_message_div);

    document.querySelector('#chatlog').append(new_li);

}