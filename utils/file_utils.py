import os
from pathlib import Path

class FileUtils:
    def __init__(self):
        self.video_extensions = {'.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv'}
        self.image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
        
        self.mime_types = {
            '.mp4': 'video/mp4',
            '.mov': 'video/quicktime',
            '.avi': 'video/x-msvideo',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.bmp': 'image/bmp',
            '.tiff': 'image/tiff',
            '.webp': 'image/webp'
        }
    
    def get_file_info(self, uploaded_file):
        """Get file information from uploaded file"""
        file_size = len(uploaded_file.getvalue())
        file_name = uploaded_file.name
        file_extension = Path(file_name).suffix.lower()
        
        # Determine file category
        if file_extension in self.video_extensions:
            category = 'video'
            file_type = 'Video'
        elif file_extension in self.image_extensions:
            category = 'image'
            file_type = 'Image'
        else:
            category = 'unknown'
            file_type = 'Unknown'
        
        return {
            'name': file_name,
            'size': self._format_file_size(file_size),
            'type': file_type,
            'category': category,
            'extension': file_extension
        }
    
    def _format_file_size(self, size_bytes):
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    def get_mime_type(self, filename):
        """Get MIME type for file"""
        extension = Path(filename).suffix.lower()
        return self.mime_types.get(extension, 'application/octet-stream')
    
    def is_supported_file(self, filename):
        """Check if file is supported"""
        extension = Path(filename).suffix.lower()
        return extension in self.video_extensions or extension in self.image_extensions
    
    def cleanup_temp_files(self, file_paths):
        """Clean up temporary files"""
        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    os.unlink(file_path)
            except Exception:
                pass  # Ignore cleanup errors
