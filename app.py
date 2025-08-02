import streamlit as st
import os
import tempfile
import shutil
from pathlib import Path
import base64
import time

from processors.video_processor import VideoProcessor
from processors.image_processor import ImageProcessor
from processors.command_parser import CommandParser
from utils.file_utils import FileUtils

# Initialize processors
@st.cache_resource
def get_processors():
    return {
        'video': VideoProcessor(),
        'image': ImageProcessor(), 
        'command': CommandParser(),
        'file_utils': FileUtils()
    }

def main():
    st.set_page_config(
        page_title="Smart Anti-Algorithm Repost Assistant",
        page_icon="🎬",
        layout="wide"
    )
    
    st.title("🎬 Smart Anti-Algorithm Repost Assistant")
    st.markdown("Upload your video or photo and transform it for safe social media reposting!")
    
    processors = get_processors()
    
    # Initialize session state
    if 'processed_file' not in st.session_state:
        st.session_state.processed_file = None
    if 'original_file' not in st.session_state:
        st.session_state.original_file = None
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    
    # File upload section
    st.header("📁 Upload Media")
    uploaded_file = st.file_uploader(
        "Choose a video or image file",
        type=['mp4', 'mov', 'avi', 'jpg', 'jpeg', 'png', 'gif'],
        help="Supported formats: MP4, MOV, AVI for videos | JPG, PNG, GIF for images"
    )
    
    if uploaded_file is not None:
        st.session_state.original_file = uploaded_file
        
        # Display file info
        file_details = processors['file_utils'].get_file_info(uploaded_file)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("File Name", file_details['name'])
        with col2:
            st.metric("File Size", file_details['size'])
        with col3:
            st.metric("File Type", file_details['type'])
        
        # Platform preset buttons
        st.header("🎯 Platform Presets")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📱 TikTok Mode", use_container_width=True, disabled=st.session_state.processing):
                if file_details['category'] == 'video':
                    process_video_preset(uploaded_file, 'tiktok', processors)
                else:
                    process_image_preset(uploaded_file, 'tiktok', processors)
        
        with col2:
            if st.button("📸 Instagram Mode", use_container_width=True, disabled=st.session_state.processing):
                if file_details['category'] == 'video':
                    process_video_preset(uploaded_file, 'instagram', processors)
                else:
                    process_image_preset(uploaded_file, 'instagram', processors)
        
        with col3:
            if st.button("🎥 YouTube Mode", use_container_width=True, disabled=st.session_state.processing):
                if file_details['category'] == 'video':
                    process_video_preset(uploaded_file, 'youtube', processors)
                else:
                    process_image_preset(uploaded_file, 'youtube', processors)
        
        # Custom commands section
        st.header("💬 Custom Edit Commands")
        with st.expander("ℹ️ Command Examples", expanded=False):
            st.markdown("""
            **Video Commands:**
            - `flip horizontal` - Flip video horizontally
            - `speed 1.5` - Change playback speed
            - `zoom 1.2` - Zoom in by factor
            - `rotate 90` - Rotate by degrees
            - `slow 20%` - Slow down by percentage
            
            **Image Commands:**
            - `flip vertical` - Flip image vertically
            - `brightness 120` - Increase brightness
            - `contrast 110` - Increase contrast
            - `crop square` - Crop to square aspect ratio
            - `vintage filter` - Apply vintage effect
            """)
        
        custom_command = st.text_input(
            "Enter custom edit command:",
            placeholder="e.g., 'flip horizontal + speed 1.2 + vintage filter'",
            disabled=st.session_state.processing
        )
        
        if st.button("🚀 Apply Custom Edit", disabled=st.session_state.processing or not custom_command):
            if file_details['category'] == 'video':
                process_video_custom(uploaded_file, custom_command, processors)
            else:
                process_image_custom(uploaded_file, custom_command, processors)
        
        # Processing indicator
        if st.session_state.processing:
            with st.spinner("Processing your media... Please wait."):
                time.sleep(0.1)  # Small delay to show spinner
        
        # Download section
        if st.session_state.processed_file:
            st.header("⬇️ Download Processed Media")
            
            # Create download button
            with open(st.session_state.processed_file, "rb") as file:
                file_data = file.read()
                file_name = Path(st.session_state.processed_file).name
                
                st.download_button(
                    label="📥 Download Processed File",
                    data=file_data,
                    file_name=f"repost_{file_name}",
                    mime=processors['file_utils'].get_mime_type(file_name),
                    use_container_width=True
                )
            
            # Display preview for images
            if file_details['category'] == 'image':
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Original")
                    st.image(uploaded_file, use_column_width=True)
                with col2:
                    st.subheader("Processed")
                    st.image(st.session_state.processed_file, use_column_width=True)

def process_video_preset(uploaded_file, platform, processors):
    """Process video with platform preset"""
    st.session_state.processing = True
    st.rerun()
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_input:
            temp_input.write(uploaded_file.read())
            temp_input_path = temp_input.name
        
        output_path = processors['video'].apply_preset(temp_input_path, platform)
        st.session_state.processed_file = output_path
        st.success(f"✅ Video processed for {platform.title()}!")
        
    except Exception as e:
        st.error(f"❌ Error processing video: {str(e)}")
    finally:
        st.session_state.processing = False
        if 'temp_input_path' in locals():
            try:
                os.unlink(temp_input_path)
            except:
                pass
        st.rerun()

def process_image_preset(uploaded_file, platform, processors):
    """Process image with platform preset"""
    st.session_state.processing = True
    st.rerun()
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_input:
            temp_input.write(uploaded_file.read())
            temp_input_path = temp_input.name
        
        output_path = processors['image'].apply_preset(temp_input_path, platform)
        st.session_state.processed_file = output_path
        st.success(f"✅ Image processed for {platform.title()}!")
        
    except Exception as e:
        st.error(f"❌ Error processing image: {str(e)}")
    finally:
        st.session_state.processing = False
        if 'temp_input_path' in locals():
            try:
                os.unlink(temp_input_path)
            except:
                pass
        st.rerun()

def process_video_custom(uploaded_file, command, processors):
    """Process video with custom command"""
    st.session_state.processing = True
    st.rerun()
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_input:
            temp_input.write(uploaded_file.read())
            temp_input_path = temp_input.name
        
        parsed_commands = processors['command'].parse_command(command, 'video')
        output_path = processors['video'].apply_custom_commands(temp_input_path, parsed_commands)
        st.session_state.processed_file = output_path
        st.success("✅ Custom video processing completed!")
        
    except Exception as e:
        st.error(f"❌ Error processing video: {str(e)}")
    finally:
        st.session_state.processing = False
        if 'temp_input_path' in locals():
            try:
                os.unlink(temp_input_path)
            except:
                pass
        st.rerun()

def process_image_custom(uploaded_file, command, processors):
    """Process image with custom command"""
    st.session_state.processing = True
    st.rerun()
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_input:
            temp_input.write(uploaded_file.read())
            temp_input_path = temp_input.name
        
        parsed_commands = processors['command'].parse_command(command, 'image')
        output_path = processors['image'].apply_custom_commands(temp_input_path, parsed_commands)
        st.session_state.processed_file = output_path
        st.success("✅ Custom image processing completed!")
        
    except Exception as e:
        st.error(f"❌ Error processing image: {str(e)}")
    finally:
        st.session_state.processing = False
        if 'temp_input_path' in locals():
            try:
                os.unlink(temp_input_path)
            except:
                pass
        st.rerun()

if __name__ == "__main__":
    main()
