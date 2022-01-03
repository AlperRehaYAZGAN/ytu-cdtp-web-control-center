console.log("In socket section (anomaly.js)");
const socket = io();

socket.on('connect', () => {
    console.log("Connected to anomaly server");
});

// socket disconnect
socket.on('disconnect', () => {
    console.log("Disconnected from anomaly server");
});

// anomaly-detected-1
socket.on('anomaly-detected-1', function (data) {
    // console.log("Anomaly detected: " + data.anomaly);
    console.log("Anomaly button clicked 1");
    // set button to red
    document.getElementById('anomaly-button-1').style.backgroundColor = 'red';
    // set text to "Anomaly detected"
    document.getElementById('anomaly-button-1').innerHTML = "Anomaly detected";
    // if the anomaly button is clicked, send a message to the server
    document.getElementById('anomaly-button-1').onclick = function () {
        // set color to normal
        document.getElementById('anomaly-button-1').style.backgroundColor = '#00ff00';
        socket.emit('anomaly-button-1-clicked', {type : data});
    };
});

// anomaly-detected-2
socket.on('anomaly-detected-2', function (data) {
    // set button to red
    document.getElementById('anomaly-button-2').style.backgroundColor = 'red';
    // set text to "Anomaly detected"
    document.getElementById('anomaly-button-2').innerHTML = "Anomaly detected";
    // if the anomaly button is clicked, send a message to the server
    document.getElementById('anomaly-button-2').onclick = function () {
        // set color to normal
        document.getElementById('anomaly-button-2').style.backgroundColor = '#00ff00';
        socket.emit('anomaly-button-2-clicked', { type: data});
    };
});


document.getElementById('anomaly-button-1').onclick = function () {
    // buton clicked log
    console.log("Anomaly button clicked 1");
    // set color to normal
    document.getElementById('anomaly-button-1').style.backgroundColor = '#00ff00';
    socket.emit('anomaly-button-1-clicked', { type: "TEST"});
};

document.getElementById('anomaly-button-2').onclick = function () {
    // buton clicked log
    console.log("Anomaly button clicked 2");
    // set color to normal
    document.getElementById('anomaly-button-2').style.backgroundColor = '#00ff00';
    socket.emit('anomaly-button-2-clicked', { type: "TEST"});
};
