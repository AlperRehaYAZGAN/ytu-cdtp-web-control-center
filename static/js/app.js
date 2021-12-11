var socket = io("/stream");
socket.on('connect', function () {
    console.log("Connected camera stream server.");
});

// update sensor values
socket.on('camera-listener', function (data) {
    console.log(data);
    $('#remote-video').attr('src', "data:image/jpeg;base64," + data);
});
socket.emit('init-camera-streaming', {});