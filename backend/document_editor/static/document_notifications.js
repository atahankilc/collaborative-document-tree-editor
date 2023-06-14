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

        socket.onmessage = async function wseventhandler (event) {
            var messages = event.data;
            document.getElementById("notification").innerHTML = messages
            const response = await fetch('http://localhost:8000/service/document_xml/')
            const data = await response.json()
            document.getElementById("server_response").innerHTML = data.server_response
        }
        this.socket = socket
    }
}

window.onload = async function () {
    await new Promise(r => setTimeout(r, 500));
    const response = await fetch('http://localhost:8000/service/ws_port/')
    const data = await response.json()
    console.log(data)
    ws = new Ws(`localhost:${data['ws_port']}`);
}