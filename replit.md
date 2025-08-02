# Smart Anti-Algorithm Repost Assistant

## Overview

A Streamlit-based web application that automatically applies the most advanced 2025 research-based anti-algorithm techniques to videos and images upon upload. The system implements a sophisticated 5-layer evasion framework including FGS-Audio inspired adversarial perturbations, reversible steganography, hybrid DCT+GAN frequency domain manipulation, triple-stage robust processing, and platform-specific algorithm targeting. Features dynamic variation system that randomizes parameters to prevent pattern detection across uploads, with specialized audio frequency manipulation for videos including sample rate adjustments, EQ filtering, and volume micro-variations.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application with a single-page interface
- **Layout**: Wide layout configuration with file upload widget and processing controls
- **State Management**: Streamlit session state for tracking processed files and processing status
- **Caching**: `@st.cache_resource` decorator for processor initialization to optimize performance

### Backend Architecture
- **Modular Design**: Processor-based architecture with separate modules for different media types
- **Core Processors**:
  - `VideoProcessor`: Handles video transformations using FFmpeg
  - `ImageProcessor`: Manages image manipulations using PIL (Pillow)
  - `CommandParser`: Parses user commands for custom transformations
- **File Management**: `FileUtils` class for file type detection and metadata extraction

### Processing Pipeline
- **8-Layer Anti-Algorithm Framework**: Research-based 2025 system implementing multiple evasion techniques per upload
  - Layer 1: FGS-Audio inspired adversarial perturbations with content-adaptive gradients
  - Layer 2: Reversible steganography with texture-aware LSB modifications
  - Layer 3: Hybrid DCT+GAN frequency domain manipulation in 8x8 JPEG blocks
  - Layer 4: Triple-stage processing (psycho-visual, YUV transform, error correction)
  - Layer 5: Platform-specific targeting (TikTok/Instagram/YouTube algorithm optimization)
  - Layer 6: Metadata & file structure manipulation (EXIF stripping, fake camera data, file hash randomization)
  - Layer 7: Format conversion chains (multi-stage file transformations to break additional fingerprinting)
  - Layer 8: Batch processing protection (session pattern prevention across multiple uploads)
- **Dynamic Variation System**: Time-based and randomized parameter selection to prevent pattern detection
- **Advanced Audio Processing**: Triple-stage audio manipulation with sample rate shifts, EQ filtering, and volume micro-adjustments
- **Custom Command System**: 47+ implemented image effects with full processing logic for manual control

### File Handling
- **Temporary Storage**: Uses system temp directory for processing intermediate files
- **Supported Formats**: 
  - Videos: MP4, MOV, AVI, MKV, WMV, FLV
  - Images: JPG, JPEG, PNG, GIF, BMP, TIFF, WebP
- **File Validation**: Extension-based type detection and MIME type mapping

## External Dependencies

### Core Libraries
- **Streamlit**: Web application framework for the user interface
- **FFmpeg-python**: Video processing and manipulation library
- **Pillow (PIL)**: Image processing and enhancement library
- **NumPy**: Array operations for image noise generation

### System Dependencies
- **FFmpeg**: Required system dependency for video processing operations
- **Python Standard Library**: `tempfile`, `pathlib`, `os`, `base64`, `time`, `re` for file operations and utilities

### Processing Dependencies
- **Video Codecs**: libx264 for video encoding, AAC for audio encoding
- **Image Formats**: JPEG compression and various image format support through Pillow
- **Advanced Mathematics**: SciPy for DCT transforms, ndimage operations, and frequency domain processing
- **Research Implementation**: 2025 academic techniques for adversarial perturbations and steganography

## Recent Major Updates (August 2025)

### Research-Based Anti-Algorithm System Implementation
- **Internet Research**: Conducted comprehensive analysis of 2025 anti-algorithm techniques
- **Academic Integration**: Implemented FGS-Audio framework, reversible steganography, hybrid DCT+GAN methods
- **Dynamic Randomization**: Added time-based variation system preventing algorithm pattern recognition
- **Audio Frequency Manipulation**: Integrated advanced audio processing with sample rate, EQ, and volume adjustments
- **Platform Optimization**: Specialized targeting for TikTok, Instagram, and YouTube detection systems
- **Custom Effects**: Completed implementation of all 47 image processing effects with full visual logic
- **Metadata Manipulation**: Added comprehensive EXIF stripping, fake camera metadata injection, and file structure randomization
- **File Fingerprint Evasion**: Implemented invisible file header modifications and random padding insertion for hash evasion
- **Format Conversion Chains**: Added 5 different multi-stage conversion methods (JPEG→PNG→JPEG, quality chains, compression variations)
- **Batch Protection System**: Implemented session memory to prevent pattern detection across consecutive uploads

### Revolutionary Video Processing Overhaul (August 2025)
- **8-Layer Video System**: Complete video processing overhaul with temporal, spatial, and frequency domain manipulation
- **Optimized Audio Processing**: Safe, minimal audio processing with quality preservation and fallback systems
- **Frame Manipulation Evasion**: Frame duplication/deletion that's imperceptible but breaks temporal fingerprints
- **Optical Flow Disruption**: Motion vector modifications that confuse motion-based detection algorithms
- **Lens Distortion Simulation**: Camera lens characteristic simulation for geometric fingerprint evasion
- **Advanced Keyframe Manipulation**: GOP size control, scene detection thresholds, B-frame randomization
- **Container Format Chains**: MP4→MKV→MP4 conversion with different encoding settings per stage
- **Video Batch Protection**: 10-minute session windows with 8 variation types for optimal pattern prevention
- **Audio Preservation**: Audio integrity validation, error recovery, and fallback encoding to prevent audio loss

The application operates entirely offline without external API dependencies, processing all media locally using system resources.