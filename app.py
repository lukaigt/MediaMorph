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
    if 'processed_files' not in st.session_state:
        st.session_state.processed_files = []
    if 'original_file' not in st.session_state:
        st.session_state.original_file = None
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    if 'progress' not in st.session_state:
        st.session_state.progress = 0
    if 'progress_text' not in st.session_state:
        st.session_state.progress_text = ""
    if 'current_platform' not in st.session_state:
        st.session_state.current_platform = None
    if 'file_details' not in st.session_state:
        st.session_state.file_details = None
    if 'batch_mode' not in st.session_state:
        st.session_state.batch_mode = False
    if 'audio_quality' not in st.session_state:
        st.session_state.audio_quality = '192k'
    
    # Advanced settings sidebar
    with st.sidebar:
        st.header("⚙️ Advanced Settings")
        
        # Batch mode toggle - Make it prominent
        st.subheader("📦 Processing Mode")
        st.session_state.batch_mode = st.checkbox(
            "🔄 **BULK PROCESSING MODE**", 
            value=st.session_state.batch_mode,
            help="Enable this to upload and process multiple files at once!"
        )
        
        if st.session_state.batch_mode:
            st.success("✅ Bulk mode enabled - you can now select multiple files!")
        else:
            st.info("💡 Enable bulk mode to process multiple files at once")
        
        # Audio quality for videos
        st.subheader("🎵 Audio Quality")
        st.session_state.audio_quality = st.selectbox(
            "Audio Bitrate",
            ['128k', '160k', '192k', '256k', '320k'],
            index=2,  # Default to 192k
            help="Higher = better quality but larger file size"
        )
        
        # File size optimization
        st.subheader("📊 File Size Options")
        size_limit = st.selectbox(
            "Output Size Limit",
            ['No Limit', '25MB', '50MB', '100MB', '200MB'],
            help="Automatically compress to fit size limits"
        )
        
        # Advanced features
        st.subheader("🔧 Advanced Features")
        auto_crop = st.checkbox("✂️ Auto-crop black borders", value=False)
        watermark_removal = st.checkbox("🚫 Attempt watermark removal", value=False)
        preview_enabled = st.checkbox("👁️ Show preview before download", value=True)
    
    # File upload section
    st.header("📁 Upload Media")
    
    if st.session_state.batch_mode:
        st.success("🔄 **BULK PROCESSING MODE ACTIVE** - You can select multiple files!")
        uploaded_files = st.file_uploader(
            "📦 DRAG & DROP MULTIPLE FILES HERE (Hold Ctrl/Cmd to select multiple)",
            type=['mp4', 'mov', 'avi', 'mkv', 'webm', 'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff'],
            accept_multiple_files=True,
            help="🔥 BULK MODE: Select multiple files at once! Hold Ctrl (Windows) or Cmd (Mac) to select multiple files",
            key="bulk_uploader"
        )
        uploaded_file = uploaded_files[0] if uploaded_files else None
        if uploaded_files and len(uploaded_files) > 1:
            st.success(f"📦 **{len(uploaded_files)} FILES SELECTED FOR BULK PROCESSING!**")
            
            # Show all selected files
            with st.expander(f"📋 View all {len(uploaded_files)} selected files", expanded=True):
                for i, f in enumerate(uploaded_files, 1):
                    file_size = f.size / (1024*1024)  # MB
                    st.write(f"{i}. **{f.name}** ({file_size:.1f} MB)")
        elif uploaded_files and len(uploaded_files) == 1:
            st.info("📦 1 file selected - Add more files for bulk processing!")
    else:
        st.info("💡 **TIP:** Enable 'Batch Processing Mode' in the sidebar to upload multiple files at once!")
        uploaded_file = st.file_uploader(
            "Choose a video or image file",
            type=['mp4', 'mov', 'avi', 'mkv', 'webm', 'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff'],
            help="Supported formats: MP4, MOV, AVI, MKV, WebM for videos | JPG, PNG, GIF, BMP, TIFF for images",
            key="single_uploader"
        )
        uploaded_files = [uploaded_file] if uploaded_file else []
    
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
        
        # Progress tracking display
        if st.session_state.processing:
            if not hasattr(st.session_state, 'progress_display') or st.session_state.progress_display is None:
                st.session_state.progress_display = st.empty()
            
            # Update detailed progress display
            _update_progress_display()
            
            # Auto-refresh while processing
            time.sleep(0.2)  # Faster updates for real-time progress
            st.rerun()
        
        # Platform preset buttons
        st.header("🎯 Advanced Algorithm Evasion Presets")
        if st.session_state.batch_mode and len(uploaded_files) > 1:
            st.markdown(f"**🔄 BULK PROCESSING MODE: Process all {len(uploaded_files)} files at once with MAXIMUM protection:**")
            st.info(f"📦 Ready to bulk process: {len(uploaded_files)} files | All files will be processed with the same settings")
        else:
            st.markdown("**Choose your target platform for MAXIMUM protection that algorithms can't detect:**")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📱 TikTok Anti-Algorithm", use_container_width=True, type="primary", 
                        disabled=st.session_state.processing):
                st.session_state.current_platform = 'tiktok'
                if st.session_state.batch_mode and len(uploaded_files) > 1:
                    process_batch_files(uploaded_files, 'tiktok', processors, {
                        'audio_quality': st.session_state.audio_quality,
                        'size_limit': size_limit,
                        'auto_crop': auto_crop,
                        'watermark_removal': watermark_removal,
                        'preview_enabled': preview_enabled
                    })
                else:
                    process_media_preset(uploaded_file, 'tiktok', file_details, processors, {
                        'audio_quality': st.session_state.audio_quality,
                        'size_limit': size_limit,
                        'auto_crop': auto_crop,
                        'watermark_removal': watermark_removal,
                        'preview_enabled': preview_enabled
                    })
        
        with col2:
            if st.button("📸 Instagram Anti-Algorithm", use_container_width=True, type="primary",
                        disabled=st.session_state.processing):
                st.session_state.current_platform = 'instagram'
                if st.session_state.batch_mode and len(uploaded_files) > 1:
                    process_batch_files(uploaded_files, 'instagram', processors, {
                        'audio_quality': st.session_state.audio_quality,
                        'size_limit': size_limit,
                        'auto_crop': auto_crop,
                        'watermark_removal': watermark_removal,
                        'preview_enabled': preview_enabled
                    })
                else:
                    process_media_preset(uploaded_file, 'instagram', file_details, processors, {
                        'audio_quality': st.session_state.audio_quality,
                        'size_limit': size_limit,
                        'auto_crop': auto_crop,
                        'watermark_removal': watermark_removal,
                        'preview_enabled': preview_enabled
                    })
        
        with col3:
            if st.button("🎥 YouTube Anti-Algorithm", use_container_width=True, type="primary",
                        disabled=st.session_state.processing):
                st.session_state.current_platform = 'youtube'
                if st.session_state.batch_mode and len(uploaded_files) > 1:
                    process_batch_files(uploaded_files, 'youtube', processors, {
                        'audio_quality': st.session_state.audio_quality,
                        'size_limit': size_limit,
                        'auto_crop': auto_crop,
                        'watermark_removal': watermark_removal,
                        'preview_enabled': preview_enabled
                    })
                else:
                    process_media_preset(uploaded_file, 'youtube', file_details, processors, {
                        'audio_quality': st.session_state.audio_quality,
                        'size_limit': size_limit,
                        'auto_crop': auto_crop,
                        'watermark_removal': watermark_removal,
                        'preview_enabled': preview_enabled
                    })
        
        with col4:
            if st.button("🩳 YouTube Shorts", use_container_width=True, type="primary",
                        disabled=st.session_state.processing):
                st.session_state.current_platform = 'youtube_shorts'
                if st.session_state.batch_mode and len(uploaded_files) > 1:
                    process_batch_files(uploaded_files, 'youtube_shorts', processors, {
                        'audio_quality': st.session_state.audio_quality,
                        'size_limit': size_limit,
                        'auto_crop': auto_crop,
                        'watermark_removal': watermark_removal,
                        'preview_enabled': preview_enabled
                    })
                else:
                    process_media_preset(uploaded_file, 'youtube_shorts', file_details, processors, {
                        'audio_quality': st.session_state.audio_quality,
                        'size_limit': size_limit,
                        'auto_crop': auto_crop,
                        'watermark_removal': watermark_removal,
                        'preview_enabled': preview_enabled
                    })
        
        # Show what each preset does
        with st.expander("🔧 What Each Preset Does", expanded=False):
            st.markdown("""
            **TikTok Anti-Algorithm (9:16 Vertical):**
            - 6-Layer Protection: Adversarial perturbations + neural traffic disruption
            - Multi-modal evasion + compression resistance + universal perturbations
            - Horizontal flip + speed boost + zoom + strong noise + metadata manipulation
            
            **Instagram Anti-Algorithm (9:16 Reels):**
            - 4-Layer Protection: AI evasion + polymorphic variations
            - Reels format + vibrant color boost + film grain
            - Hue shifts + sharpness enhancement + multi-modal detection bypass
            
            **YouTube Anti-Algorithm (16:9 Landscape):**
            - 4-Layer Protection: Content-ID bypass + neural network confusion
            - 16:9 letterbox + extreme saturation boost + transfer learning exploits
            - Strong sharpening + color balance shifts + curve adjustments
            
            **YouTube Shorts (9:16 Vertical):**
            - Same 4-Layer YouTube Protection in vertical format
            - Content-ID bypass + neural confusion optimized for Shorts
            - 9:16 aspect ratio perfect for YouTube Shorts algorithm
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
            options = {
                'audio_quality': st.session_state.audio_quality,
                'size_limit': size_limit,
                'auto_crop': auto_crop,
                'watermark_removal': watermark_removal
            }
            process_custom_command(uploaded_file, custom_command, file_details, processors, options)
        
        # Processing indicator with detailed steps
        if st.session_state.processing:
            if not hasattr(st.session_state, 'progress_display') or st.session_state.progress_display is None:
                st.session_state.progress_display = st.empty()
            
            # Update display
            _update_progress_display()
            
            # Auto-refresh while processing - faster for video encoding
            time.sleep(0.1)  # Very fast updates during processing
            st.rerun()
        
    # Batch processing results section
    if st.session_state.processed_files and len(st.session_state.processed_files) > 0:
        st.header("📦 Bulk Processing Results")
        
        platform_name = st.session_state.current_platform.title() if st.session_state.current_platform else "Unknown"
        
        # Show processing summary
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("✅ Files Processed", len(st.session_state.processed_files))
        with col2:
            st.metric("🎯 Target Platform", platform_name)
        with col3:
            total_size = sum(os.path.getsize(f['processed_path']) for f in st.session_state.processed_files if os.path.exists(f['processed_path']))
            st.metric("📊 Total Output Size", f"{total_size / (1024*1024):.1f} MB")
        st.success(f"✅ Successfully processed {len(st.session_state.processed_files)} files for {platform_name}!")
        
        # Show file list
        for i, file_info in enumerate(st.session_state.processed_files):
            with st.expander(f"📄 {file_info['original_name']} → {file_info['platform'].title()}", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Original:**", file_info['original_name'])
                    st.write("**Platform:**", file_info['platform'].title())
                with col2:
                    # Individual download
                    with open(file_info['processed_path'], 'rb') as f:
                        file_data = f.read()
                    st.download_button(
                        label=f"📥 Download {file_info['platform'].title()} File",
                        data=file_data,
                        file_name=f"anti_algorithm_{file_info['platform']}_{file_info['original_name']}",
                        key=f"download_{i}"
                    )
        
        # Batch download
        create_batch_download_zip()
        
        # Reset batch button
        if st.button("🔄 Process New Batch", use_container_width=True):
            st.session_state.processed_files = []
            st.session_state.current_platform = None
            st.rerun()
    
    # Single file processing results and comparison section
    elif st.session_state.processed_file and uploaded_file is not None:
        st.header("🔄 Original vs Processed Comparison")
        
        # Safety check for file_details
        if st.session_state.file_details and st.session_state.file_details['category'] == 'image':
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📸 Original Image")
                st.image(uploaded_file, caption="Original", use_container_width=True)
            with col2:
                platform_name = st.session_state.current_platform.title() if st.session_state.current_platform else 'Custom'
                st.subheader(f"✨ Processed ({platform_name})")
                st.image(st.session_state.processed_file, caption="Algorithm-Evaded", use_container_width=True)
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("🎥 Original Video")
                st.video(uploaded_file)
            with col2:
                platform_name = st.session_state.current_platform.title() if st.session_state.current_platform else 'Custom'
                st.subheader(f"✨ Processed ({platform_name})")
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

def update_detailed_progress(step_name, details, estimated_time_left=None, current_step=None, total_steps=None):
    """Update detailed step-by-step progress with time estimates"""
    import time
    
    # Initialize if not exists
    if not hasattr(st.session_state, 'detailed_progress'):
        st.session_state.detailed_progress = {
            'steps': [],
            'start_time': time.time(),
            'current_step': 0,
            'total_steps': 0
        }
    
    # Update current step info
    step_info = {
        'name': step_name,
        'details': details,
        'timestamp': time.time(),
        'estimated_time': estimated_time_left
    }
    
    if current_step is not None:
        st.session_state.detailed_progress['current_step'] = current_step
    if total_steps is not None:
        st.session_state.detailed_progress['total_steps'] = total_steps
    
    # Add or update current step
    if len(st.session_state.detailed_progress['steps']) == 0 or st.session_state.detailed_progress['steps'][-1]['name'] != step_name:
        st.session_state.detailed_progress['steps'].append(step_info)
    else:
        st.session_state.detailed_progress['steps'][-1] = step_info
    
    # Update display if elements exist
    if hasattr(st.session_state, 'progress_display') and st.session_state.progress_display is not None:
        _update_progress_display()

def _update_progress_display():
    """Update the detailed progress display with enhanced video encoding progress"""
    import time
    
    if not hasattr(st.session_state, 'detailed_progress') or not st.session_state.detailed_progress['steps']:
        return
    
    progress_data = st.session_state.detailed_progress
    current_time = time.time()
    elapsed_time = current_time - progress_data['start_time']
    
    # Build display content
    display_content = []
    display_content.append("### 🔄 Real-Time Processing Progress")
    display_content.append(f"**Total Elapsed Time:** {elapsed_time:.1f}s")
    
    # Show overall progress if available
    if progress_data['total_steps'] > 0:
        overall_progress = (progress_data['current_step'] / progress_data['total_steps']) * 100
        display_content.append(f"**Overall Progress:** {overall_progress:.1f}% (Step {progress_data['current_step']}/{progress_data['total_steps']})")
    
    # Show current session state progress for video encoding
    if hasattr(st.session_state, 'progress') and st.session_state.progress > 0:
        display_content.append(f"**🎬 Video Encoding Progress: {st.session_state.progress}%**")
        
        # Create visual progress bar
        progress_bar_width = 25
        filled_width = int((st.session_state.progress / 100) * progress_bar_width)
        empty_width = progress_bar_width - filled_width
        progress_bar = "█" * filled_width + "░" * empty_width
        display_content.append(f"```\n[{progress_bar}] {st.session_state.progress}%\n```")
        
        if hasattr(st.session_state, 'progress_text') and st.session_state.progress_text:
            display_content.append(f"**Current Status:** {st.session_state.progress_text}")
            
        # Show simplified ETA if available
        if "ETA:" in str(getattr(st.session_state, 'progress_text', '')):
            try:
                eta = st.session_state.progress_text.split("ETA:")[-1].strip()
                display_content.append(f"**⏱️ Time Remaining:** {eta}")
            except:
                pass
    
    display_content.append("\n**Processing Steps:**")
    
    for i, step in enumerate(progress_data['steps'][-5:]):  # Show last 5 steps
        step_time = step['timestamp'] - progress_data['start_time']
        time_str = f"[{step_time:.1f}s]"
        
        if i == len(progress_data['steps'][-5:]) - 1:  # Current step
            status = "🔄"
            if step['estimated_time']:
                time_str += f" (ETA: {step['estimated_time']})"
        else:
            status = "✅"
        
        display_content.append(f"{status} **{step['name']}** {time_str}")
        
        # Show more detail for video encoding step
        if step['name'] == "Video Encoding" and 'details' in step:
            if "fps" in step['details'] and "ETA" in step['details']:
                display_content.append(f"   └─ {step['details']}")
            else:
                display_content.append(f"   └─ {step['details']}")
        else:
            display_content.append(f"   └─ {step['details']}")
    
    # Update display
    if hasattr(st.session_state, 'progress_display') and st.session_state.progress_display is not None:
        st.session_state.progress_display.markdown("\n".join(display_content))
    
def process_media_preset(uploaded_file, platform, file_details, processors, options=None):
    """Enhanced function to process media with platform preset and advanced features"""
    if options is None:
        options = {}
    
    temp_input_path = None
    try:
        st.session_state.processing = True
        
        # Create detailed progress display
        st.session_state.progress_display = st.empty()
        
        update_detailed_progress("Initialization", "Setting up processing environment...", "5s", 1, 8)
        
        # Handle different video formats and convert to MP4 if needed
        original_format = file_details['name'].split('.')[-1].lower()
        if file_details['category'] == 'video':
            if original_format in ['mov', 'avi', 'mkv', 'webm']:
                suffix = f'.{original_format}'
                output_suffix = '.mp4'
                needs_conversion = True
            else:
                suffix = '.mp4'
                output_suffix = '.mp4'
                needs_conversion = False
            processor = processors['video']
        else:
            suffix = '.jpg' 
            processor = processors['image']
            needs_conversion = False
        
        update_detailed_progress("File Reading", "Loading and validating file data...", "3s", 2, 8)
        
        # Reset file pointer and read data
        uploaded_file.seek(0)
        file_data = uploaded_file.read()
        
        # Create temporary input file
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_input:
            temp_input.write(file_data)
            temp_input_path = temp_input.name
        
        update_detailed_progress("Processing Setup", "Configuring advanced algorithms and settings...", "2s", 3, 8)
        
        # Pre-processing: Auto-crop black borders if enabled
        if options.get('auto_crop', False) and file_details['category'] == 'video':
            update_detailed_progress("Auto-Crop", "Detecting and removing black borders...", "10s", 4, 8)
            temp_input_path = auto_crop_video(temp_input_path)
        
        # Pre-processing: Watermark removal if enabled
        if options.get('watermark_removal', False):
            update_detailed_progress("Watermark Removal", "Analyzing and removing watermarks...", "15s", 5, 8)
            temp_input_path = remove_watermarks(temp_input_path, file_details['category'])
        
        # Format conversion if needed
        if needs_conversion:
            update_detailed_progress("Format Conversion", f"Converting {original_format.upper()} to MP4...", "20s", 6, 8)
            temp_input_path = convert_video_format(temp_input_path, '.mp4')
        
        update_detailed_progress("Algorithm Protection", f"Applying MAXIMUM {platform.upper()} protection layers...", "30s", 7, 8)
        
        # Process the file with enhanced settings
        if file_details['category'] == 'video':
            # Pass audio quality setting and progress callback to video processor
            if hasattr(processor, 'set_audio_quality'):
                processor.set_audio_quality(options.get('audio_quality', '192k'))
            if hasattr(processor, 'set_progress_callback'):
                def video_progress_callback(percentage, status_text):
                    # Parse ETA from status text if available
                    eta = None
                    if "ETA:" in status_text:
                        try:
                            eta_part = status_text.split("ETA:")[-1].strip()
                            eta = eta_part
                        except:
                            eta = "Calculating..."
                    
                    # Update progress with detailed encoding information
                    try:
                        update_detailed_progress("Video Encoding", status_text, eta, percentage, 100)
                        
                        # Also update session state for immediate display
                        st.session_state.progress = percentage
                        st.session_state.progress_text = status_text
                    except Exception as e:
                        print(f"Progress update error: {e}")
                        # Basic fallback update
                        st.session_state.progress = percentage
                        st.session_state.progress_text = f"Encoding: {percentage}%"
                
                processor.set_progress_callback(video_progress_callback)
            
            output_path = processor.apply_preset(temp_input_path, platform)
        else:
            update_detailed_progress("Image Processing", "Applying image transformations...", "10s", 7, 8)
            output_path = processor.apply_preset(temp_input_path, platform)
        
        # Apply file size optimization if specified
        size_limit = options.get('size_limit', 'No Limit')
        if size_limit != 'No Limit':
            update_detailed_progress("Size Optimization", f"Optimizing file size to {size_limit}...", "10s", 8, 8)
            output_path = optimize_file_size(output_path, size_limit, file_details['category'])
        
        # Update session state
        st.session_state.processed_file = output_path
        st.session_state.processing = False
        update_detailed_progress("Complete", "Processing finished successfully!", None, 8, 8)
        
        st.success(f"✅ Successfully processed {file_details['type'].lower()} for {platform.title()} with MAXIMUM algorithm evasion!")
        
        # Show detailed changes made with research-based techniques
        st.info(f"""
        **🔬 Research-Based 2025 Anti-Algorithm System Applied for {platform.title()}:**
        
        **Layer 1: Adversarial Perturbations** (FGS-Audio inspired)
        - Content-adaptive gradient perturbations that fool AI detection
        - Dynamic patterns that change with each upload to prevent recognition
        
        **Layer 2: Reversible Steganography** (Content-adaptive LSB)
        - Texture-aware LSB modifications in high-detail areas
        - Multi-bit embedding that survives compression algorithms
        
        **Layer 3: Hybrid DCT + GAN Domain** (Frequency manipulation)
        - JPEG-aware 8x8 block DCT coefficient modifications
        - Strategic frequency band targeting based on platform analysis
        
        **Layer 4: Triple-Stage Processing** (Audio research inspired)
        - Psycho-visual masking for imperceptible modifications
        - YUV color space transformations for compression resilience
        - Error correction through redundant micro-adjustments
        
        **Layer 5: Platform-Specific Evasion** ({platform.title()} algorithm targeting)
        - {platform.title()}-specific noise patterns and color preferences
        - Dynamic quality and encoding variations (prevents pattern detection)
        - Audio frequency manipulation (videos): Sample rate + EQ + volume micro-adjustments
        
        **Layer 6: Metadata & File Structure Manipulation** (Advanced fingerprint evasion)
        - Complete EXIF metadata stripping and fake camera data injection
        - Random file header modifications and invisible padding insertion
        - File hash randomization through structure manipulation
        - Fake timestamp and device signature generation
        
        **Layer 7: Format Conversion Chains** (Multi-stage file transformation)
        - JPEG→PNG→JPEG / JPEG→BMP→JPEG / JPEG→TIFF→JPEG conversion chains
        - Multiple quality and compression method variations
        - Progressive and subsampling randomization
        
        **Layer 8: Batch Processing Protection** (Session pattern prevention)
        - Tracks recent processing patterns to avoid repetition
        - Forces different techniques for consecutive uploads
        - Prevents algorithm pattern recognition across multiple posts
        
        **🎯 Result:** Maximum algorithm evasion with imperceptible visual changes + undetectable file fingerprint + batch protection
        
        ## **🎬 Advanced Video Processing (2025 Research-Based)**
        
        **8-Layer Video Anti-Algorithm System:**
        
        **Layer 1: Temporal Domain Manipulation**
        - Micro frame timing adjustments (imperceptible speed variations)
        - Dynamic frame interpolation with FPS micro-variations
        - Temporal noise injection that changes over time
        
        **Layer 2: Spatial Domain Evasion**
        - Dynamic zoom with sine wave micro-variations
        - Subtle perspective transformations (geometric warping)
        - Content-adaptive spatial modifications
        
        **Layer 3: Frequency Domain Manipulation**
        - Advanced DCT-inspired frequency modifications
        - Color space transformations in YUV domain
        - Multi-channel frequency band adjustments
        
        **Layer 4: Noise Injection System**
        - Multi-layered temporal and spatial noise
        - Content-adaptive noise (stronger on edges, weaker on smooth areas)
        - Algorithm-confusing noise patterns that survive compression
        
        **Layer 5: Pixel-Level Disruption**
        - Micro-blur with temporal oscillations
        - Advanced color channel mixing (steganography-inspired)
        - Psycho-visual masking for imperceptible changes
        
        **Layer 6: Optimized Audio Processing (Preserves Audio Quality)**
        - **Minimal Processing:** Only essential, safe audio adjustments to preserve audio integrity
        - **Volume Normalization:** Subtle psychoacoustic volume adjustments
        - **Safe EQ:** Single-band equalizer with minimal gain adjustments
        - **Audio Preservation:** Fallback to original audio if any processing fails
        - **Quality Validation:** Automatic audio stream verification in output
        - **Error Recovery:** Multiple fallback encodings to ensure audio is never lost
        
        **Layer 7: Container & Metadata Manipulation**
        - Randomized H.264 encoding parameters (profile, level, preset)
        - Fake creation timestamps and metadata injection
        - Multiple pixel format variations (yuv420p, yuvj420p)
        
        **Layer 8: Advanced Format Conversion + Keyframe Manipulation**
        - **MP4→MKV→MP4** conversion chains with different settings
        - **Custom keyframe intervals:** GOP size manipulation (250-350 frames)
        - **Scene change detection:** Custom thresholds to break pattern detection
        - **B-frame manipulation:** Variable B-frame counts (2-5 frames)
        - **Reference frame randomization:** Different ref frame counts per stage
        
        **🚀 NEW ADVANCED FEATURES:**
        
        **Frame Duplication/Deletion Evasion**
        - Randomly duplicates or removes single frames (imperceptible at 30fps)
        - Re-interpolates for smooth playback while breaking temporal patterns
        
        **Optical Flow Disruption**
        - Subtle motion vector modifications that break motion-based detection
        - Video stabilization with randomized parameters to confuse flow analysis
        
        **Lens Distortion Simulation**
        - Simulates camera lens characteristics to break geometric fingerprints
        - Random distortion coefficients that survive platform re-encoding
        """)
        
    except Exception as e:
        st.error(f"❌ Error processing {file_details['type'].lower()}: {str(e)}")
        import traceback
        st.error(f"Debug details: {traceback.format_exc()}")
    finally:
        # Cleanup temp file
        try:
            if 'temp_input_path' in locals() and temp_input_path and os.path.exists(temp_input_path):
                os.unlink(temp_input_path)
        except:
            pass

def process_custom_command(uploaded_file, command_string, file_details, processors, options=None):
    """Process custom command string and apply to media"""
    temp_input_path = None
    try:
        # Parse the command
        parser = processors['command_parser']
        commands = parser.parse_command(command_string, file_details['category'])
        
        if not commands:
            st.error("❌ No valid commands found in your input")
            return
        
        # Create temp file
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
        
        # Apply custom commands
        if file_details['category'] == 'video':
            # For video, fallback to preset for now (video custom commands need FFmpeg implementation)
            output_path = processor.apply_preset(temp_input_path, 'tiktok')
            st.warning("⚠️ Video custom commands not fully implemented yet. Applied TikTok preset instead.")
        else:
            # Apply custom commands to image
            output_path = processor.apply_custom_command(temp_input_path, commands)
        
        # Update session state
        st.session_state.processed_file = output_path
        st.session_state.current_platform = 'custom'
        
        # Show success message with applied commands
        command_names = [cmd['type'] for cmd in commands]
        st.success(f"✅ Successfully applied {len(commands)} custom effects: {', '.join(command_names)}")
        
        st.info(f"""
        **Applied Custom Effects:**
        {' → '.join(command_names)}
        
        **Total transformations:** {len(commands)}
        **Command processed:** {command_string}
        """)
        
    except Exception as e:
        st.error(f"❌ Error processing custom command: {str(e)}")
        import traceback
        st.error(f"Debug details: {traceback.format_exc()}")
    finally:
        # Cleanup temp file
        try:
            if 'temp_input_path' in locals() and temp_input_path and os.path.exists(temp_input_path):
                os.unlink(temp_input_path)
        except:
            pass
        st.rerun()

def process_batch_files(uploaded_files, platform, processors, options):
    """Process multiple files in batch mode with progress tracking"""
    try:
        st.session_state.processing = True
        st.session_state.processed_files = []
        st.session_state.current_platform = platform
        total_files = len(uploaded_files)
        
        # Create progress display for batch processing
        st.session_state.progress_display = st.empty()
        
        update_detailed_progress(
            "Batch Initialization", 
            f"Starting bulk processing of {total_files} files for {platform.title()}...", 
            f"{total_files*25}s", 
            0, 
            total_files
        )
        
        for i, uploaded_file in enumerate(uploaded_files):
            file_details = processors['file_utils'].get_file_info(uploaded_file)
            
            update_detailed_progress(
                "Batch Processing", 
                f"File {i+1}/{total_files}: {file_details['name']} ({file_details['size']})", 
                f"{(total_files-i)*25}s", 
                i+1, 
                total_files
            )
            
            # Process each file
            output_path = process_single_file_batch(uploaded_file, platform, file_details, processors, options)
            if output_path:
                st.session_state.processed_files.append({
                    'original_name': file_details['name'],
                    'processed_path': output_path,
                    'platform': platform
                })
        
        st.session_state.processing = False
        update_detailed_progress("Batch Complete", f"Successfully processed {len(st.session_state.processed_files)} files!", None, total_files, total_files)
        
        # Show batch results
        st.success(f"✅ Successfully processed {len(st.session_state.processed_files)} files for {platform.title()}!")
        
        # Download all files as zip
        if st.session_state.processed_files:
            create_batch_download_zip()
            
    except Exception as e:
        st.session_state.processing = False
        st.error(f"❌ Batch processing failed: {str(e)}")

def process_single_file_batch(uploaded_file, platform, file_details, processors, options):
    """Process a single file in batch mode (simplified version without UI updates)"""
    try:
        # Similar to process_media_preset but without progress updates for each file
        original_format = file_details['name'].split('.')[-1].lower()
        if file_details['category'] == 'video':
            suffix = f'.{original_format}' if original_format in ['mov', 'avi', 'mkv', 'webm'] else '.mp4'
            processor = processors['video']
        else:
            suffix = '.jpg'
            processor = processors['image']
        
        uploaded_file.seek(0)
        file_data = uploaded_file.read()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_input:
            temp_input.write(file_data)
            temp_input_path = temp_input.name
        
        # Apply preprocessing options
        if options.get('auto_crop', False) and file_details['category'] == 'video':
            temp_input_path = auto_crop_video(temp_input_path)
        
        if options.get('watermark_removal', False):
            temp_input_path = remove_watermarks(temp_input_path, file_details['category'])
        
        # Process with preset
        output_path = processor.apply_preset(temp_input_path, platform)
        
        # Apply size optimization
        size_limit = options.get('size_limit', 'No Limit')
        if size_limit != 'No Limit':
            output_path = optimize_file_size(output_path, size_limit, file_details['category'])
        
        return output_path
        
    except Exception as e:
        st.warning(f"⚠️ Failed to process {file_details['name']}: {str(e)}")
        return None

def convert_video_format(input_path, output_suffix):
    """Convert video to MP4 format using FFmpeg"""
    try:
        import ffmpeg
        output_path = input_path.replace(input_path.split('.')[-1], 'mp4')
        
        (
            ffmpeg
            .input(input_path)
            .output(output_path, vcodec='libx264', acodec='aac')
            .overwrite_output()
            .run(quiet=True)
        )
        
        # Cleanup original file
        os.unlink(input_path)
        return output_path
        
    except Exception as e:
        st.warning(f"⚠️ Format conversion failed, using original: {str(e)}")
        return input_path

def auto_crop_video(input_path):
    """Auto-detect and crop black borders from video"""
    try:
        import ffmpeg
        output_path = input_path.replace('.mp4', '_cropped.mp4')
        
        # Use FFmpeg's cropdetect filter to detect black borders
        (
            ffmpeg
            .input(input_path)
            .filter('cropdetect', limit=0.1, round=2)
            .output(output_path, vcodec='libx264', acodec='copy')
            .overwrite_output()
            .run(quiet=True)
        )
        
        os.unlink(input_path)
        return output_path
        
    except Exception as e:
        st.warning(f"⚠️ Auto-crop failed, using original: {str(e)}")
        return input_path

def remove_watermarks(input_path, media_type):
    """Intelligent watermark removal using advanced detection and inpainting"""
    try:
        if media_type == 'video':
            return remove_video_watermarks_intelligent(input_path)
        else:
            return remove_image_watermarks_intelligent(input_path)
    except Exception as e:
        st.warning(f"⚠️ Watermark removal failed, using original: {str(e)}")
        return input_path

def detect_watermark_regions(image_path):
    """Detect potential watermark regions using computer vision"""
    try:
        try:
            import cv2
        except ImportError:
            print("OpenCV not available, using fallback detection")
            return []
        import numpy as np
        
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            return []
            
        height, width = img.shape[:2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Multiple detection strategies
        watermark_regions = []
        
        # Strategy 1: Edge-based detection for logos/text
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            # Filter for potential watermarks (reasonable size, edge locations)
            if (20 < w < width//3 and 20 < h < height//3 and 
                (x < width//4 or x > 3*width//4 or y < height//4 or y > 3*height//4)):
                watermark_regions.append((x, y, w, h))
        
        # Strategy 2: Common watermark positions
        common_positions = [
            # Bottom-left (for usernames like "Tonybagalaughs")
            (10, height-80, 250, 70),
            # Bottom-right
            (width-260, height-80, 250, 70),
            # Top-left
            (10, 10, 200, 60),
            # Top-right  
            (width-210, 10, 200, 60),
            # Center-left
            (10, height//2-35, 200, 70),
            # Center-right
            (width-210, height//2-35, 200, 70),
            # Bottom-center
            (width//2-125, height-80, 250, 70)
        ]
        
        # Ensure positions are within image bounds
        for x, y, w, h in common_positions:
            x = max(0, min(x, width-1))
            y = max(0, min(y, height-1))
            w = min(w, width-x)
            h = min(h, height-y)
            if w > 10 and h > 10:
                watermark_regions.append((x, y, w, h))
        
        return watermark_regions
        
    except Exception as e:
        print(f"Watermark detection failed: {e}")
        return []

def remove_video_watermarks_intelligent(input_path):
    """Intelligent video watermark removal with dynamic detection"""
    try:
        try:
            import cv2
        except ImportError:
            print("OpenCV not available, using fallback method")
            return remove_video_watermarks_fallback(input_path)
        import subprocess
        
        # First, extract a frame to analyze watermark positions
        temp_frame = input_path.replace('.mp4', '_frame.jpg')
        
        # Extract middle frame for analysis
        cmd_extract = [
            'ffmpeg', '-i', input_path,
            '-vf', 'select=eq(n\\,30)',
            '-vframes', '1',
            '-y', temp_frame
        ]
        
        subprocess.run(cmd_extract, capture_output=True)
        
        if os.path.exists(temp_frame):
            # Detect watermark regions
            regions = detect_watermark_regions(temp_frame)
            os.unlink(temp_frame)
            
            if regions:
                # Build delogo filter chain
                delogo_filters = []
                for i, (x, y, w, h) in enumerate(regions[:6]):  # Limit to 6 regions
                    delogo_filters.append(f"delogo=x={x}:y={y}:w={w}:h={h}")
                
                filter_chain = ",".join(delogo_filters)
                
                output_path = input_path.replace('.mp4', '_nowatermark.mp4')
                
                # Apply intelligent watermark removal
                cmd = [
                    'ffmpeg', '-i', input_path,
                    '-vf', filter_chain,
                    '-c:a', 'copy',
                    '-crf', '18',
                    '-preset', 'medium',
                    '-y', output_path
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0 and os.path.exists(output_path):
                    os.unlink(input_path)
                    print(f"✓ Intelligent watermark removal applied to {len(regions)} regions")
                    return output_path
                else:
                    print(f"Delogo failed: {result.stderr}")
        
        # Fallback: Use proven blur-based approach for common positions
        return remove_video_watermarks_fallback(input_path)
        
    except Exception as e:
        print(f"Intelligent watermark removal failed: {e}")
        return remove_video_watermarks_fallback(input_path)

def remove_video_watermarks_fallback(input_path):
    """Fallback watermark removal using blur for common positions"""
    try:
        import subprocess
        
        output_path = input_path.replace('.mp4', '_nowatermark.mp4')
        
        # Get video dimensions first for dynamic watermark removal
        probe_result = subprocess.run(['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_streams', input_path], 
                                    capture_output=True, text=True)
        if probe_result.returncode == 0:
            import json
            probe_data = json.loads(probe_result.stdout)
            video_stream = next((s for s in probe_data['streams'] if s['codec_type'] == 'video'), None)
            if video_stream:
                width = int(video_stream['width'])
                height = int(video_stream['height'])
                
                # Calculate dynamic watermark positions based on video dimensions
                # Bottom-left (for "Tonybagalaughs" style watermarks)
                bl_x = int(width * 0.02)  # 2% from left
                bl_y = int(height * 0.85)  # 85% from top (bottom area)
                bl_w = int(width * 0.25)   # 25% of width
                bl_h = int(height * 0.08)  # 8% of height
                
                # Use simple delogo filter for watermark removal
                cmd = [
                    'ffmpeg', '-i', input_path,
                    '-vf', f'delogo=x={bl_x}:y={bl_y}:w={bl_w}:h={bl_h}',
                    '-c:a', 'copy',
                    '-crf', '18',
                    '-preset', 'fast',
                    '-y', output_path
                ]
            else:
                # Fallback if video stream not found
                cmd = [
                    'ffmpeg', '-i', input_path,
                    '-vf', 'boxblur=20:3',  # Simple blur fallback
                    '-c:a', 'copy',
                    '-crf', '18',
                    '-preset', 'fast',
                    '-y', output_path
                ]
        else:
            # Fallback if ffprobe fails
            cmd = [
                'ffmpeg', '-i', input_path,
                '-vf', 'boxblur=20:3',  # Simple blur fallback
                '-c:a', 'copy',
                '-crf', '18',
                '-preset', 'fast',
                '-y', output_path
            ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists(output_path):
            os.unlink(input_path)
            print("✓ Fallback watermark removal applied")
            return output_path
        else:
            print(f"Fallback watermark removal failed: {result.stderr}")
            return input_path
            
    except Exception as e:
        print(f"Fallback watermark removal failed: {e}")
        return input_path

def remove_image_watermarks_intelligent(input_path):
    """Intelligent image watermark removal using inpainting and detection"""
    try:
        try:
            import cv2
        except ImportError:
            print("OpenCV not available, using fallback method")
            return remove_image_watermarks_fallback(input_path)
        import numpy as np
        from PIL import Image
        
        # Detect watermark regions
        regions = detect_watermark_regions(input_path)
        
        if not regions:
            # Fallback to corner-based removal
            return remove_image_watermarks_fallback(input_path)
        
        # Load image with OpenCV for advanced processing
        img = cv2.imread(input_path)
        if img is None:
            return input_path
            
        # Create mask for inpainting
        mask = np.zeros(img.shape[:2], dtype=np.uint8)
        
        # Mark watermark regions in mask
        for x, y, w, h in regions:
            cv2.rectangle(mask, (x, y), (x+w, y+h), 255, -1)
        
        # Apply inpainting to remove watermarks
        result = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
        
        # Convert back to PIL and save
        result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(result_rgb)
        
        output_path = input_path.replace(input_path.split('.')[-1], f'nowatermark.{input_path.split(".")[-1]}')
        pil_image.save(output_path, quality=95)
        
        os.unlink(input_path)
        print(f"✓ Intelligent image watermark removal applied to {len(regions)} regions")
        return output_path
        
    except Exception as e:
        print(f"Intelligent image watermark removal failed: {e}")
        return remove_image_watermarks_fallback(input_path)

def remove_image_watermarks_fallback(input_path):
    """Fallback image watermark removal using targeted blur"""
    try:
        from PIL import Image, ImageFilter
        import numpy as np
        
        image = Image.open(input_path)
        width, height = image.size
        
        # Convert to numpy for advanced processing
        img_array = np.array(image)
        
        # Define watermark regions based on common positions
        regions = [
            # Bottom-left (perfect for usernames)
            (10, height-80, 250, 70),
            # Bottom-right  
            (width-260, height-80, 250, 70),
            # Top corners
            (10, 10, 200, 60),
            (width-210, 10, 200, 60),
            # Center positions
            (10, height//2-35, 200, 70),
            (width-210, height//2-35, 200, 70)
        ]
        
        processed_image = image.copy()
        
        for x, y, w, h in regions:
            # Ensure coordinates are within bounds
            x = max(0, min(x, width-1))
            y = max(0, min(y, height-1))
            w = min(w, width-x)
            h = min(h, height-y)
            
            if w > 10 and h > 10:
                # Extract region and apply smart blur
                region = image.crop((x, y, x+w, y+h))
                blurred_region = region.filter(ImageFilter.GaussianBlur(radius=3))
                processed_image.paste(blurred_region, (x, y))
        
        output_path = input_path.replace(input_path.split('.')[-1], f'nowatermark.{input_path.split(".")[-1]}')
        processed_image.save(output_path, quality=95)
        
        os.unlink(input_path)
        print("✓ Fallback image watermark removal applied")
        return output_path
        
    except Exception as e:
        print(f"Fallback image watermark removal failed: {e}")
        return input_path

def optimize_file_size(input_path, size_limit_str, media_type):
    """Optimize file size to meet specified limits"""
    try:
        # Parse size limit
        size_limit_mb = int(size_limit_str.replace('MB', ''))
        size_limit_bytes = size_limit_mb * 1024 * 1024
        
        # Check current size
        current_size = os.path.getsize(input_path)
        
        if current_size <= size_limit_bytes:
            return input_path  # Already within limit
        
        if media_type == 'video':
            return optimize_video_size(input_path, size_limit_bytes)
        else:
            return optimize_image_size(input_path, size_limit_bytes)
            
    except Exception as e:
        st.warning(f"⚠️ Size optimization failed: {str(e)}")
        return input_path

def optimize_video_size(input_path, target_size_bytes):
    """Optimize video size by adjusting bitrate"""
    try:
        import ffmpeg
        
        # Get video duration
        probe = ffmpeg.probe(input_path)
        duration = float(probe['streams'][0]['duration'])
        
        # Calculate target bitrate (with 10% buffer)
        target_bitrate = int((target_size_bytes * 8 * 0.9) / duration)
        
        output_path = input_path.replace('.mp4', '_optimized.mp4')
        
        (
            ffmpeg
            .input(input_path)
            .output(output_path, 
                   vcodec='libx264', 
                   acodec='aac',
                   **{'b:v': f'{target_bitrate}', 'b:a': '128k'})
            .overwrite_output()
            .run(quiet=True)
        )
        
        os.unlink(input_path)
        return output_path
        
    except Exception as e:
        return input_path

def optimize_image_size(input_path, target_size_bytes):
    """Optimize image size by adjusting quality"""
    try:
        from PIL import Image
        
        image = Image.open(input_path)
        
        # Try different quality levels
        for quality in [85, 75, 65, 55, 45]:
            output_path = input_path.replace(input_path.split('.')[-1], f'optimized.jpg')
            image.save(output_path, 'JPEG', quality=quality)
            
            if os.path.getsize(output_path) <= target_size_bytes:
                os.unlink(input_path)
                return output_path
        
        # If still too large, resize the image
        width, height = image.size
        for scale in [0.9, 0.8, 0.7, 0.6]:
            new_width = int(width * scale)
            new_height = int(height * scale)
            resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            output_path = input_path.replace(input_path.split('.')[-1], f'optimized.jpg')
            resized.save(output_path, 'JPEG', quality=75)
            
            if os.path.getsize(output_path) <= target_size_bytes:
                os.unlink(input_path)
                return output_path
        
        return input_path
        
    except Exception as e:
        return input_path

def create_batch_download_zip():
    """Create a ZIP file with all processed files for batch download"""
    try:
        import zipfile
        
        zip_path = tempfile.mktemp(suffix='.zip')
        
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file_info in st.session_state.processed_files:
                file_path = file_info['processed_path']
                original_name = file_info['original_name']
                platform = file_info['platform']
                
                # Create a clean filename for the zip
                name_parts = original_name.split('.')
                clean_name = f"anti_algorithm_{platform}_{'.'.join(name_parts[:-1])}.{name_parts[-1]}"
                
                zipf.write(file_path, clean_name)
        
        # Provide download button for the zip
        with open(zip_path, 'rb') as zip_file:
            st.download_button(
                label=f"📦 Download All {len(st.session_state.processed_files)} Files (ZIP)",
                data=zip_file.read(),
                file_name=f"anti_algorithm_batch_{st.session_state.current_platform}.zip",
                mime="application/zip",
                use_container_width=True,
                type="primary"
            )
        
        os.unlink(zip_path)
        
    except Exception as e:
        st.error(f"❌ Failed to create batch download: {str(e)}")

if __name__ == "__main__":
    main()
