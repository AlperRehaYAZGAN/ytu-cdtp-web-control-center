console.log("In socket section");
const socket = io('ws://localhost:5000');

socket.on('connect', () => {
    console.log("Connected to server");
});

let remote_imagebase64 = document.getElementById('remote-image');

// update sensor values
socket.on('camera-listener', function (data) {
    // replace the image element with the new base 64 image
    remote_imagebase64.src = "data:image/jpeg;base64," + data.data_image;
});