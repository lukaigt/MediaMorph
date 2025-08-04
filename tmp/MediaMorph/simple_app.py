#!/usr/bin/env python3

# Simple test app to check what's working
print("Testing imports...")

try:
    import sys
    print(f"✅ Python {sys.version}")
except Exception as e:
    print(f"❌ Python import failed: {e}")

try:
    import streamlit as st
    print("✅ Streamlit import successful")
    
    st.title("🎬 Test App")
    st.write("If you can see this, streamlit is working!")
    st.write("Upload a file to test:")
    
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file:
        st.success("File upload works!")
        
except ImportError as e:
    print(f"❌ Streamlit import failed: {e}")
    # Fallback - create a simple web server
    from http.server import HTTPServer, BaseHTTPRequestHandler
    import threading
    
    class SimpleHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = """
            <html><body>
            <h1>🎬 MediaMorph - Simple Mode</h1>
            <p>Streamlit isn't working, but the server is running!</p>
            <p>This proves the VPS deployment is working.</p>
            </body></html>
            """
            self.wfile.write(html.encode())
        
        def log_message(self, format, *args):
            pass
    
    def start_server():
        server = HTTPServer(('0.0.0.0', 8447), SimpleHandler)
        print("✅ Fallback server starting on port 8447")
        server.serve_forever()
    
    # Start in background
    thread = threading.Thread(target=start_server, daemon=True)
    thread.start()
    print("🌐 Open http://your-vps-ip:8447 to test")
    
    # Keep alive
    import time
    while True:
        time.sleep(1)