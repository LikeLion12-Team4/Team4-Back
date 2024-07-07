const videoElement = document.getElementById('webcam');
const canvasElement = document.getElementById('outputCanvas');
const canvasCtx = canvasElement.getContext('2d');

const pose = new Pose({
    locateFile: (file) => {
        return `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`;
    }
});

pose.setOptions({
    modelComplexity: 1,
    smoothLandmarks: true,
    enableSegmentation: false,
    minDetectionConfidence: 0.5,
    minTrackingConfidence: 0.5
});
pose.onResults(onResults);

const camera = new Camera(videoElement, {
    onFrame: async () => {
        await pose.send({image: videoElement});
    },
    width: 640,
    height: 480
});
camera.start();

const customConnections = [
    // 기본 Mediapipe 연결 추가
    ...POSE_CONNECTIONS
];

function onResults(results) {
    if (!results.poseLandmarks) {
        return;
    }

    // Clear the canvas
    canvasCtx.save();
    canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);

    // Draw the pose landmarks
    drawConnectors(canvasCtx, results.poseLandmarks, customConnections,
                   {color: '#00FF00', lineWidth: 4});
    drawLandmarks(canvasCtx, results.poseLandmarks,
                  {color: '#FF0000', lineWidth: 2});

    canvasCtx.restore();
}

// Ensure video element is visible and has dimensions set
videoElement.style.display = 'block';
videoElement.style.width = '100%';
videoElement.style.height = '100%';

// Check for permissions
navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
        videoElement.srcObject = stream;
        videoElement.play();
    })
    .catch((err) => {
        console.error("Error accessing webcam: " + err);
    });
