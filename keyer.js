// Initialize variables
let keydown = 0;
let dtime = 0;
let utime = 0;
let cwmsg = "";
let practiceMode = false;
//const sidetone = new Audio("https://github.com/hcarter333/pico-w-mem-keyer/raw/refs/heads/main/sidetone.wav");

const FREQUENCY = 440;

var DOT_TIME = 300;
var DASH_TIME = DOT_TIME * 3;
var SYMBOL_BREAK = DOT_TIME;
var LETTER_BREAK = DOT_TIME * 3;
var WORD_BREAK = DOT_TIME * 7;


let note_context;
let note_node;
let gain_node;

let audioContextInitialized = false;
let audioResume = false;

async function initializeAudioContext() {
  note_context = new AudioContext();
  //await note_context.resume();
  note_node = note_context.createOscillator();
  gain_node = note_context.createGain();
  note_node.frequency.value = FREQUENCY.toFixed(2);
  gain_node.gain.value = 0;
  note_node.connect(gain_node);
  gain_node.connect(note_context.destination);
  note_node.start();
  audioContextInitialized = true;
}
                           

//sidetone.loop = true; // Loop the sidetone
//sidetone.load();
if (!audioContextInitialized) {
  initializeAudioContext();
}

  
// Histogram variables
const dtimeHistogramBins = new Array(50).fill(0); // 50 bins for 0-500ms with 10ms width
const utimeHistogramBins = new Array(50).fill(0); // 50 bins for 0-500ms with 10ms width
let dtimeCanvas, dtimeCtx;
let utimeCanvas, utimeCtx;

// Function to initialize the histogram canvases
document.addEventListener("DOMContentLoaded", () => {
    const targetDiv = document.getElementById('metdivid');
    const container = document.createElement("div");
    container.style.display = "flex";
    container.style.flexDirection = "row";
    container.style.alignItems = "flex-start";
    container.style.justifyContent = "center";
    container.style.gap = "20px";
    container.style.width = "100%";
    targetDiv.appendChild(container);

    // Create a div for the histograms
    const histogramContainer = document.createElement("div");
    histogramContainer.style.display = "flex";
    histogramContainer.style.flexDirection = "column";
    histogramContainer.style.alignItems = "center";
    histogramContainer.style.width = "50%";
    container.appendChild(histogramContainer);

    // Add practice mode button
    const buttonDiv = document.createElement("div");
    buttonDiv.id = "buttonDiv";
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
  
    const generateButton = document.createElement("button");
    generateButton.textContent = "Generate Histogram Image";
    //generateButton.style.marginTop = "20px";
    generateButton.addEventListener("click", combineCanvasesAndGenerateDownloadLink);
    buttonDiv.appendChild(generateButton);

    // Add a button to buttonDiv that calls playKeySequence with cwmsg
    const playSequenceButton = document.createElement("button");
    playSequenceButton.id = "playSequenceButton";
    playSequenceButton.innerText = "Play Key Sequence";
    playSequenceButton.addEventListener("click", () => playKeySequence(cwmsg));
    buttonDiv.appendChild(playSequenceButton);


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
    //sidetone.currentTime = 0;
    //sidetone.play().catch(err => console.error("Error playing sidetone:", err));
    gain_node.gain.setTargetAtTime(0.1, 0, 0.001)
}

// Function to stop the sidetone
function stopSidetone() {
    //sidetone.pause();
    //sidetone.currentTime = 0; // Reset audio playback position
    gain_node.gain.setTargetAtTime(0, 0, 0.001)
}
  
function combineCanvasesAndGenerateDownloadLink() {
    // Get the two canvas elements
    const dtimeCanvas = document.getElementById("dtimeHistogramCanvas");
    const utimeCanvas = document.getElementById("utimeHistogramCanvas");
    const bDiv = document.getElementById('buttonDiv');
    if (!dtimeCanvas || !utimeCanvas) {
        console.error("Canvas elements not found.");
        return;
    }

    // Set up labels
    const dtimeLabel = "Dot/Dash Times";
    const utimeLabel = "wChar/btwnChar/btwnWord Times";

    // Create a new canvas to combine the two histograms and their labels
    const combinedCanvas = document.createElement("canvas");
    const labelHeight = 30; // Height for each label
    combinedCanvas.width = Math.max(dtimeCanvas.width, utimeCanvas.width); // Use the larger width
    combinedCanvas.height = dtimeCanvas.height + utimeCanvas.height + labelHeight * 2; // Combine heights with labels

    const ctx = combinedCanvas.getContext("2d");

    // Draw a white background
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, combinedCanvas.width, combinedCanvas.height);

    // Draw the first label
    ctx.fillStyle = "black";
    ctx.font = "16px sans-serif";
    ctx.textAlign = "center";
    ctx.fillText(dtimeLabel, combinedCanvas.width / 2, labelHeight - 5);

    // Draw the first canvas below the label
    ctx.drawImage(dtimeCanvas, 0, labelHeight);

    // Draw the second label
    ctx.fillText(utimeLabel, combinedCanvas.width / 2, dtimeCanvas.height + labelHeight * 2 - 5);

    // Draw the second canvas below the second label
    ctx.drawImage(utimeCanvas, 0, dtimeCanvas.height + labelHeight * 2);

    // Generate a Base64-encoded PNG image from the combined canvas
    const base64Image = combinedCanvas.toDataURL("image/png");

    // Create a download link
    let downloadLink = document.getElementById("downloadHistogramLink");
    if (!downloadLink) {
        downloadLink = document.createElement("a");
        downloadLink.id = "downloadHistogramLink";
        downloadLink.style.display = "block";
        downloadLink.style.marginTop = "20px";
        downloadLink.style.textAlign = "right"; // Right-align the link
        bDiv.appendChild(downloadLink);
    }

    downloadLink.href = base64Image;
    downloadLink.download = "combined_histogram.png"; // Default filename
    downloadLink.textContent = "Share your Results [png]";
}

// Function to handle key press
function keyPress() {
    console.log("Key pressed");
    if (keydown === 0) {
        dtime = performance.now();
        keydown = 1;
    }
    if(!audioResume){
      note_context.resume();
      audioResume = true;
    }
   if (utime !== 0) {
        utime = performance.now() - utime;
        console.log("Full utime: " + Math.round(utime));
        cwmsg += Math.round(utime) + "+";
        updateUtimeHistogram(Math.round(utime));
    }
    playSidetone();
}


// Function to handle key release
function keyRelease() {
    console.log("Key released");
    keydown = 0;
    dtime = performance.now() - dtime;
    console.log("Full dtime: " + Math.round(dtime));
    cwmsg += Math.round(dtime) + "+";
    updateDtimeHistogram(Math.round(dtime));

    utime = performance.now();
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

document.addEventListener("keydown", event => {
    if (event.key === "Alt" || event.key === "Tab") {
        return; // Ignore Alt and Tab keys
    }
    if (event.key !== "Escape" && keydown === 0) {
        keyPress();
    }
});

document.addEventListener("keyup", event => {
    if (event.key === "Alt" || event.key === "Tab") {
        return; // Ignore Alt and Tab keys
    }
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
  
// Function to alternate playing the sidetone based on keyDownUp intervals
function playKeySequence(keyDownUpString) {
    const keyDownUp = keyDownUpString.split("+").map(Number); // Convert the string into an array of numbers
    console.log(keyDownUpString)
    async function playSequence() {
        for (let i = 1; i < keyDownUp.length; i++) {
            if (isNaN(keyDownUp[i])) continue; // Skip invalid entries

            if (i % 2 === 0) {
                // Even index: play the sidetone
                playSidetone();
            } else {
                // Odd index: stop the sidetone
                stopSidetone();
            }

            // Wait for the duration specified by the current interval
            await new Promise(resolve => setTimeout(resolve, keyDownUp[i]));
        }

        // Ensure the sidetone is stopped after the sequence completes
        stopSidetone();
    }

    playSequence();
}
  
  

// Main function
function main() {
    console.log("Press keys to generate CW messages. Press Escape to send the message.");
}

main();
  
