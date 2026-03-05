const socket = new WebSocket(
'ws://' + window.location.host + '/ws/notifications/'
);

socket.onmessage = function(e){

const data = JSON.parse(e.data);

const notification = document.createElement("div");

notification.style.position="fixed";
notification.style.top="20px";
notification.style.right="20px";
notification.style.background="#2ecc71";
notification.style.color="white";
notification.style.padding="10px 15px";
notification.style.borderRadius="5px";

notification.innerText = data.message;

document.body.appendChild(notification);

setTimeout(()=>{
notification.remove();
},4000);

};