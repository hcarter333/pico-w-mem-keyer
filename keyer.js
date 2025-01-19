0// Initialize variables
let keydown = 0;
let dtime = 0;
let utime = 0;
let cwmsg = "";
const sidetone = new Audio("sidetone.wav");
sidetone.loop = true; // Loop the sidetone

// Function to play the sidetone
function playSidetone() {
    sidetone.play().catch(err => console.error("Error playing sidetone:", err));
}

// Function to stop the sidetone
function stopSidetone() {
    sidetone.pause();
    sidetone.currentTime = 0; // Reset audio playback position
}

// Function to handle key press
function keyPress() {
    console.log("Key pressed");
    if (keydown === 0) {
        dtime = performance.now();
        keydown = 1;
        if (utime !== 0) {
            utime = performance.now() - utime;
            console.log("Full utime: " + Math.round(utime));
            cwmsg += Math.round(utime) + "+";
        }
        playSidetone();
    }
}

// Function to handle key release
function keyRelease() {
    console.log("Key released");
    keydown = 0;
    dtime = performance.now() - dtime;
    console.log("Full dtime: " + Math.round(dtime));
    cwmsg += Math.round(dtime) + "+";
    utime = performance.now();
    stopSidetone();
}

// Function to send the CW message to the server
function sendCWMessage() {
    console.log("Sending CW message: " + cwmsg);
    fetch(`http://192.168.4.1/light/skgo?msg=${cwmsg}`, { mode: 'no-cors' })
        .then(() => console.log("CW message sent successfully."))
        .catch(err => console.error("Error sending CW message:", err));

    cwmsg = "";
    dtime = 0;
    utime = 0;
    keydown = 0;
}

// Event listener for key presses and releases
document.addEventListener("keydown", event => {
    if (event.key !== "Escape") {
        if (keydown === 0) keyPress();
    }
});

document.addEventListener("keyup", event => {
    if (event.key !== "Escape") {
        keyRelease();
    } else {
        console.log("Escape key pressed. Exiting.");
        sendCWMessage();
    }
});

// Main function
function main() {
    console.log("Press keys to generate CW messages. Press Escape to send the message.");
}

// Run the main function
main();
