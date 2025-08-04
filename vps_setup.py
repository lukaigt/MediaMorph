#!/usr/bin/env python3
"""
VPS Setup Script for Smart Anti-Algorithm Repost Assistant
This script checks dependencies and creates proper startup scripts for your VPS
"""

import sys
import subprocess
import os
import shutil

def check_python():
    """Check Python version"""
    print(f"Python version: {sys.version}")
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8+ required")
        return False
    return True

def check_ffmpeg():
    """Check if FFmpeg is installed"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("FFmpeg: Available")
            return True
    except FileNotFoundError:
        pass
    
    print("ERROR: FFmpeg not found. Install with: sudo apt install ffmpeg")
    return False

def install_python_packages():
    """Install required Python packages"""
    packages = [
        'streamlit>=1.28.0',
        'ffmpeg-python>=0.2.0', 
        'pillow>=10.0.0',
        'numpy>=1.24.0',
        'opencv-python>=4.8.0',
        'scikit-image>=0.21.0',
        'scipy>=1.11.0'
    ]
    
    print("Installing Python packages...")
    for package in packages:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✅ {package} installed")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
            return False
    return True

def test_imports():
    """Test all required imports"""
    try:
        import streamlit
        import ffmpeg
        import PIL
        import numpy
        import cv2
        import scipy
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def create_startup_script():
    """Create VPS startup script"""
    script_content = '''#!/bin/bash
# Startup script for MediaMorph on VPS

echo "Starting Smart Anti-Algorithm Repost Assistant..."

# Kill any existing streamlit processes
pkill -f streamlit 2>/dev/null

# Wait a moment
sleep 2

# Start streamlit
echo "Starting on port 8447..."
streamlit run app.py --server.address 0.0.0.0 --server.port 8447 --server.headless true

echo "Application started! Access at http://your-vps-ip:8447"
'''
    
    with open('start_vps.sh', 'w') as f:
        f.write(script_content)
    
    # Make executable
    os.chmod('start_vps.sh', 0o755)
    print("✅ Created start_vps.sh script")

def create_systemd_service():
    """Create systemd service file for auto-startup"""
    current_dir = os.getcwd()
    user = os.getenv('USER', 'root')
    
    service_content = f'''[Unit]
Description=Smart Anti-Algorithm Repost Assistant
After=network.target

[Service]
Type=simple
User={user}
WorkingDirectory={current_dir}
ExecStart=/usr/bin/python3 -m streamlit run app.py --server.address 0.0.0.0 --server.port 8447 --server.headless true
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
'''
    
    service_file = 'mediamorph.service'
    with open(service_file, 'w') as f:
        f.write(service_content)
    
    print(f"✅ Created {service_file}")
    print(f"To install as service: sudo cp {service_file} /etc/systemd/system/")
    print("Then run: sudo systemctl enable mediamorph && sudo systemctl start mediamorph")

def main():
    print("🚀 VPS Setup for Smart Anti-Algorithm Repost Assistant")
    print("=" * 60)
    
    # Check system requirements
    if not check_python():
        return False
        
    if not check_ffmpeg():
        return False
    
    # Install packages
    if not install_python_packages():
        return False
    
    # Test imports
    if not test_imports():
        return False
    
    # Create startup scripts
    create_startup_script()
    create_systemd_service()
    
    print("\n✅ Setup complete!")
    print("\nTo start manually: ./start_vps.sh")
    print("To start as service: sudo systemctl start mediamorph")
    print("Access at: http://your-vps-ip:8447")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)