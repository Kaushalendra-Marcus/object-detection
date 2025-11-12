# YOLO Object Detection API

A production-ready REST API for real-time object detection using YOLO. Features image detection, video processing, and live webcam streaming with a modern web dashboard.

## 🚀 Features

- **REST API** - FastAPI-based REST endpoints for easy integration
- **Image Detection** - Upload and detect objects in images
- **Video Processing** - Batch process videos with frame-by-frame detection
- **Live Webcam Stream** - Real-time WebSocket-based webcam detection
- **Web Dashboard** - Beautiful, responsive UI for all features
- **Docker Support** - Easy deployment with Docker & Docker Compose
- **CORS Enabled** - Use from any frontend application
- **Auto-scaling** - Asynchronous processing with uvicorn workers

## 📋 Requirements

- Python 3.10+
- CUDA-compatible GPU (optional, but recommended)
- Docker & Docker Compose (for containerized deployment)

## 🔧 Installation

### Option 1: Local Setup (Development)

1. **Navigate to backend directory:**
```bash
cd train/backend
```

2. **Activate virtual environment:**
```bash
# Windows
myenv\Scripts\activate

# Linux/Mac
source myenv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the API:**
```bash
python api.py
```

The API will start at `http://localhost:8000`

### Option 2: Docker Setup (Production)

1. **Build and run with Docker Compose:**
```bash
cd train
docker-compose up --build
```

This will:
- Build the API container
- Start the API on `http://localhost:8000`
- Start the frontend on `http://localhost:3000`

2. **Stop services:**
```bash
docker-compose down
```

## 📖 API Endpoints

### Health & Info

**GET `/`**
- Returns API information and available endpoints

**GET `/health`**
- Health check endpoint
- Returns: `{ status, model_loaded, model_path, classes, timestamp }`

**GET `/model-info`**
- Get detailed model information
- Returns: `{ model_name, classes, num_classes, confidence_threshold }`

### Image Detection

**POST `/detect/image`**
- Detect objects in a single image

**Parameters:**
- `file` (required): Image file (jpg, png, bmp, etc.)
- `confidence` (optional): Detection threshold (0.0-1.0), default: 0.5

**Response:**
```json
{
  "status": "success",
  "detections": [
    {
      "class_id": 5,
      "class_name": "EmergencyPhone",
      "confidence": 0.92,
      "bbox": {
        "x1": 100.5,
        "y1": 200.3,
        "x2": 250.8,
        "y2": 380.2
      }
    }
  ],
  "num_detections": 1,
  "image_saved": "results/detection_20250112_154230.jpg",
  "timestamp": "20250112_154230"
}
```

**Example cURL:**
```bash
curl -X POST "http://localhost:8000/detect/image" \
  -F "file=@image.jpg" \
  -F "confidence=0.5"
```

### Video Detection

**POST `/detect/video`**
- Process video file and save output with detections

**Parameters:**
- `file` (required): Video file (mp4, avi, mov, etc.)
- `confidence` (optional): Detection threshold (0.0-1.0), default: 0.5

**Response:**
```json
{
  "status": "success",
  "video_saved": "results/detected_20250112_154230.mp4",
  "frames_processed": 150,
  "detections": [
    {
      "frame": 0,
      "class": "FireExtinguisher",
      "confidence": 0.87
    }
  ],
  "timestamp": "20250112_154230"
}
```

### Live Webcam Detection

**WebSocket `/ws/webcam`**
- Real-time webcam detection via WebSocket

**Connection:**
```javascript
const ws = new WebSocket("ws://localhost:8000/ws/webcam");

ws.onmessage = (event) => {
  // Handle detections JSON
  const data = JSON.parse(event.data);
  // data = { type: "detections", count: N, objects: [...], timestamp: "..." }
  
  // Or image data (base64)
  // event.data = "data:image/jpeg;base64,..."
};
```

## 🎨 Web Dashboard

Access the dashboard at:
- **Local:** `http://localhost:3000`
- **With Docker:** `http://localhost:3000`

### Dashboard Features

1. **Image Detection Tab**
   - Drag & drop or click to upload images
   - View detected objects with confidence scores
   - Download annotated results

2. **Video Detection Tab**
   - Upload videos for batch processing
   - Monitor processing progress
   - Download processed video

3. **Live Webcam Tab**
   - Start/stop live webcam stream
   - Real-time detection display
   - Live object list with confidence scores

4. **Statistics Panel**
   - Total detections count
   - Average confidence score
   - Unique classes detected
   - Processing time

## 🐍 Python Client Example

```python
import requests
import json

API_URL = "http://localhost:8000"

# 1. Image Detection
def detect_image(image_path, confidence=0.5):
    with open(image_path, 'rb') as f:
        files = {'file': f}
        params = {'confidence': confidence}
        response = requests.post(f"{API_URL}/detect/image", files=files, params=params)
    return response.json()

result = detect_image("photo.jpg", confidence=0.6)
print(f"Found {result['num_detections']} objects")
for det in result['detections']:
    print(f"  - {det['class_name']}: {det['confidence']:.1%}")


# 2. Video Detection
def detect_video(video_path, confidence=0.5):
    with open(video_path, 'rb') as f:
        files = {'file': f}
        params = {'confidence': confidence}
        response = requests.post(f"{API_URL}/detect/video", files=files, params=params)
    return response.json()

result = detect_video("video.mp4")
print(f"Processed {result['frames_processed']} frames")
print(f"Saved to: {result['video_saved']}")


# 3. Live Webcam (using WebSocket)
import asyncio
import websockets
import json
import base64
from PIL import Image
import io

async def live_detection():
    async with websockets.connect("ws://localhost:8000/ws/webcam") as ws:
        async for message in ws:
            data = json.loads(message)
            print(f"Detected {data['count']} objects")
            for obj in data['objects']:
                print(f"  - {obj['class']}: {obj['confidence']:.1%}")

# Run: asyncio.run(live_detection())
```

## 🔍 Model Information

**Model:** final.pt (YOLO-based)

**Classes:**
1. OxygenTank (index 0)
2. NitrogenTank (index 1)
3. FirstAidBox (index 2)
4. FireAlarm (index 3)
5. SafetySwitchPanel (index 4)
6. **EmergencyPhone** (index 5) ⭐ *Swapped*
7. **FireExtinguisher** (index 6) ⭐ *Swapped*

**Default Confidence Threshold:** 0.5 (50%)

## 📦 Project Structure

```
train/
├── backend/
│   ├── api.py                 # FastAPI application
│   ├── app.py                # Original test script
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile            # Docker image definition
│   ├── myenv/               # Virtual environment
│   ├── weights/
│   │   ├── final.pt         # Trained model (swapped names)
│   │   ├── best.pt          # Original best model
│   │   └── ...
│   └── [utility scripts]
├── frontend/
│   └── index.html           # Web dashboard
├── results/                  # Detection outputs
└── docker-compose.yml       # Docker Compose configuration
```

## 🐳 Docker Commands

### Build
```bash
docker-compose build
```

### Run
```bash
docker-compose up
```

### Stop
```bash
docker-compose down
```

### View logs
```bash
docker-compose logs -f api
docker-compose logs -f frontend
```

### Run with GPU support
```yaml
# Add to docker-compose.yml under 'api' service:
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: 1
          capabilities: [gpu]
```

## ⚙️ Configuration

### API Configuration
Edit `backend/api.py`:
```python
CONFIDENCE_THRESHOLD = 0.5      # Default confidence threshold
MAX_DETECTIONS = 100            # Maximum detections per frame
RESULTS_DIR = Path(...)         # Output directory for results
```

### Server Configuration
Edit `backend/requirements.txt` to change uvicorn workers:
```bash
# Run with multiple workers
uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4
```

## 🚀 Deployment Examples

### 1. AWS EC2
```bash
# SSH into instance
ssh -i key.pem ubuntu@your-instance

# Clone repo and setup
git clone <repo>
cd train
docker-compose up -d

# Access at http://your-instance-ip:3000
```

### 2. Google Cloud Run
```bash
# Build image
gcloud builds submit --tag gcr.io/PROJECT/yolo-api

# Deploy
gcloud run deploy yolo-api \
  --image gcr.io/PROJECT/yolo-api \
  --port 8000 \
  --memory 4Gi
```

### 3. Heroku
```bash
# Create Procfile:
# web: uvicorn api:app --host 0.0.0.0 --port $PORT

heroku create your-app
git push heroku main
```

## 🔧 Troubleshooting

### API won't start
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000  # Windows
lsof -i :8000                  # Linux/Mac

# Kill process
taskkill /PID <PID> /F         # Windows
kill -9 <PID>                  # Linux/Mac
```

### Webcam not detected
- Ensure webcam is connected and accessible
- On Linux, may need: `sudo usermod -a -G video $USER`
- Docker may need `--privileged` flag for webcam access

### Out of memory errors
- Reduce image size before upload
- Process videos in smaller chunks
- Run on machine with more RAM

### GPU not detected
- Install CUDA & cuDNN
- Install torch with CUDA support:
  ```bash
  pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
  ```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Ultralytics YOLO](https://docs.ultralytics.com/)
- [Docker Documentation](https://docs.docker.com/)
- [WebSocket Guide](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)

## 📝 License

This project uses YOLO model from Ultralytics. Ensure you comply with their license terms.

## 💬 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review API logs: `docker-compose logs api`
3. Verify API health: `curl http://localhost:8000/health`

---

**Made with ❤️ for object detection**
