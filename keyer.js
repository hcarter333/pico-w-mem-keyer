// Initialize variables
let keydown = 0;
let dtime = 0;
let utime = 0;
let cwmsg = "";
let practiceMode = false;
const sidetone = new Audio("sidetone.wav");
sidetone.loop = true; // Loop the sidetone

// Histogram variables
const dtimeHistogramBins = new Array(50).fill(0); // 40 bins for 0-400ms with 10ms width
const utimeHistogramBins = new Array(50).fill(0); // 50 bins for 0-500ms with 10ms width
let dtimeCanvas, dtimeCtx;
let utimeCanvas, utimeCtx;

// Function to initialize the histogram canvases
document.addEventListener("DOMContentLoaded", () => {
    const container = document.createElement("div");
    container.style.display = "flex";
    container.style.flexDirection = "row";
    container.style.alignItems = "flex-start";
    container.style.justifyContent = "center";
    container.style.gap = "20px";
    container.style.width = "100%";
    document.body.appendChild(container);

    // Create a div for the histograms
    const histogramContainer = document.createElement("div");
    histogramContainer.style.display = "flex";
    histogramContainer.style.flexDirection = "column";
    histogramContainer.style.alignItems = "center";
    histogramContainer.style.width = "50%";
    container.appendChild(histogramContainer);

    // Add practice mode button
    const buttonDiv = document.createElement("div");
    buttonDiv.style.display = "flex";
    buttonDiv.style.flexDirection = "column";
    buttonDiv.style.alignItems = "center";
    buttonDiv.style.width = "20%";
    container.appendChild(buttonDiv);

    const button = document.createElement("button");
    button.id = "practiceModeButton";
    button.innerText = "Enable Practice Mode";
    button.addEventListener("click", togglePracticeMode);
    buttonDiv.appendChild(button);

    // Create title for dtime histogram
    const dtimeTitle = document.createElement("div");
    dtimeTitle.innerText = "Dot/Dash Times";
    dtimeTitle.style.textAlign = "center";
    dtimeTitle.style.fontSize = "16px";
    dtimeTitle.style.marginBottom = "10px";
    histogramContainer.appendChild(dtimeTitle);

    // Create canvas for dtime histogram
    dtimeCanvas = document.createElement("canvas");
    dtimeCanvas.id = "dtimeHistogramCanvas";
    dtimeCanvas.width = 435; // Width of canvas
    dtimeCanvas.height = (dtimeCanvas.width * 8) / 9; // Maintain 9:16 aspect ratio
    histogramContainer.appendChild(dtimeCanvas);
    dtimeCtx = dtimeCanvas.getContext("2d");
    drawDtimeHistogram();

    // Create title for utime histogram
    const utimeTitle = document.createElement("div");
    utimeTitle.innerText = "wChar/btwnChar/btwnWord Times";
    utimeTitle.style.textAlign = "center";
    utimeTitle.style.fontSize = "16px";
    utimeTitle.style.margin = "10px 0";
    histogramContainer.appendChild(utimeTitle);

    // Create canvas for utime histogram
    utimeCanvas = document.createElement("canvas");
    utimeCanvas.id = "utimeHistogramCanvas";
    utimeCanvas.width = 435; // Width of canvas
    utimeCanvas.height = (utimeCanvas.width * 8) / 9; // Maintain 9:16 aspect ratio
    histogramContainer.appendChild(utimeCanvas);
    utimeCtx = utimeCanvas.getContext("2d");
    drawUtimeHistogram();
});

// Function to draw the dtime histogram
function drawDtimeHistogram() {
    dtimeCtx.clearRect(0, 0, dtimeCanvas.width, dtimeCanvas.height); // Clear canvas

    // Set up histogram dimensions
    const barWidth = dtimeCanvas.width / dtimeHistogramBins.length;
    const maxCount = Math.max(...dtimeHistogramBins);

    // Draw bars
    dtimeHistogramBins.forEach((count, index) => {
        const barHeight = (count / maxCount) * dtimeCanvas.height;
        dtimeCtx.fillStyle = "blue";
        dtimeCtx.fillRect(index * barWidth, dtimeCanvas.height - barHeight, barWidth, barHeight);
    });

    // Draw axes
    dtimeCtx.strokeStyle = "black";
    dtimeCtx.beginPath();
    dtimeCtx.moveTo(0, dtimeCanvas.height);
    dtimeCtx.lineTo(dtimeCanvas.width, dtimeCanvas.height); // X-axis
    dtimeCtx.lineTo(dtimeCanvas.width, 0); // Y-axis
    dtimeCtx.stroke();

    // Add labels to the x-axis every 10 bins
    dtimeCtx.fillStyle = "black";
    dtimeCtx.font = "12px sans-serif";
    for (let i = 0; i <= dtimeHistogramBins.length; i += 10) {
        const xPosition = i * barWidth;
        dtimeCtx.fillText(i * 10, xPosition, dtimeCanvas.height - 5); // Label position
    }
}

// Function to draw the utime histogram
function drawUtimeHistogram() {
    utimeCtx.clearRect(0, 0, utimeCanvas.width, utimeCanvas.height); // Clear canvas

    // Set up histogram dimensions
    const barWidth = utimeCanvas.width / utimeHistogramBins.length;
    const maxCount = Math.max(...utimeHistogramBins);

    // Draw bars
    utimeHistogramBins.forEach((count, index) => {
        const barHeight = (count / maxCount) * utimeCanvas.height;
        utimeCtx.fillStyle = "green";
        utimeCtx.fillRect(index * barWidth, utimeCanvas.height - barHeight, barWidth, barHeight);
    });

    // Draw axes
    utimeCtx.strokeStyle = "black";
    utimeCtx.beginPath();
    utimeCtx.moveTo(0, utimeCanvas.height);
    utimeCtx.lineTo(utimeCanvas.width, utimeCanvas.height); // X-axis
    utimeCtx.lineTo(utimeCanvas.width, 0); // Y-axis
    utimeCtx.stroke();

    // Add labels to the x-axis every 10 bins
    utimeCtx.fillStyle = "black";
    utimeCtx.font = "12px sans-serif";
    for (let i = 0; i <= utimeHistogramBins.length; i += 10) {
        const xPosition = i * barWidth;
        utimeCtx.fillText(i * 10, xPosition, utimeCanvas.height - 5); // Label position
    }
}

// Function to update the dtime histogram with a new value
function updateDtimeHistogram(dtime) {
    if (dtime >= 0 && dtime <= 500) {
        const binIndex = Math.floor(dtime / 10); // Determine bin index
        dtimeHistogramBins[binIndex]++;
        drawDtimeHistogram();
    }
}

// Function to update the utime histogram with a new value
function updateUtimeHistogram(utime) {
    if (utime >= 0 && utime <= 500) {
        const binIndex = Math.floor(utime / 10); // Determine bin index
        utimeHistogramBins[binIndex]++;
        drawUtimeHistogram();
    }
}

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
    }
    playSidetone();
}

// Function to handle key release
function keyRelease() {
    console.log("Key released");
    keydown = 0;
    const releaseTime = performance.now();
    const currentDtime = releaseTime - dtime;
    console.log("Full dtime: " + Math.round(currentDtime));
    cwmsg += Math.round(currentDtime) + "+";
    updateDtimeHistogram(Math.round(currentDtime));

    if (utime !== 0) {
        const currentUtime = dtime - utime;
        console.log("Full utime: " + Math.round(currentUtime));
        updateUtimeHistogram(Math.round(currentUtime));
    }

    utime = releaseTime;
    stopSidetone();
}

// Function to send the CW message to the server
function sendCWMessage() {
    if (practiceMode) {
        console.log("Practice mode enabled. CW message not sent.");
        return;
    }

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

// Function to toggle practice mode
function togglePracticeMode() {
    practiceMode = !practiceMode;
    const status = practiceMode ? "enabled" : "disabled";
    console.log(`Practice mode ${status}.`);
    document.getElementById("practiceModeButton").innerText = practiceMode ? "Disable Practice Mode" : "Enable Practice Mode";
}

// Main function
function main() {
    console.log("Press keys to generate CW messages. Press Escape to send the message.");
}

main();
