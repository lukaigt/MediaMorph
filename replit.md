# Smart Anti-Algorithm Repost Assistant

## Overview

A Streamlit-based web application that helps users transform videos and images for safe social media reposting using advanced algorithm evasion techniques. The application applies sophisticated modifications including LSB steganography, perceptual hash evasion, DCT domain transformations, and multi-layer noise patterns to help content bypass modern AI-driven algorithm detection while maintaining visual quality. It supports multiple social media platforms including TikTok, Instagram, and YouTube, with heavy anti-algorithm presets optimized for each platform's detection systems.

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
- **Advanced Video Processing**: FFmpeg-based transformations with multi-layer modifications including horizontal flip, speed adjustment, zoom effects, strong noise patterns, color balance shifts, and hash-changing scale operations
- **Sophisticated Image Processing**: PIL and scipy-based operations featuring LSB steganography, perceptual hash evasion, DCT domain modifications, gradient-based perturbations, color channel manipulation, and micro-transformations
- **Heavy Anti-Algorithm Presets**: Research-based transformation chains designed to evade 2025 AI detection systems for each social media platform
- **Advanced Command System**: Flexible parsing for custom transformation combinations with algorithm evasion techniques

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

The application operates entirely offline without external API dependencies, processing all media locally using system resources.