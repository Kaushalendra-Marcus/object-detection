# api.py
"""
FastAPI-based REST API for YOLO object detection.
Supports image upload, video stream, and live webcam detection.
"""

from fastapi import FastAPI, File, UploadFile, WebSocket, HTTPException
from fastapi.responses import FileResponse, StreamingResponse, HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
from ultralytics import YOLO
import torch

# Monkeypatch ultralytics torch_safe_load to disable weights_only=True
# This avoids the need to allowlist dozens of custom classes in PyTorch 2.6+
import ultralytics.nn.tasks as ultralytics_tasks
_original_torch_safe_load = ultralytics_tasks.torch_safe_load

def torch_safe_load_patched(file):
    """Load checkpoint without weights_only restriction (trusted source)."""
    return torch.load(file, map_location='cpu', weights_only=False), file

ultralytics_tasks.torch_safe_load = torch_safe_load_patched

import io
from pathlib import Path
import asyncio
import json
from datetime import datetime
import os
import base64
import uuid
from typing import Dict, List

# Initialize FastAPI app
app = FastAPI(title="YOLO Object Detection API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use a relative results directory so it works on Render (not hardcoded Windows path)
MODEL_PATH = Path(__file__).parent / "weights" / "final.pt"

# Defer model loading to startup so we can prepare safe globals first and fail cleanly
model = None

@app.on_event("startup")
def load_model_event():
    global model
    try:
        model = YOLO(str(MODEL_PATH))
    except Exception as e:
        # Re-raise with context so deployment logs show why startup failed
        raise RuntimeError(f"Failed to load model {MODEL_PATH}: {e}") from e

# Configuration
CONFIDENCE_THRESHOLD = 0.5
MAX_DETECTIONS = 100
# Results directory under the project so it exists on Render and locally
RESULTS_DIR = Path(__file__).parent.parent / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Map file_id to actual filename (simple in-memory cache that survives within a process)
# For production, use a database or persistent file index
file_id_map: Dict[str, str] = {}

def cleanup_old_files(max_age_minutes: int = 60):
    """Clean up files older than specified minutes"""
    try:
        current_time = datetime.now()
        for filename in os.listdir(RESULTS_DIR):
            file_path = RESULTS_DIR / filename
            if file_path.is_file():
                file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                age_minutes = (current_time - file_time).total_seconds() / 60
                if age_minutes > max_age_minutes:
                    os.remove(file_path)
                    print(f"Cleaned up old file: {filename}")
    except Exception as e:
        print(f"Cleanup error: {e}")

@app.get("/")
async def root():
    """Root endpoint - returns API info"""
    return {
        "name": "YOLO Object Detection API",
        "version": "1.0.0",
        "model": "final.pt",
        "classes": model.names,
        "endpoints": [
            "/docs - Swagger API documentation",
            "/detect/image - Detect objects in image",
            "/detect/video - Detect objects in video",
            "/download/{file_id} - Download detected file",
            "/detect/webcam - Live webcam detection (WebSocket)",
            "/health - Health check",
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": True,
        "model_path": str(MODEL_PATH),
        "classes": len(model.names),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/model-info")
async def model_info():
    """Get model information"""
    return {
        "model_name": "final.pt",
        "model_path": str(MODEL_PATH),
        "classes": model.names,
        "num_classes": len(model.names),
        "confidence_threshold": CONFIDENCE_THRESHOLD
    }

@app.post("/detect/image")
async def detect_image(
    file: UploadFile = File(...),
    confidence: float = CONFIDENCE_THRESHOLD
):
    """
    Detect objects in an uploaded image.
    
    Parameters:
    - file: Image file (jpg, png, etc.)
    - confidence: Detection confidence threshold (0.0-1.0)
    
    Returns:
    - JSON with detections and download URL
    """
    try:
        # Clean up old files first
        cleanup_old_files(30)  # Clean files older than 30 minutes
        
        # Read uploaded file
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Run detection
        results = model(img, conf=confidence)
        result = results[0]
        
        # Extract detections
        detections = []
        for box in result.boxes:
            detection = {
                "class_id": int(box.cls[0]),
                "class_name": model.names[int(box.cls[0])],
                "confidence": float(box.conf[0]),
                "bbox": {
                    "x1": float(box.xyxy[0][0]),
                    "y1": float(box.xyxy[0][1]),
                    "x2": float(box.xyxy[0][2]),
                    "y2": float(box.xyxy[0][3]),
                }
            }
            detections.append(detection)
        
        # Draw bounding boxes on image
        annotated_img = result.plot()
        
        # Save annotated image with unique ID
        file_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"detection_{timestamp}_{file_id}.jpg"
        output_path = RESULTS_DIR / output_filename
        
        cv2.imwrite(str(output_path), annotated_img)
        
        # Store mapping (for quick lookup)
        file_id_map[file_id] = output_filename
        
        # Generate download URL
        download_url = f"/download/{file_id}"
        
        return {
            "status": "success",
            "detections": detections,
            "num_detections": len(detections),
            "download_url": download_url,
            "file_id": file_id,
            "timestamp": timestamp,
            "message": "Use the download_url to download the annotated image"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{file_id}")
async def download_file(file_id: str):
    """
    Download detected image file.
    File is looked up by UUID; if found, it's served immediately.
    """
    try:
        # Check if file_id is in the map (quick lookup)
        if file_id in file_id_map:
            output_filename = file_id_map[file_id]
            file_path = RESULTS_DIR / output_filename
        else:
            # Fallback: try to find file by UUID in results directory
            # (handles cases where the map wasn't populated)
            matching_files = list(RESULTS_DIR.glob(f"*_{file_id}.jpg"))
            if not matching_files:
                matching_files = list(RESULTS_DIR.glob(f"*_{file_id}.mp4"))
            
            if not matching_files:
                raise HTTPException(status_code=404, detail="File not found")
            
            file_path = matching_files[0]
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found on server")
        
        # Determine media type based on file extension
        suffix = file_path.suffix.lower()
        if suffix == ".jpg" or suffix == ".jpeg":
            media_type = "image/jpeg"
        elif suffix == ".mp4":
            media_type = "video/mp4"
        else:
            media_type = "application/octet-stream"
        
        # Return the file as response (client downloads it)
        return FileResponse(
            path=file_path,
            media_type=media_type,
            filename=f"detected_{file_id}{suffix}"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download error: {str(e)}")
    try:
        if file_id not in file_metadata:
            raise HTTPException(status_code=404, detail="File not found or already downloaded")
        
        file_info = file_metadata[file_id]
        file_path = Path(file_info["filepath"])
        
        if not file_path.exists():
            # Remove from metadata if file doesn't exist
            del file_metadata[file_id]
            raise HTTPException(status_code=404, detail="File not found on server")
        
        # Determine media type
        if file_info["type"] == "image":
            media_type = "image/jpeg"
        elif file_info["type"] == "video":
            media_type = "video/mp4"
        else:
            media_type = "application/octet-stream"
        
        # Create response with file
        response = FileResponse(
            path=file_path,
            media_type=media_type,
            filename=file_info["filename"]
        )
        
        # Schedule file deletion after response is sent
        @response.background
        def delete_file_after_download():
            try:
                if file_path.exists():
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")
                # Remove from metadata
                if file_id in file_metadata:
                    del file_metadata[file_id]
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download error: {str(e)}")

@app.post("/detect/video")
async def detect_video(
    file: UploadFile = File(...),
    confidence: float = CONFIDENCE_THRESHOLD
):
    """Detect objects in uploaded video"""
    try:
        # Clean up old files first
        cleanup_old_files(30)
        
        file_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_video = RESULTS_DIR / f"temp_{timestamp}_{file_id}.mp4"

        contents = await file.read()
        with open(temp_video, "wb") as f:
            f.write(contents)

        cap = cv2.VideoCapture(str(temp_video))
        if not cap.isOpened():
            raise HTTPException(status_code=400, detail="Invalid video file")

        # Original FPS and resolution
        orig_fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Reduce frame rate for faster processing
        skip_rate = 3
        fps = orig_fps / skip_rate

        output_filename = f"detected_{timestamp}_{file_id}.mp4"
        output_path = RESULTS_DIR / output_filename
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))

        frame_count = 0
        processed_frames = 0
        detections_list = []

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1

            # Skip frames for lower FPS
            if frame_count % skip_rate != 0:
                continue

            results = model(frame, conf=confidence)
            result = results[0]

            for box in result.boxes:
                detections_list.append({
                    "frame": processed_frames,
                    "class": model.names[int(box.cls[0])],
                    "confidence": float(box.conf[0])
                })

            annotated_frame = result.plot()
            out.write(annotated_frame)
            processed_frames += 1

        cap.release()
        out.release()
        
        # Clean up temp file
        if temp_video.exists():
            os.remove(temp_video)

        # Store file mapping
        file_id_map[file_id] = output_filename

        # Generate download URL
        download_url = f"/download/{file_id}"

        return {
            "status": "success",
            "download_url": download_url,
            "file_id": file_id,
            "frames_processed": processed_frames,
            "total_frames": frame_count,
            "original_fps": orig_fps,
            "processed_fps": fps,
            "timestamp": timestamp,
            "message": "Use the download_url to download the annotated video"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/webcam")
async def websocket_webcam(websocket: WebSocket):
    """
    WebSocket endpoint for live webcam detection.
    Connect and receive real-time detection frames as JPEG images.
    """
    await websocket.accept()
    cap = cv2.VideoCapture(0)  # Default webcam
    
    if not cap.isOpened():
        await websocket.send_json({"error": "Cannot open webcam"})
        await websocket.close()
        return
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Resize frame for faster processing
            frame = cv2.resize(frame, (640, 480))
            
            # Run detection
            results = model(frame, conf=CONFIDENCE_THRESHOLD)
            result = results[0]
            
            # Extract detections
            detections = []
            for box in result.boxes:
                detections.append({
                    "class": model.names[int(box.cls[0])],
                    "confidence": float(box.conf[0]),
                    "bbox": [float(x) for x in box.xyxy[0]]
                })
            
            # Draw annotations
            annotated_frame = result.plot()
            
            # Encode frame to JPEG
            _, buffer = cv2.imencode('.jpg', annotated_frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
            frame_data = buffer.tobytes()
            
            # Send frame and detections
            await websocket.send_json({
                "type": "detections",
                "count": len(detections),
                "objects": detections,
                "timestamp": datetime.now().isoformat()
            })
            
            # Send image as base64
            await websocket.send_text(f"data:image/jpeg;base64,{base64.b64encode(frame_data).decode()}")
            
            await asyncio.sleep(0.03)  # ~30 FPS
    
    except Exception as e:
        await websocket.send_json({"error": str(e)})
    finally:
        cap.release()
        await websocket.close()

@app.get("/detect/webcam-html")
async def webcam_html():
    """
    HTML page for live webcam detection with real-time stream.
    """
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Live Webcam Detection</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
                background: #1e1e1e;
                color: white;
            }
            .container {
                display: flex;
                gap: 20px;
                width: 90%;
                max-width: 1400px;
            }
            .video-section {
                flex: 1;
            }
            .info-section {
                flex: 1;
                background: #2d2d2d;
                padding: 20px;
                border-radius: 10px;
                overflow-y: auto;
                max-height: 600px;
            }
            img {
                width: 100%;
                border-radius: 10px;
                background: #000;
            }
            button {
                padding: 10px 20px;
                margin: 10px 0;
                background: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
            }
            button:hover {
                background: #0056b3;
            }
            button:disabled {
                background: #ccc;
                cursor: not-allowed;
            }
            .detection-item {
                background: #1e1e1e;
                padding: 10px;
                margin: 5px 0;
                border-left: 3px solid #007bff;
                border-radius: 5px;
            }
            h1 { margin: 20px 0; }
            h2 { margin-top: 0; }
        </style>
    </head>
    <body>
        <h1>🎥 Live Webcam Object Detection</h1>
        
        <div class="container">
            <div class="video-section">
                <img id="stream" src="" alt="Stream">
                <button id="startBtn" onclick="startStream()">Start Stream</button>
                <button id="stopBtn" onclick="stopStream()" disabled>Stop Stream</button>
            </div>
            
            <div class="info-section">
                <h2>Detections</h2>
                <p>Status: <span id="status" style="color: #ff6b6b;">Disconnected</span></p>
                <div id="detections"></div>
            </div>
        </div>
        
        <script>
            let ws = null;
            let isStreaming = false;
            
            function startStream() {
                if (isStreaming) return;
                
                ws = new WebSocket("ws://" + window.location.host + "/ws/webcam");
                ws.onopen = () => {
                    document.getElementById('status').textContent = 'Connected';
                    document.getElementById('status').style.color = '#51cf66';
                    document.getElementById('startBtn').disabled = true;
                    document.getElementById('stopBtn').disabled = false;
                    isStreaming = true;
                };
                
                ws.onmessage = (event) => {
                    if (event.data.startsWith('data:image')) {
                        document.getElementById('stream').src = event.data;
                    } else {
                        const data = JSON.parse(event.data);
                        updateDetections(data);
                    }
                };
                
                ws.onerror = () => {
                    document.getElementById('status').textContent = 'Error';
                    document.getElementById('status').style.color = '#ff6b6b';
                };
                
                ws.onclose = () => {
                    document.getElementById('status').textContent = 'Disconnected';
                    document.getElementById('status').style.color = '#ff6b6b';
                    document.getElementById('startBtn').disabled = false;
                    document.getElementById('stopBtn').disabled = true;
                    isStreaming = false;
                };
            }
            
            function stopStream() {
                if (ws) {
                    ws.close();
                }
            }
            
            function updateDetections(data) {
                const container = document.getElementById('detections');
                if (data.count === 0) {
                    container.innerHTML = '<p style="color: #aaa;">No detections</p>';
                } else {
                    container.innerHTML = data.objects.map(obj => `
                        <div class="detection-item">
                            <strong>${obj.class}</strong><br>
                            Confidence: ${(obj.confidence * 100).toFixed(1)}%
                        </div>
                    `).join('');
                }
            }
        </script>
    </body>
    </html>
    """)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)