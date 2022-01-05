console.log("In socket section (anomaly.js)");
const socket = io();

socket.on('connect', () => {
    console.log("Connected to anomaly server");
});

// socket disconnect
socket.on('disconnect', () => {
    console.log("Disconnected from anomaly server");
});

// lcd btn-display button
const btnDisplay = document.getElementById('btn-display');
btnDisplay.onclick = function () {
    // get text content of input search box where id displaytext
    const displayText = document.getElementById('displaytext').value;
    socket.emit('show-display', { text : displayText });
};

// get buttons
const camera1tonormal = document.getElementById('camera1tonormal');
const camera1tofire = document.getElementById('camera1tofire');
const camera1tocarexit = document.getElementById('camera1tocarexit');
const camera1tohumanonroad = document.getElementById('camera1tohumanonroad');
    
const camera2tonormal = document.getElementById('camera2tonormal');
const camera2tofire = document.getElementById('camera2tofire');
const camera2tocarexit = document.getElementById('camera2tocarexit');
const camera2tohumanonroad = document.getElementById('camera2tohumanonroad');

// camera1status, camera1anomaly, camera1date spans
const camera1status = document.getElementById('camera1status');
const camera1anomaly = document.getElementById('camera1anomaly');
const camera1date = document.getElementById('camera1date');

const camera2status = document.getElementById('camera2status');
const camera2anomaly = document.getElementById('camera2anomaly');
const camera2date = document.getElementById('camera2date');

// anomaly-button-1, anomaly-button-1-test, anomaly-button-2, anomaly-button-2-test buttons
const anomalyButton1 = document.getElementById('anomaly-button-1');
const anomalyButton1Test = document.getElementById('anomaly-button-1-test');
const anomalyButton2 = document.getElementById('anomaly-button-2');
const anomalyButton2Test = document.getElementById('anomaly-button-2-test');

// if camera1tonormal button clicked
camera1tonormal.onclick = function () {
    console.log("camera1tonormal button clicked");
    socket.emit('camera-1-request', { to : 1 });
};

// if camera1tofire button clicked
camera1tofire.onclick = function () {
    console.log("camera1tofire button clicked");
    socket.emit('camera-1-request', { to : 2 });
};

// if camera1tocarexit button clicked
camera1tocarexit.onclick = function () {
    console.log("camera1tocarexit button clicked");
    socket.emit('camera-1-request', { to : 3 });
};

// if camera1tohumanonroad button clicked
camera1tohumanonroad.onclick = function () {
    console.log("camera1tohumanonroad button clicked");
    socket.emit('camera-1-request', { to : 4 });
};

// if camera2tonormal button clicked
camera2tonormal.onclick = function () {
    console.log("camera2tonormal button clicked");
    socket.emit('camera-2-request', { to : 1 });
};

// if camera2tofire button clicked
camera2tofire.onclick = function () {
    console.log("camera2tofire button clicked");
    socket.emit('camera-2-request', { to : 2 });
};

// if camera2tocarexit button clicked
camera2tocarexit.onclick = function () {
    console.log("camera2tocarexit button clicked");
    socket.emit('camera-2-request', { to : 3 });
};

// if camera2tohumanonroad button clicked
camera2tohumanonroad.onclick = function () {
    console.log("camera2tohumanonroad button clicked");
    socket.emit('camera-2-request', { to : 4 });
};

// if test1 button clicked
anomalyButton1Test.onclick = function () {
    console.log("anomalyButton1Test button clicked");
    socket.emit('anomaly-btn-1-test', {});
};

// if test2 button clicked
anomalyButton2Test.onclick = function () {
    console.log("anomalyButton2Test button clicked");
    socket.emit('anomaly-btn-2-test', {});
};


// anomaly-detected-1
socket.on('anomaly-detected-1', function (data) {
    console.log("Anomaly detected: ", data);
    // set color to red
    anomalyButton1.style.backgroundColor = '#ff0000';
    // set anomaly span content
    camera1anomaly.innerHTML = data.type;
    // set current isodate span content
    camera1date.innerHTML = new Date().toISOString();
    // if the anomaly button is clicked, send a message to the server
    anomalyButton1.onclick = function () {
        socket.emit('anomaly-button-1-clicked', {type : data.type});
    };

});

// anomaly-detected-2
socket.on('anomaly-detected-2', function (data) {
    console.log("Anomaly detected: ", data);
    // set color to red
    anomalyButton2.style.backgroundColor = '#ff0000';
    // set anomaly span content
    camera2anomaly.innerHTML = data.type;
    // set current isodate span content
    camera2date.innerHTML = new Date().toISOString();
    // if the anomaly button is clicked, send a message to the server
    anomalyButton2.onclick = function () {
        socket.emit('anomaly-button-2-clicked', {type : data.type});
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


// on camera-1-changed
socket.on('camera-1-changed', function (data) {
    console.log("Camera 1 changed: ", data);
    let changedTo = data.to;


    // if changed to normal make normal button class btn-primary and others btn-secondary
    if(changedTo == 1) {
        camera1tonormal.className = "btn btn-primary";
        camera1tofire.className = "btn btn-secondary";
        camera1tocarexit.className = "btn btn-secondary";
        camera1tohumanonroad.className = "btn btn-secondary";
        // set status span content
        camera1status.innerHTML = "LISTENING_NORMAL";
    } else if(changedTo == 2) {
        camera1tonormal.className = "btn btn-secondary";
        camera1tofire.className = "btn btn-primary";
        camera1tocarexit.className = "btn btn-secondary";
        camera1tohumanonroad.className = "btn btn-secondary";
        // set status span content
        camera1status.innerHTML = "LISTENING_FIRE";
    } else if(changedTo == 3) {
        camera1tonormal.className = "btn btn-secondary";
        camera1tofire.className = "btn btn-secondary";
        camera1tocarexit.className = "btn btn-primary";
        camera1tohumanonroad.className = "btn btn-secondary";
        // set status span content
        camera1status.innerHTML = "LISTENING_CAR_EXIT";
    } else if(changedTo == 4) {
        camera1tonormal.className = "btn btn-secondary";
        camera1tofire.className = "btn btn-secondary";
        camera1tocarexit.className = "btn btn-secondary";
        camera1tohumanonroad.className = "btn btn-primary";
        // set status span content
        camera1status.innerHTML = "LISTENING_HUMAN_ON_ROAD";
    }
});


// on camera-2-changed
socket.on('camera-2-changed', function (data) {
    console.log("Camera 2 changed: ", data);
    let changedTo = data.to;

    // if changed to normal make normal button class btn-primary and others btn-secondary
    if(changedTo == 1) {
        camera2tonormal.className = "btn btn-primary";
        camera2tofire.className = "btn btn-secondary";
        camera2tocarexit.className = "btn btn-secondary";
        camera2tohumanonroad.className = "btn btn-secondary";
        // set status span content
        camera2status.innerHTML = "LISTENING_NORMAL";
    } else if(changedTo == 2) {
        camera2tonormal.className = "btn btn-secondary";
        camera2tofire.className = "btn btn-primary";
        camera2tocarexit.className = "btn btn-secondary";
        camera2tohumanonroad.className = "btn btn-secondary";
        // set status span content
        camera2status.innerHTML = "LISTENING_FIRE";
    } else if(changedTo == 3) {
        camera2tonormal.className = "btn btn-secondary";
        camera2tofire.className = "btn btn-secondary";
        camera2tocarexit.className = "btn btn-primary";
        camera2tohumanonroad.className = "btn btn-secondary";
        // set status span content
        camera2status.innerHTML = "LISTENING_CAR_EXIT";
    } else if(changedTo == 4) {
        camera2tonormal.className = "btn btn-secondary";
        camera2tofire.className = "btn btn-secondary";
        camera2tocarexit.className = "btn btn-secondary";
        camera2tohumanonroad.className = "btn btn-primary";
        // set status span content
        camera2status.innerHTML = "LISTENING_HUMAN_ON_ROAD";
    }
});
