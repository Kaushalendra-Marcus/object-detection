# 🔌 Integration Examples

Real-world examples of integrating the YOLO Detection API with different frameworks and use cases.

## 📋 Table of Contents
1. [Python Integrations](#python-integrations)
2. [JavaScript/Web](#javascriptweb)
3. [Real-world Use Cases](#real-world-use-cases)
4. [Mobile Integration](#mobile-integration)

---

## Python Integrations

### Basic Image Detection

```python
from backend.client import YOLOClient

client = YOLOClient("http://localhost:8000")

# Detect objects
result = client.detect_image("factory_floor.jpg", confidence=0.6)

# Process results
if result['num_detections'] > 0:
    for detection in result['detections']:
        print(f"Found {detection['class_name']} at {detection['bbox']}")
```

### Batch Processing Images

```python
from backend.client import YOLOClient
from pathlib import Path
import json

client = YOLOClient()

image_dir = Path("images")
results = {}

for image_file in image_dir.glob("*.jpg"):
    print(f"Processing {image_file.name}...")
    result = client.detect_image(str(image_file))
    results[image_file.name] = result['detections']

# Save results
with open("results.json", "w") as f:
    json.dump(results, f, indent=2)
```

### Video Processing Pipeline

```python
from backend.client import YOLOClient
import json
from datetime import datetime

client = YOLOClient()

def process_security_footage(video_path):
    print(f"Processing {video_path}...")
    result = client.detect_video(video_path, confidence=0.7)
    
    # Analyze detections
    detections_by_class = {}
    for det in result['detections']:
        class_name = det['class']
        if class_name not in detections_by_class:
            detections_by_class[class_name] = 0
        detections_by_class[class_name] += 1
    
    # Report
    print("\n📊 Detection Summary:")
    print(f"Frames processed: {result['frames_processed']}")
    print(f"Total detections: {len(result['detections'])}")
    print("\nBy class:")
    for cls, count in detections_by_class.items():
        print(f"  - {cls}: {count}")

# Usage
process_security_footage("security_footage.mp4")
```

### Real-time Alert System

```python
import asyncio
from backend.client import YOLOAsyncClient
import smtplib

client = YOLOAsyncClient()
alert_threshold = {'FireExtinguisher': 5, 'FireAlarm': 3}
frame_count = 0

async def monitor_for_alerts():
    def on_detection(data):
        global frame_count
        frame_count += 1
        
        for obj in data['objects']:
            if obj['class'] in alert_threshold:
                if obj['confidence'] > 0.8:
                    send_alert(f"HIGH CONFIDENCE {obj['class']} detected!")
    
    await client.live_detection(on_detection=on_detection)

def send_alert(message):
    # Send email, SMS, or webhook
    print(f"🚨 ALERT: {message}")
    # Example: send email
    # smtp = smtplib.SMTP('smtp.gmail.com', 587)
    # smtp.sendmail('from@gmail.com', 'to@gmail.com', message)

asyncio.run(monitor_for_alerts())
```

### Integration with Database

```python
from backend.client import YOLOClient
import sqlite3
from datetime import datetime

client = YOLOClient()

# Setup database
conn = sqlite3.connect('detections.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS detections (
        id INTEGER PRIMARY KEY,
        timestamp TEXT,
        image_path TEXT,
        class_name TEXT,
        confidence REAL,
        bbox_x1 REAL, bbox_y1 REAL, bbox_x2 REAL, bbox_y2 REAL
    )
''')
conn.commit()

def save_detections(image_path, result):
    timestamp = datetime.now().isoformat()
    
    for det in result['detections']:
        bbox = det['bbox']
        cursor.execute('''
            INSERT INTO detections 
            (timestamp, image_path, class_name, confidence, bbox_x1, bbox_y1, bbox_x2, bbox_y2)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            timestamp,
            image_path,
            det['class_name'],
            det['confidence'],
            bbox['x1'], bbox['y1'], bbox['x2'], bbox['y2']
        ))
    conn.commit()

# Usage
result = client.detect_image("photo.jpg")
save_detections("photo.jpg", result)
```

---

## JavaScript/Web

### Vanilla JavaScript

```javascript
const API_URL = "http://localhost:8000";

async function detectImage(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch(`${API_URL}/detect/image`, {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        console.log(`Found ${result.num_detections} objects:`);
        
        result.detections.forEach(det => {
            console.log(`- ${det.class_name}: ${(det.confidence * 100).toFixed(1)}%`);
        });
        
        return result;
    } catch (error) {
        console.error('Detection failed:', error);
    }
}

// Usage
document.getElementById('file-input').addEventListener('change', (e) => {
    detectImage(e.target.files[0]);
});
```

### React Component

```jsx
import React, { useState } from 'react';
import axios from 'axios';

function ImageDetector() {
    const [detections, setDetections] = useState([]);
    const [loading, setLoading] = useState(false);
    const API_URL = "http://localhost:8000";

    const handleImageUpload = async (file) => {
        setLoading(true);
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post(
                `${API_URL}/detect/image`,
                formData,
                { headers: { 'Content-Type': 'multipart/form-data' } }
            );
            setDetections(response.data.detections);
        } catch (error) {
            console.error('Detection failed:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <input
                type="file"
                onChange={(e) => handleImageUpload(e.target.files[0])}
            />
            
            {loading && <p>Processing...</p>}
            
            <div>
                {detections.map((det, idx) => (
                    <div key={idx}>
                        <strong>{det.class_name}</strong>: {(det.confidence * 100).toFixed(1)}%
                    </div>
                ))}
            </div>
        </div>
    );
}

export default ImageDetector;
```

### WebSocket Real-time Display

```javascript
class LiveDetectionDisplay {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.detectionsList = [];
    }

    start() {
        const ws = new WebSocket('ws://localhost:8000/ws/webcam');
        
        ws.onopen = () => console.log('Connected to live stream');
        
        ws.onmessage = (event) => {
            if (event.data.startsWith('data:image')) {
                // Update video stream
                document.getElementById('stream').src = event.data;
            } else {
                // Update detections
                const data = JSON.parse(event.data);
                this.updateDetections(data);
            }
        };
        
        ws.onerror = () => console.error('WebSocket error');
        ws.onclose = () => console.log('Disconnected');
    }

    updateDetections(data) {
        const html = data.objects.map(obj => `
            <div class="detection">
                <span>${obj.class}</span>
                <span>${(obj.confidence * 100).toFixed(1)}%</span>
            </div>
        `).join('');
        
        this.container.innerHTML = html || '<p>No detections</p>';
    }
}

// Usage
const display = new LiveDetectionDisplay('detections-container');
display.start();
```

### Node.js Integration

```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

const API_URL = "http://localhost:8000";

async function detectImage(imagePath) {
    const form = new FormData();
    form.append('file', fs.createReadStream(imagePath));

    try {
        const response = await axios.post(
            `${API_URL}/detect/image`,
            form,
            { headers: form.getHeaders() }
        );
        
        console.log(`Detections in ${imagePath}:`);
        response.data.detections.forEach(det => {
            console.log(`  - ${det.class_name}: ${(det.confidence * 100).toFixed(1)}%`);
        });
        
        return response.data;
    } catch (error) {
        console.error('Error:', error.message);
    }
}

// Usage
detectImage('photo.jpg');
```

---

## Real-world Use Cases

### 1. Manufacturing Quality Control

```python
from backend.client import YOLOClient
import csv
from datetime import datetime

client = YOLOClient()

def quality_check_production_line(image_path):
    """Detect safety violations on production line"""
    result = client.detect_image(image_path, confidence=0.7)
    
    violations = []
    for det in result['detections']:
        if det['class_name'] in ['FireExtinguisher', 'SafetySwitchPanel']:
            if det['confidence'] < 0.8:  # Low confidence = obscured/missing
                violations.append({
                    'object': det['class_name'],
                    'confidence': det['confidence'],
                    'issue': 'Equipment not clearly visible'
                })
    
    if violations:
        log_violation(image_path, violations)
        return False
    return True

def log_violation(image_path, violations):
    with open('quality_log.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        for v in violations:
            writer.writerow([datetime.now(), image_path, v['object'], v['issue']])

# Continuous monitoring
for frame in production_line_feed():
    if not quality_check_production_line(frame):
        raise_quality_alert(frame)
```

### 2. Building Safety Monitoring

```python
from backend.client import YOLOAsyncClient
import asyncio
from datetime import datetime, timedelta

client = YOLOAsyncClient()
safety_report = {
    'timestamp': datetime.now(),
    'missing_equipment': [],
    'findings': {}
}

async def safety_audit():
    """Run safety audit on building"""
    
    def on_detection(data):
        for obj in data['objects']:
            class_name = obj['class']
            confidence = obj['confidence']
            
            if class_name not in safety_report['findings']:
                safety_report['findings'][class_name] = []
            
            safety_report['findings'][class_name].append({
                'detected': confidence > 0.6,
                'confidence': confidence
            })
    
    await client.live_detection(on_detection=on_detection)
    
    # Generate report
    generate_safety_report(safety_report)

def generate_safety_report(report):
    """Generate PDF report"""
    print("🏢 BUILDING SAFETY REPORT")
    print(f"Generated: {report['timestamp']}")
    print("\nFindings:")
    for equipment, detections in report['findings'].items():
        detected_count = sum(1 for d in detections if d['detected'])
        print(f"  {equipment}: {detected_count}/{len(detections)} detections")

asyncio.run(safety_audit())
```

### 3. Security Surveillance

```python
from backend.client import YOLOClient
import cv2
from datetime import datetime
import os

client = YOLOClient()

def analyze_security_footage(video_path, output_dir='security_alerts'):
    """Analyze security footage for suspicious items"""
    
    result = client.detect_video(video_path, confidence=0.7)
    
    # Create alert report
    os.makedirs(output_dir, exist_ok=True)
    
    anomalies = []
    for det in result['detections']:
        # Alert on unexpected locations of emergency equipment
        if det['class'] in ['FireExtinguisher', 'EmergencyPhone']:
            anomalies.append({
                'frame': det['frame'],
                'item': det['class'],
                'confidence': det['confidence'],
                'timestamp': calculate_timestamp(det['frame'], 30)  # 30 FPS
            })
    
    if anomalies:
        with open(os.path.join(output_dir, 'alerts.txt'), 'w') as f:
            for anomaly in anomalies:
                f.write(f"ALERT at {anomaly['timestamp']}: "
                       f"Unusual presence of {anomaly['item']}\n")
    
    return anomalies

def calculate_timestamp(frame_num, fps):
    seconds = frame_num / fps
    return f"{int(seconds//60):02d}:{int(seconds%60):02d}"

# Usage
anomalies = analyze_security_footage('surveillance.mp4')
if anomalies:
    print(f"⚠️ Found {len(anomalies)} potential security concerns")
```

---

## Mobile Integration

### Flutter Integration

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class YOLODetector {
  static const String API_URL = 'http://your-server:8000';

  static Future<List<Detection>> detectImage(String imagePath) async {
    var request = http.MultipartRequest(
      'POST',
      Uri.parse('$API_URL/detect/image'),
    );
    
    request.files.add(
      await http.MultipartFile.fromPath('file', imagePath)
    );
    
    var response = await request.send();
    final result = await response.stream.bytesToString();
    final json = jsonDecode(result);
    
    return (json['detections'] as List)
        .map((d) => Detection.fromJson(d))
        .toList();
  }
}

class Detection {
  final String className;
  final double confidence;
  
  Detection({required this.className, required this.confidence});
  
  factory Detection.fromJson(Map<String, dynamic> json) {
    return Detection(
      className: json['class_name'],
      confidence: json['confidence'],
    );
  }
}
```

### Swift (iOS) Integration

```swift
import Foundation

class YOLOClient {
    let apiURL = "http://your-server:8000"
    
    func detectImage(_ imageData: Data, completion: @escaping ([Detection]?) -> Void) {
        var request = URLRequest(url: URL(string: "\(apiURL)/detect/image")!)
        request.httpMethod = "POST"
        
        let boundary = UUID().uuidString
        request.setValue("multipart/form-data; boundary=\(boundary)", 
                        forHTTPHeaderField: "Content-Type")
        
        var body = Data()
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"file\"; filename=\"image.jpg\"\r\n".data(using: .utf8)!)
        body.append("Content-Type: image/jpeg\r\n\r\n".data(using: .utf8)!)
        body.append(imageData)
        body.append("\r\n--\(boundary)--\r\n".data(using: .utf8)!)
        
        request.httpBody = body
        
        URLSession.shared.dataTask(with: request) { data, _, error in
            guard let data = data, error == nil else {
                completion(nil)
                return
            }
            
            if let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
               let detections = json["detections"] as? [[String: Any]] {
                let results = detections.map { det in
                    Detection(
                        className: det["class_name"] as? String ?? "",
                        confidence: det["confidence"] as? Double ?? 0
                    )
                }
                completion(results)
            }
        }.resume()
    }
}

struct Detection {
    let className: String
    let confidence: Double
}
```

---

## Tips & Best Practices

1. **Error Handling**
   - Always wrap API calls in try-catch
   - Implement retry logic for failed requests
   - Log errors for debugging

2. **Performance**
   - Batch process when possible
   - Use appropriate confidence thresholds
   - Cache model info to reduce API calls

3. **Security**
   - Use HTTPS in production
   - Implement authentication for sensitive data
   - Validate file types before uploading

4. **Optimization**
   - Resize large images before detection
   - Use WebSocket for real-time applications
   - Implement frame skipping for video streams

---

For more examples, check the `backend/client.py` file!
