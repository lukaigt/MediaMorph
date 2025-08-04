#!/bin/bash
# Simple VPS Deployment Script 
# Works on Ubuntu 20.04+ VPS

echo "Smart Anti-Algorithm Repost Assistant - VPS Deploy"
echo "=================================================="

# Kill existing processes
echo "Stopping existing processes..."
pkill -f streamlit 2>/dev/null
pkill -f "python.*app.py" 2>/dev/null

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "ERROR: app.py not found. Make sure you're in the project directory."
    exit 1
fi

# System packages
echo "Installing system packages..."
sudo apt update
sudo apt install -y python3-pip ffmpeg

# Install Python packages directly (no virtual env for simplicity)
echo "Installing Python packages..."
pip3 install --user --upgrade pip
pip3 install --user streamlit==1.28.0 ffmpeg-python pillow numpy opencv-python scikit-image scipy

# Add user bin to PATH if not already there
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

# Test installation
echo "Testing installation..."
python3 -c "
try:
    import streamlit, ffmpeg, PIL, numpy, cv2, scipy
    print('All packages imported successfully')
except ImportError as e:
    print(f'Import error: {e}')
    exit(1)
"

if [ $? -ne 0 ]; then
    echo "Package installation failed. Trying system-wide..."
    sudo pip3 install streamlit==1.28.0 ffmpeg-python pillow numpy opencv-python scikit-image scipy
fi

# Create streamlit config
mkdir -p ~/.streamlit
cat > ~/.streamlit/config.toml << 'EOF'
[server]
headless = true
address = "0.0.0.0"
port = 8447
enableCORS = false
enableXsrfProtection = false
maxUploadSize = 1000

[browser]
gatherUsageStats = false
EOF

echo "Starting application..."
echo "Access at: http://your-vps-ip:8447"
echo "Press Ctrl+C to stop"

# Start streamlit
streamlit run app.py --server.address 0.0.0.0 --server.port 8447