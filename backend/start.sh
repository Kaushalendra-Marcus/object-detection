#!/bin/bash
# YOLO Detection API - Startup Script for Linux/Mac

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║    🎯 YOLO Object Detection API - Startup        ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Activate virtual environment
echo "[1/3] Activating virtual environment..."
source myenv/bin/activate

# Install/upgrade dependencies
echo "[2/3] Checking dependencies..."
pip install -q fastapi uvicorn python-multipart websockets aiofiles

# Start API
echo "[3/3] Starting API server..."
echo ""
echo "✓ API Server starting on http://localhost:8000"
echo "✓ Swagger UI available at http://localhost:8000/docs"
echo "✓ Web Dashboard at http://localhost:3000 (when running frontend)"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python api.py
