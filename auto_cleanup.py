import os
import glob
import time
import threading

def cleanup_temp_files():
    """Automatically cleanup video processing temp files"""
    patterns = [
        '/tmp/processed_*.mp4',
        '/tmp/processed_*.mov', 
        '/tmp/processed_*.avi',
        '/tmp/audio_protected_*.mp4',
        '/tmp/temp_*.mp4',
        '/tmp/temp_*.mov'
    ]
    
    for pattern in patterns:
        files = glob.glob(pattern)
        for file in files:
            try:
                # Only delete files older than 10 minutes
                if time.time() - os.path.getmtime(file) > 600:
                    os.remove(file)
                    print(f"🗑️ Cleaned up: {file}")
            except Exception as e:
                pass

def start_auto_cleanup():
    """Start background cleanup every 10 minutes"""
    def cleanup_loop():
        while True:
            time.sleep(600)  # 10 minutes
            cleanup_temp_files()
    
    cleanup_thread = threading.Thread(target=cleanup_loop, daemon=True)
    cleanup_thread.start()
    print("🤖 Auto-cleanup started - runs every 10 minutes")

# Auto-start when imported
start_auto_cleanup()