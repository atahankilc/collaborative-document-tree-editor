class Ws {
    constructor(ip_port) {
    	this.socket = undefined;
    	this.ip_port = ip_port;
    	this.create_websocket();
    }

    create_websocket() {
        if (this.socket)
            this.socket.close();

        var socket = new WebSocket('ws://' + this.ip_port);

        socket.onopen = function() {
            console.log('Connected!!!');
        }

        socket.onerror = function() {
            console.log('Error');
        }

        socket.onclose = function() {
            console.log('Closed');
            ws.socket = undefined;
            setTimeout(() => {
                if (! ws.socket ) {
                    ws.createwebsocket();
                } }, 5000);
        }

        socket.onmessage = function wseventhandler (event) {
            var messages = event.data;
            let notification = document.getElementById("notification")
            console.log(notification)
            console.log(messages);
            notification.innerHTML = messages
        }
        this.socket = socket
    }
}

window.onload = async function () {
    const response = await fetch('http://localhost:8000/service/ws_port/')
    const data = await response.json()
    console.log(data)
    ws = new Ws(`localhost:${data['ws_port']}`);
}