# Smart Anti-Algorithm Repost Assistant

## Overview

A Streamlit-based web application that helps users transform videos and images for safe social media reposting. The application applies platform-specific modifications (flipping, color adjustments, noise, speed changes) to help content bypass algorithm detection while maintaining quality. It supports multiple social media platforms including TikTok, Instagram, and YouTube, with different processing presets optimized for each platform's algorithm patterns.

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
- **Video Processing**: FFmpeg-based transformations including horizontal flip, speed adjustment, zoom effects, and noise addition
- **Image Processing**: PIL-based operations for color enhancement, brightness adjustment, noise addition, and format conversion
- **Platform Presets**: Predefined transformation chains optimized for specific social media platforms
- **Command System**: Flexible command parsing for custom transformation combinations

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