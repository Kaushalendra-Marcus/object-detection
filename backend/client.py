#client.py
"""
YOLO Detection Client Library
Easy-to-use Python client for the YOLO Detection API
"""

import requests
import asyncio
import json
import base64
from pathlib import Path
from typing import Optional, List, Dict, Tuple
import websockets


class YOLOClient:
    """Synchronous client for YOLO Detection API"""
    
    def __init__(self, api_url: str = "http://localhost:8000"):
        """
        Initialize YOLO client
        
        Args:
            api_url: Base URL of the API (default: http://localhost:8000)
        """
        self.api_url = api_url.rstrip('/')
        self.session = requests.Session()
    
    def health_check(self) -> Dict:
        """Check API health status"""
        response = self.session.get(f"{self.api_url}/health")
        response.raise_for_status()
        return response.json()
    
    def get_model_info(self) -> Dict:
        """Get model information including classes"""
        response = self.session.get(f"{self.api_url}/model-info")
        response.raise_for_status()
        return response.json()
    
    def detect_image(
        self,
        image_path: str,
        confidence: float = 0.5
    ) -> Dict:
        """
        Detect objects in an image
        
        Args:
            image_path: Path to image file
            confidence: Detection confidence threshold (0.0-1.0)
        
        Returns:
            Detection results with bounding boxes and confidences
        """
        with open(image_path, 'rb') as f:
            files = {'file': f}
            params = {'confidence': confidence}
            response = self.session.post(
                f"{self.api_url}/detect/image",
                files=files,
                params=params
            )
        response.raise_for_status()
        return response.json()
    
    def detect_video(
        self,
        video_path: str,
        confidence: float = 0.5
    ) -> Dict:
        """
        Process video and detect objects in all frames
        
        Args:
            video_path: Path to video file
            confidence: Detection confidence threshold (0.0-1.0)
        
        Returns:
            Processing results with frame detections
        """
        with open(video_path, 'rb') as f:
            files = {'file': f}
            params = {'confidence': confidence}
            response = self.session.post(
                f"{self.api_url}/detect/video",
                files=files,
                params=params
            )
        response.raise_for_status()
        return response.json()
    
    def print_detections(self, result: Dict) -> None:
        """Pretty print detection results"""
        print(f"\n{'='*60}")
        print(f"DETECTION RESULTS")
        print(f"{'='*60}")
        print(f"Total Detections: {result.get('num_detections', 0)}")
        
        if 'detections' in result:
            for i, det in enumerate(result['detections'], 1):
                print(f"\n{i}. {det['class_name']}")
                print(f"   Confidence: {det['confidence']:.1%}")
                bbox = det['bbox']
                print(f"   Location: ({bbox['x1']:.1f}, {bbox['y1']:.1f}) "
                      f"to ({bbox['x2']:.1f}, {bbox['y2']:.1f})")
        
        if 'image_saved' in result:
            print(f"\nResult saved to: {result['image_saved']}")
        
        print(f"{'='*60}\n")


class YOLOAsyncClient:
    """Asynchronous client for YOLO Detection API with WebSocket support"""
    
    def __init__(self, api_url: str = "http://localhost:8000"):
        """
        Initialize async YOLO client
        
        Args:
            api_url: Base URL of the API (default: http://localhost:8000)
        """
        self.api_url = api_url.rstrip('/')
        self.ws = None
    
    async def live_detection(
        self,
        on_detection: callable,
        on_frame: Optional[callable] = None
    ):
        """
        Start live webcam detection via WebSocket
        
        Args:
            on_detection: Callback function(detections_dict) for each frame
            on_frame: Optional callback function(image_base64) for video frames
        """
        # Convert http to ws, https to wss
        ws_url = self.api_url.replace('http://', 'ws://').replace('https://', 'wss://')
        
        try:
            async with websockets.connect(f"{ws_url}/ws/webcam") as ws:
                self.ws = ws
                print("Connected to live stream")
                
                async for message in ws:
                    if message.startswith('data:image'):
                        # Frame data
                        if on_frame:
                            on_frame(message)
                    else:
                        # Detection data
                        data = json.loads(message)
                        if on_detection:
                            on_detection(data)
        
        except KeyboardInterrupt:
            print("\nDisconnected from live stream")
        except Exception as e:
            print(f"Error in live detection: {e}")
        finally:
            self.ws = None
    
    async def stop_detection(self):
        """Stop live detection stream"""
        if self.ws:
            await self.ws.close()


# Example usage functions
def example_image_detection():
    """Example: Detect objects in a static image"""
    print("🖼️ Image Detection Example\n")
    
    client = YOLOClient()
    
    try:
        # Check API is available
        info = client.health_check()
        print(f"✓ API Status: {info['status']}")
        print(f"✓ Model: {info['model_path']}\n")
        
        # Detect in image
        image_path = "test_image.jpg"
        print(f"Detecting objects in: {image_path}")
        result = client.detect_image(image_path, confidence=0.5)
        
        # Show results
        client.print_detections(result)
        
    except FileNotFoundError:
        print("⚠️ Image file not found. Please provide a test_image.jpg")
    except Exception as e:
        print(f"❌ Error: {e}")


def example_video_detection():
    """Example: Detect objects in a video"""
    print("🎬 Video Detection Example\n")
    
    client = YOLOClient()
    
    try:
        video_path = "test_video.mp4"
        print(f"Processing video: {video_path}")
        print("This may take a while...\n")
        
        result = client.detect_video(video_path, confidence=0.5)
        
        print(f"✓ Video processed successfully!")
        print(f"  Frames: {result['frames_processed']}")
        print(f"  Total detections: {len(result['detections'])}")
        print(f"  Output: {result['video_saved']}")
        
    except FileNotFoundError:
        print("⚠️ Video file not found. Please provide a test_video.mp4")
    except Exception as e:
        print(f"❌ Error: {e}")


async def example_live_detection():
    """Example: Live webcam detection"""
    print("🎥 Live Webcam Detection Example\n")
    
    client = YOLOAsyncClient()
    
    detection_count = 0
    
    def on_detection(data):
        nonlocal detection_count
        detection_count += 1
        count = data.get('count', 0)
        if count > 0:
            print(f"\n[Frame {detection_count}] Detected {count} objects:")
            for obj in data['objects']:
                print(f"  - {obj['class']}: {obj['confidence']:.1%}")
    
    try:
        print("Starting live detection (Press Ctrl+C to stop)...\n")
        await client.live_detection(on_detection=on_detection)
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    import sys
    
    print("YOLO Detection Client Examples\n")
    
    if len(sys.argv) > 1:
        example = sys.argv[1].lower()
        
        if example == "image":
            example_image_detection()
        elif example == "video":
            example_video_detection()
        elif example == "live":
            asyncio.run(example_live_detection())
        else:
            print("Usage: python client.py [image|video|live]")
    else:
        print("Usage: python client.py [image|video|live]\n")
        print("Examples:")
        print("  python client.py image  # Static image detection")
        print("  python client.py video  # Video file detection")
        print("  python client.py live   # Live webcam detection")
