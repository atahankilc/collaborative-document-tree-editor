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
            console.log('Connected');
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
            console.log(messages);
        }
        this.socket = socket
    }
}

window.onload = function () {
  ws = new Ws('localhost:5678');
}