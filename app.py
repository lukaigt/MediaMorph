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
    if 'current_platform' not in st.session_state:
        st.session_state.current_platform = None
    if 'file_details' not in st.session_state:
        st.session_state.file_details = None
    
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
        st.session_state.file_details = file_details
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("File Name", file_details['name'])
        with col2:
            st.metric("File Size", file_details['size'])
        with col3:
            st.metric("File Type", file_details['type'])
        
        # Show original file preview
        if file_details['category'] == 'image':
            st.subheader("📸 Original Image")
            st.image(uploaded_file, caption="Original", use_container_width=True)
        else:
            st.subheader("🎥 Original Video")
            st.video(uploaded_file)
        
        # Platform preset buttons
        st.header("🎯 Advanced Algorithm Evasion Presets")
        st.markdown("**Choose your target platform for heavy modifications that algorithms can't detect:**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📱 TikTok Anti-Algorithm", use_container_width=True, type="primary"):
                st.session_state.current_platform = 'tiktok'
                with st.spinner("Processing for TikTok..."):
                    process_media_preset(uploaded_file, 'tiktok', file_details, processors)
        
        with col2:
            if st.button("📸 Instagram Anti-Algorithm", use_container_width=True, type="primary"):
                st.session_state.current_platform = 'instagram'
                with st.spinner("Processing for Instagram..."):
                    process_media_preset(uploaded_file, 'instagram', file_details, processors)
        
        with col3:
            if st.button("🎥 YouTube Anti-Algorithm", use_container_width=True, type="primary"):
                st.session_state.current_platform = 'youtube'
                with st.spinner("Processing for YouTube..."):
                    process_media_preset(uploaded_file, 'youtube', file_details, processors)
        
        # Show what each preset does
        with st.expander("🔧 What Each Preset Does", expanded=False):
            st.markdown("""
            **TikTok Anti-Algorithm:**
            - Horizontal flip + 15% speed boost + zoom + strong noise
            - Color channel manipulation + pixel position changes
            - Heavy brightness/contrast/saturation adjustments
            
            **Instagram Anti-Algorithm:**
            - Square crop + vibrant color boost + film grain
            - Hue shifts + sharpness enhancement + noise layers
            - Multiple scale manipulations to change file hash
            
            **YouTube Anti-Algorithm:**
            - 16:9 letterbox + extreme saturation boost
            - Strong sharpening + color balance shifts
            - Curve adjustments + temporal noise patterns
            """)
        
        # Custom commands section
        st.header("💬 Custom Edit Commands")
        with st.expander("📋 All Available Commands (70+ Effects)", expanded=False):
            st.markdown("""
            **📹 Video Commands:**
            
            **Basic Adjustments:**
            - `flip horizontal/vertical` - Flip video
            - `speed 1.5` - Change playback speed
            - `zoom 1.2` - Zoom in/out
            - `rotate 90` - Rotate by degrees
            - `slow 20%` - Slow down by percentage
            - `brightness 120`, `contrast 110`, `saturation 1.3`
            - `gamma 1.2`, `hue 30`, `temperature 200`
            
            **Visual Effects:**
            - `blur 5`, `sharpen 1.5`, `grain 25`, `noise 15`
            - `glitch 10`, `chromatic 3`, `vhs`, `film`
            - `sepia`, `invert`, `vintage`, `fade 0.3`
            - `mirror horizontal`, `kaleidoscope 6`, `wave 10`
            - `pixelate 8`, `oil 4`, `emboss`, `edge`
            - `solarize 128`, `posterize 4`, `vignette 0.8`
            
            **Advanced Effects:**
            - `letterbox`, `crop_zoom 1.2`, `stabilize`
            - `framerate 30`, `reverse`, `loop 2`
            - `echo 0.5`, `freeze 1.0`, `skip 1.0`
            - `audio_pitch 1.2`, `audio_echo 0.3`, `audio_bass 5`
            
            **🖼️ Image Commands:**
            
            **Basic Adjustments:**
            - `flip vertical/horizontal` - Flip image
            - `brightness 120`, `contrast 110`, `color 120`
            - `crop square`, `rotate 45`, `tilt 2.0`
            - `gamma 1.2`, `hue 30`, `saturation 1.3`
            - `temperature 200`, `fade 0.3`, `compression 70`
            
            **Creative Effects:**
            - `blur 5`, `sharpen 1.5`, `grain 25`, `noise 15`
            - `glitch 10`, `chromatic 3`, `vhs`, `film`
            - `sepia`, `invert`, `vintage`, `mirror`
            - `kaleidoscope 6`, `wave 10`, `pixelate 8`
            - `oil 4`, `emboss`, `edge`, `solarize 128`
            - `posterize 4`, `vignette 0.8`, `dither`
            
            **Artistic Styles:**
            - `sketch`, `cartoon`, `watercolor`, `pencil`
            - `mosaic 20`, `cross_hatch`, `stipple`, `ascii`
            - `thermal`, `x_ray`, `night_vision`, `halftone 15`
            
            **Shape Effects:**
            - `square`, `portrait`, `landscape`, `letterbox`
            - `fisheye 0.8`, `barrel 0.3`, `perspective`
            - `crop_zoom 1.2`
            
            **💡 Usage Examples:**
            - Single effect: `blur 10`
            - Multiple effects: `sepia + grain 20 + vignette 0.5`
            - Complex combo: `glitch 15 + chromatic 5 + film + noise 25`
            """)
        
        custom_command = st.text_input(
            "Enter custom edit command:",
            placeholder="e.g., 'glitch 15 + chromatic 5 + film + vignette 0.8 + noise 25'",
            disabled=st.session_state.processing
        )
        
        if st.button("🚀 Apply Custom Edit", disabled=st.session_state.processing or not custom_command):
            process_custom_command(uploaded_file, custom_command, file_details, processors)
        
        # Processing indicator
        if st.session_state.processing:
            with st.spinner("Processing your media... Please wait."):
                time.sleep(0.1)  # Small delay to show spinner
        
    # Processing results and comparison section
    if st.session_state.processed_file and uploaded_file is not None:
        st.header("🔄 Original vs Processed Comparison")
        
        if st.session_state.file_details['category'] == 'image':
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📸 Original Image")
                st.image(uploaded_file, caption="Original", use_container_width=True)
            with col2:
                st.subheader(f"✨ Processed ({st.session_state.current_platform.title() if st.session_state.current_platform else 'Custom'})")
                st.image(st.session_state.processed_file, caption="Algorithm-Evaded", use_container_width=True)
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("🎥 Original Video")
                st.video(uploaded_file)
            with col2:
                st.subheader(f"✨ Processed ({st.session_state.current_platform.title() if st.session_state.current_platform else 'Custom'})")
                st.video(st.session_state.processed_file)
        
        # Download section
        st.header("⬇️ Download Your Anti-Algorithm Media")
        
        # File size comparison
        original_size = len(uploaded_file.getvalue())
        with open(st.session_state.processed_file, "rb") as file:
            processed_data = file.read()
            processed_size = len(processed_data)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Original Size", processors['file_utils']._format_file_size(original_size))
        with col2:
            st.metric("Processed Size", processors['file_utils']._format_file_size(processed_size))
        with col3:
            size_change = ((processed_size - original_size) / original_size) * 100
            st.metric("Size Change", f"{size_change:+.1f}%")
        
        # Download button
        file_name = Path(st.session_state.processed_file).name
        platform_prefix = st.session_state.current_platform if st.session_state.current_platform else "custom"
        
        st.download_button(
            label=f"📥 Download {platform_prefix.title()}-Ready File",
            data=processed_data,
            file_name=f"anti_algorithm_{platform_prefix}_{uploaded_file.name}",
            mime=processors['file_utils'].get_mime_type(file_name),
            use_container_width=True,
            type="primary"
        )
        
        st.success(f"✅ File successfully processed for {platform_prefix.title()}! The algorithm won't recognize this as the original.")
        
        # Reset button
        if st.button("🔄 Process Different File", use_container_width=True):
            st.session_state.processed_file = None
            st.session_state.current_platform = None
            st.rerun()

def process_media_preset(uploaded_file, platform, file_details, processors):
    """Unified function to process media with platform preset"""
    try:
        # Create temp file with appropriate extension
        if file_details['category'] == 'video':
            suffix = '.mp4'
            processor = processors['video']
        else:
            suffix = '.jpg' 
            processor = processors['image']
        
        # Reset file pointer and read data
        uploaded_file.seek(0)
        file_data = uploaded_file.read()
        
        # Create temporary input file
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_input:
            temp_input.write(file_data)
            temp_input_path = temp_input.name
        
        # Process the file
        output_path = processor.apply_preset(temp_input_path, platform)
        
        # Update session state
        st.session_state.processed_file = output_path
        st.success(f"✅ Successfully processed {file_details['type'].lower()} for {platform.title()} with advanced algorithm evasion!")
        
        # Show detailed changes made
        st.info(f"""
        **Applied {platform.title()} Anti-Algorithm Modifications:**
        - Advanced noise patterns and LSB steganography
        - Perceptual hash evasion through gradient perturbations  
        - DCT domain modifications to bypass compression detection
        - Color channel manipulation and micro-transformations
        - File hash changes through scale and rotation adjustments
        """)
        
    except Exception as e:
        st.error(f"❌ Error processing {file_details['type'].lower()}: {str(e)}")
        import traceback
        st.error(f"Debug details: {traceback.format_exc()}")
    finally:
        # Cleanup temp file
        if 'temp_input_path' in locals():
            try:
                os.unlink(temp_input_path)
            except:
                pass

def process_custom_command(uploaded_file, command, file_details, processors):
    """Unified function to process media with custom command"""
    st.session_state.processing = True
    st.rerun()
    
    try:
        # Create temp file with appropriate extension
        if file_details['category'] == 'video':
            suffix = '.mp4'
            processor = processors['video']
            media_type = 'video'
        else:
            suffix = '.jpg'
            processor = processors['image']
            media_type = 'image'
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_input:
            temp_input.write(uploaded_file.read())
            temp_input_path = temp_input.name
        
        parsed_commands = processors['command'].parse_command(command, media_type)
        if not parsed_commands:
            st.error("❌ No valid commands found. Please check your command syntax.")
            return
            
        output_path = processor.apply_custom_commands(temp_input_path, parsed_commands)
        st.session_state.processed_file = output_path
        st.success(f"✅ Custom {file_details['type'].lower()} processing completed with your specified modifications!")
        
    except Exception as e:
        st.error(f"❌ Error processing {file_details['type'].lower()}: {str(e)}")
        st.error("Please check your command syntax or try a different file.")
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
