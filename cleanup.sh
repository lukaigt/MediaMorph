#!/bin/bash

# Smart cleanup script - only removes video processing temp files
# Keeps n8n and other system files safe

echo "🧹 Starting smart cleanup..."

# Clean only video processing temp files
rm -f /tmp/processed_*.mp4
rm -f /tmp/processed_*.mov
rm -f /tmp/processed_*.avi
rm -f /tmp/audio_protected_*.mp4
rm -f /tmp/temp_*.mp4
rm -f /tmp/temp_*.mov

# Clean Streamlit cache (safe to delete)
rm -rf ~/.streamlit/cache/

# Show storage before/after
df -h | grep -E "Filesystem|/dev/"

echo "✅ Cleanup complete - only video processing files removed"
echo "📊 Storage freed up:"