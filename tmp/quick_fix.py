#!/usr/bin/env python3
# Quick network test and fix

import socket
import subprocess
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

print("🔍 Network Diagnostics")
print("=" * 40)

# 1. Check what's using port 8447
try:
    result = subprocess.run(['ss', '-tlnp'], capture_output=True, text=True, timeout=10)
    if result.returncode == 0:
        lines = result.stdout.split('\n')
        port_lines = [line for line in lines if '8447' in line]
        if port_lines:
            print(f"Port 8447 is in use: {port_lines[0]}")
        else:
            print("Port 8447 is FREE")
    else:
        print("Could not check port status with ss")
except:
    try:
        result = subprocess.run(['netstat', '-tlnp'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            port_lines = [line for line in lines if '8447' in line]
            if port_lines:
                print(f"Port 8447 is in use: {port_lines[0]}")
            else:
                print("Port 8447 is FREE")
        else:
            print("Could not check port status")
    except:
        print("Network tools not available")

# 2. Test local connectivity
print("\n🌐 Testing connectivity...")
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    result = sock.connect_ex(('127.0.0.1', 8447))
    if result == 0:
        print("✅ Local connection (127.0.0.1:8447) works")
        sock.close()
    else:
        print("❌ Local connection failed")
        
        # Start a test server to prove network works
        class TestHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("""
                <html><body>
                <h1>NETWORK TEST SUCCESS!</h1>
                <p>Port 8447 is working from outside.</p>
                <p>The issue is with streamlit, not your VPS network.</p>
                <h2>Solution:</h2>
                <p>Kill streamlit and restart with: <code>streamlit run app.py --server.address 0.0.0.0 --server.port 8447</code></p>
                </body></html>
                """.encode('utf-8'))
            def log_message(self, format, *args):
                pass
        
        def start_test_server():
            try:
                server = HTTPServer(('0.0.0.0', 8447), TestHandler)
                print("🔧 Started test server on 0.0.0.0:8447")
                print("🌐 Check http://your-vps-ip:8447 in browser")
                server.serve_forever()
            except Exception as e:
                print(f"❌ Could not start test server: {e}")
        
        thread = threading.Thread(target=start_test_server, daemon=True)
        thread.start()
        
        # Keep alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nTest server stopped")
            
except Exception as e:
    print(f"Connection test failed: {e}")