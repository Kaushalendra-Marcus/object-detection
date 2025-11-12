# 🚀 Quick Start Guide

Get your YOLO Detection API running in minutes!

## Prerequisites

- Python 3.10+ (already installed with virtual environment)
- Webcam (optional, for live detection)

## ⚡ Fastest Way to Start

### Windows

Double-click this file:
```
backend/start.bat
```

Or run in PowerShell:
```powershell
cd train\backend
.\myenv\Scripts\Activate.ps1
python api.py
```

### Linux/Mac

```bash
cd train/backend
chmod +x start.sh
./start.sh
```

Or manually:
```bash
cd train/backend
source myenv/bin/activate
python api.py
```

## ✅ Verify API is Running

Once the server starts, you should see:
```
Uvicorn running on http://0.0.0.0:8000
```

Open your browser:
- **API Documentation:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

## 🎯 First Detection

### Option 1: Web Dashboard

1. Navigate to `frontend/index.html` in your browser
2. Upload an image
3. Click "Detect Objects"
4. View results in real-time!

### Option 2: Using cURL

```bash
# Image detection
curl -X POST "http://localhost:8000/detect/image" \
  -H "accept: application/json" \
  -F "file=@your_image.jpg"

# Video detection
curl -X POST "http://localhost:8000/detect/video" \
  -H "accept: application/json" \
  -F "file=@your_video.mp4"
```

### Option 3: Python Client

```python
from backend.client import YOLOClient

client = YOLOClient()
result = client.detect_image("image.jpg")
client.print_detections(result)
```

## 🎬 Live Webcam Detection

Open your browser to:
```
http://localhost:8000/detect/webcam-html
```

Click "Start Stream" to see live detection from your webcam!

## 📊 API Endpoints at a Glance

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | API info |
| `/health` | GET | Health check |
| `/docs` | GET | Interactive API docs |
| `/detect/image` | POST | Detect in image |
| `/detect/video` | POST | Process video |
| `/ws/webcam` | WS | Live webcam stream |
| `/detect/webcam-html` | GET | Webcam UI |

## 🐳 Docker (One Command!)

If you have Docker installed:

```bash
cd train
docker-compose up
```

Then open:
- **API:** http://localhost:8000
- **Dashboard:** http://localhost:3000

## 📝 Next Steps

1. **Test with Your Images**
   - Prepare test images
   - Use the dashboard or API to detect

2. **Integrate with Your App**
   - Use the REST API endpoints
   - Or use the Python client library

3. **Deploy to Production**
   - Use Docker for containerization
   - Deploy to AWS, GCP, or Heroku
   - See README.md for detailed steps

## 🔧 Troubleshooting

**API won't start:**
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000  # Windows
lsof -i :8000                  # Linux/Mac
```

**ModuleNotFoundError:**
```bash
# Make sure virtual environment is activated
# Windows:
.\myenv\Scripts\Activate.ps1

# Linux/Mac:
source myenv/bin/activate

# Then reinstall requirements:
pip install -r requirements.txt
```

**WebSocket connection fails:**
- Make sure you're using `ws://` not `http://` for WebSocket
- Check firewall settings

## 📚 Learn More

- Full Documentation: [README.md](README.md)
- API Reference: [http://localhost:8000/docs](http://localhost:8000/docs)
- Python Examples: [client.py](backend/client.py)

## 💡 Common Use Cases

### Detect in Single Image
```bash
curl -X POST http://localhost:8000/detect/image -F "file=@photo.jpg"
```

### Batch Process Videos
```bash
python backend/client.py video
```

### Stream Webcam
Visit: `http://localhost:8000/detect/webcam-html`

### Custom Integration
```python
import requests
response = requests.post(
    "http://localhost:8000/detect/image",
    files={"file": open("image.jpg", "rb")}
)
detections = response.json()
```

---

**Need help?** Check the troubleshooting section in README.md
