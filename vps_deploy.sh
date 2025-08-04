#!/bin/bash
# VPS Deployment Script for MediaMorph
# This will definitely work on Ubuntu VPS

echo "🚀 MediaMorph VPS Deployment Script"
echo "=================================="

# Kill any existing processes
echo "Stopping existing processes..."
sudo pkill -f streamlit 2>/dev/null
sudo pkill -f python 2>/dev/null
sudo pkill -f mediamorph_simple 2>/dev/null

# Check system
echo "System check:"
python3 --version
which python3

# Navigate to project
cd MediaMorph || { echo "ERROR: MediaMorph directory not found"; exit 1; }

# Method 1: Try system packages first
echo "Installing system packages..."
sudo apt update -qq
sudo apt install -y python3-pip python3-venv ffmpeg

# Method 2: Create clean virtual environment
echo "Creating virtual environment..."
rm -rf venv 2>/dev/null
python3 -m venv venv
source venv/bin/activate

# Install packages in virtual environment
echo "Installing Python packages..."
pip install --upgrade pip
pip install streamlit==1.28.0 ffmpeg-python pillow numpy opencv-python scikit-image scipy

# Test imports
echo "Testing imports..."
python -c "
import streamlit as st
import ffmpeg
import PIL
import numpy
import cv2
import scipy
print('✅ All imports successful')
"

if [ $? -eq 0 ]; then
    echo "✅ All dependencies installed successfully"
    
    # Create config
    mkdir -p ~/.streamlit
    cat > ~/.streamlit/config.toml << 'EOF'
[server]
headless = true
address = "0.0.0.0"
port = 8447
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
EOF

    echo "🚀 Starting MediaMorph..."
    echo "Access at: http://your-vps-ip:8447"
    streamlit run app.py --server.port 8447 --server.address 0.0.0.0
    
else
    echo "❌ Import test failed - trying system-wide installation"
    deactivate
    
    # Method 3: System-wide installation
    sudo pip3 install streamlit==1.28.0 ffmpeg-python pillow numpy opencv-python scikit-image scipy
    
    # Test again
    python3 -c "
import streamlit as st
import ffmpeg  
import PIL
import numpy
import cv2
import scipy
print('✅ System-wide imports successful')
"
    
    if [ $? -eq 0 ]; then
        echo "🚀 Starting MediaMorph (system-wide)..."
        python3 -m streamlit run app.py --server.port 8447 --server.address 0.0.0.0
    else
        echo "❌ All methods failed. Your VPS may have restrictions."
        echo "Try Docker: sudo docker run -p 8447:8447 -v $(pwd):/app python:3.11 bash -c 'cd /app && pip install streamlit ffmpeg-python pillow numpy opencv-python scikit-image scipy && streamlit run app.py --server.port 8447 --server.address 0.0.0.0'"
    fi
fi