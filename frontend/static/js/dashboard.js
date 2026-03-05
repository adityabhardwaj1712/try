const socket = new WebSocket(
'ws://' + window.location.host + '/ws/notifications/'
);

socket.onmessage = function(e) {

const data = JSON.parse(e.data);

const notification = document.createElement("div");

notification.className =
"bg-green-500 text-white px-3 py-2 rounded fixed top-4 right-4";

notification.innerText = data.message;

document.body.appendChild(notification);

setTimeout(() => {
notification.remove();
}, 4000);

};
