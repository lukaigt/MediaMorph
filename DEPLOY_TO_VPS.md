# VPS Deployment Guide

## Quick Deploy (Recommended)

1. **Upload to GitHub** (you're already doing this)
2. **On your VPS, clone the repo:**
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

3. **Run the deployment script:**
   ```bash
   chmod +x vps_deploy.sh
   ./vps_deploy.sh
   ```

4. **Access your app:**
   ```
   http://your-vps-ip:8447
   ```

## Alternative Setup

If the script doesn't work, try manual setup:

```bash
# Install system dependencies
sudo apt update
sudo apt install -y python3-pip ffmpeg

# Install Python packages
pip3 install --user streamlit==1.28.0 ffmpeg-python pillow numpy opencv-python scikit-image scipy

# Add to PATH
export PATH="$HOME/.local/bin:$PATH"

# Start the app
streamlit run app.py --server.address 0.0.0.0 --server.port 8447
```

## Troubleshooting

### "streamlit: command not found"
```bash
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Port already in use
```bash
# Kill existing processes
pkill -f streamlit
# Wait 5 seconds, then restart
```

### Can't access from browser
- Check your VPS firewall allows port 8447
- Use your VPS's public IP address, not localhost
- Make sure you're using http:// not https://

### Import errors
Try system-wide installation:
```bash
sudo pip3 install streamlit ffmpeg-python pillow numpy opencv-python scikit-image scipy
```

## Running as Background Service

1. **Create the service file:**
   ```bash
   python3 vps_setup.py
   sudo cp mediamorph.service /etc/systemd/system/
   ```

2. **Enable and start:**
   ```bash
   sudo systemctl enable mediamorph
   sudo systemctl start mediamorph
   ```

3. **Check status:**
   ```bash
   sudo systemctl status mediamorph
   ```

## Requirements for VPS

- Ubuntu 18.04+ or similar Linux distro
- Python 3.8+
- At least 1GB RAM
- Port 8447 open in firewall
- FFmpeg system package

The app works entirely offline - no API keys needed!