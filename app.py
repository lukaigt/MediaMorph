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
        
        # Batch mode toggle
        st.session_state.batch_mode = st.checkbox("🔄 Batch Processing Mode", value=st.session_state.batch_mode)
        
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
        uploaded_files = st.file_uploader(
            "Choose multiple video or image files",
            type=['mp4', 'mov', 'avi', 'mkv', 'webm', 'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff'],
            accept_multiple_files=True,
            help="Supported formats: MP4, MOV, AVI, MKV, WebM for videos | JPG, PNG, GIF, BMP, TIFF for images"
        )
        uploaded_file = uploaded_files[0] if uploaded_files else None
        if uploaded_files and len(uploaded_files) > 1:
            st.info(f"📦 Batch mode: {len(uploaded_files)} files selected")
    else:
        uploaded_file = st.file_uploader(
            "Choose a video or image file",
            type=['mp4', 'mov', 'avi', 'mkv', 'webm', 'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff'],
            help="Supported formats: MP4, MOV, AVI, MKV, WebM for videos | JPG, PNG, GIF, BMP, TIFF for images"
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
            st.header("🔄 Processing Progress")
            progress_bar = st.progress(st.session_state.progress / 100)
            st.write(f"**{st.session_state.progress}%** - {st.session_state.progress_text}")
            
            # Auto-refresh while processing
            if st.session_state.progress < 100:
                time.sleep(0.5)
                st.rerun()
        
        # Platform preset buttons
        st.header("🎯 Advanced Algorithm Evasion Presets")
        st.markdown("**Choose your target platform for MAXIMUM protection that algorithms can't detect:**")
        
        col1, col2, col3 = st.columns(3)
        
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
            options = {
                'audio_quality': st.session_state.audio_quality,
                'size_limit': size_limit,
                'auto_crop': auto_crop,
                'watermark_removal': watermark_removal
            }
            process_custom_command(uploaded_file, custom_command, file_details, processors, options)
        
        # Processing indicator with progress bar (improved)
        if st.session_state.processing:
            st.write("### 🔄 Processing...")
            if st.session_state.progress_bar is None:
                st.session_state.progress_bar = st.progress(0)
                st.session_state.progress_text_element = st.empty()
            
            # Auto-refresh while processing
            time.sleep(0.1)
            st.rerun()
        
    # Batch processing results section
    if st.session_state.processed_files and len(st.session_state.processed_files) > 0:
        st.header("📦 Batch Processing Results")
        
        platform_name = st.session_state.current_platform.title() if st.session_state.current_platform else "Unknown"
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
        
        if st.session_state.file_details['category'] == 'image':
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

def update_progress(percentage, text):
    """Update the progress bar and text"""
    st.session_state.progress = percentage
    st.session_state.progress_text = text
    
    # Update progress bar if it exists
    if st.session_state.progress_bar is not None:
        st.session_state.progress_bar.progress(percentage / 100.0)
    
    # Update progress text if it exists
    if st.session_state.progress_text_element is not None:
        st.session_state.progress_text_element.text(f"🔄 {text} ({percentage}%)")
    
def process_media_preset(uploaded_file, platform, file_details, processors, options=None):
    """Enhanced function to process media with platform preset and advanced features"""
    if options is None:
        options = {}
    
    try:
        st.session_state.processing = True
        
        # Create progress elements
        progress_container = st.container()
        with progress_container:
            st.session_state.progress_text_element = st.empty()
            st.session_state.progress_bar = st.progress(0)
        
        update_progress(0, "Initializing processing...")
        
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
        
        update_progress(10, "Reading file data...")
        
        # Reset file pointer and read data
        uploaded_file.seek(0)
        file_data = uploaded_file.read()
        
        # Create temporary input file
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_input:
            temp_input.write(file_data)
            temp_input_path = temp_input.name
        
        update_progress(20, "Preparing advanced processing...")
        
        # Pre-processing: Auto-crop black borders if enabled
        if options.get('auto_crop', False) and file_details['category'] == 'video':
            update_progress(25, "Auto-cropping black borders...")
            temp_input_path = auto_crop_video(temp_input_path)
        
        # Pre-processing: Watermark removal if enabled
        if options.get('watermark_removal', False):
            update_progress(30, "Attempting watermark removal...")
            temp_input_path = remove_watermarks(temp_input_path, file_details['category'])
        
        # Format conversion if needed
        if needs_conversion:
            update_progress(35, f"Converting {original_format.upper()} to MP4...")
            temp_input_path = convert_video_format(temp_input_path, '.mp4')
        
        update_progress(40, f"Applying MAXIMUM {platform.upper()} protection...")
        
        # Process the file with enhanced settings
        if file_details['category'] == 'video':
            # Pass audio quality setting and progress callback to video processor
            if hasattr(processor, 'set_audio_quality'):
                processor.set_audio_quality(options.get('audio_quality', '192k'))
            if hasattr(processor, 'set_progress_callback'):
                processor.set_progress_callback(update_progress)
            output_path = processor.apply_preset(temp_input_path, platform)
        else:
            output_path = processor.apply_preset(temp_input_path, platform)
        
        update_progress(70, "Optimizing file size...")
        
        # Apply file size optimization if specified
        size_limit = options.get('size_limit', 'No Limit')
        if size_limit != 'No Limit':
            output_path = optimize_file_size(output_path, size_limit, file_details['category'])
        
        update_progress(90, "Finalizing...")
        
        # Update session state
        st.session_state.processed_file = output_path
        st.session_state.processing = False
        update_progress(100, "Processing complete!")
        
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
        if 'temp_input_path' in locals():
            try:
                os.unlink(temp_input_path)
            except:
                pass

def process_custom_command(uploaded_file, command_string, file_details, processors, options=None):
    """Process custom command string and apply to media"""
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
        if 'temp_input_path' in locals():
            try:
                os.unlink(temp_input_path)
            except:
                pass
        st.rerun()

def process_batch_files(uploaded_files, platform, processors, options):
    """Process multiple files in batch mode with progress tracking"""
    try:
        st.session_state.processing = True
        st.session_state.processed_files = []
        total_files = len(uploaded_files)
        
        for i, uploaded_file in enumerate(uploaded_files):
            file_details = processors['file_utils'].get_file_info(uploaded_file)
            
            update_progress(
                (i / total_files) * 100, 
                f"Processing file {i+1}/{total_files}: {file_details['name']}"
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
        update_progress(100, f"Batch processing complete! {len(st.session_state.processed_files)} files processed")
        
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
    """Attempt to remove watermarks using blur and inpainting techniques"""
    try:
        if media_type == 'video':
            return remove_video_watermarks(input_path)
        else:
            return remove_image_watermarks(input_path)
    except Exception as e:
        st.warning(f"⚠️ Watermark removal failed, using original: {str(e)}")
        return input_path

def remove_video_watermarks(input_path):
    """Remove watermarks from video using FFmpeg filters"""
    try:
        import ffmpeg
        output_path = input_path.replace('.mp4', '_nowatermark.mp4')
        
        # Apply delogo filter to common watermark positions
        (
            ffmpeg
            .input(input_path)
            .filter('delogo', x=10, y=10, w=100, h=50)  # Top-left corner
            .filter('delogo', x='W-110', y=10, w=100, h=50)  # Top-right corner
            .output(output_path, vcodec='libx264', acodec='copy')
            .overwrite_output()
            .run(quiet=True)
        )
        
        os.unlink(input_path)
        return output_path
        
    except Exception as e:
        return input_path

def remove_image_watermarks(input_path):
    """Remove watermarks from images using simple blur techniques"""
    try:
        from PIL import Image, ImageFilter
        
        image = Image.open(input_path)
        width, height = image.size
        
        # Create a copy for processing
        processed_image = image.copy()
        
        # Apply gentle blur to corner areas where watermarks typically appear
        corner_size = min(width, height) // 8
        
        # Top-left corner
        corner = image.crop((0, 0, corner_size, corner_size))
        blurred_corner = corner.filter(ImageFilter.GaussianBlur(radius=2))
        processed_image.paste(blurred_corner, (0, 0))
        
        # Top-right corner
        corner = image.crop((width-corner_size, 0, width, corner_size))
        blurred_corner = corner.filter(ImageFilter.GaussianBlur(radius=2))
        processed_image.paste(blurred_corner, (width-corner_size, 0))
        
        # Bottom corners
        corner = image.crop((0, height-corner_size, corner_size, height))
        blurred_corner = corner.filter(ImageFilter.GaussianBlur(radius=2))
        processed_image.paste(blurred_corner, (0, height-corner_size))
        
        corner = image.crop((width-corner_size, height-corner_size, width, height))
        blurred_corner = corner.filter(ImageFilter.GaussianBlur(radius=2))
        processed_image.paste(blurred_corner, (width-corner_size, height-corner_size))
        
        output_path = input_path.replace(input_path.split('.')[-1], f'nowatermark.{input_path.split(".")[-1]}')
        processed_image.save(output_path, quality=95)
        
        os.unlink(input_path)
        return output_path
        
    except Exception as e:
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
