import ffmpeg
import tempfile
import os
from pathlib import Path

class VideoProcessor:
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
    
    def apply_preset(self, input_path, platform):
        """Apply platform-specific preset to video"""
        output_path = os.path.join(self.temp_dir, f"processed_{platform}_{Path(input_path).stem}.mp4")
        
        if platform == 'tiktok':
            return self._apply_tiktok_preset(input_path, output_path)
        elif platform == 'instagram':
            return self._apply_instagram_preset(input_path, output_path)
        elif platform == 'youtube':
            return self._apply_youtube_preset(input_path, output_path)
        else:
            raise ValueError(f"Unknown platform: {platform}")
    
    def _apply_tiktok_preset(self, input_path, output_path):
        """TikTok: Flip + speed up + zoom + glitch effect"""
        try:
            (
                ffmpeg
                .input(input_path)
                .video
                .filter('hflip')  # Horizontal flip
                .filter('setpts', '0.9*PTS')  # Speed up by 10%
                .filter('zoompan', zoom='1.1', x='iw/2-(iw/zoom/2)', y='ih/2-(ih/zoom/2)', d=1)  # Zoom effect
                .filter('noise', alls=20, allf='t+u')  # Glitch effect
                .output(output_path, acodec='aac', vcodec='libx264', crf=23)
                .overwrite_output()
                .run(quiet=True)
            )
            return output_path
        except ffmpeg.Error as e:
            raise Exception(f"FFmpeg error in TikTok preset: {e}")
    
    def _apply_instagram_preset(self, input_path, output_path):
        """Instagram: Square crop + color boost + grain"""
        try:
            (
                ffmpeg
                .input(input_path)
                .video
                .filter('crop', 'min(iw,ih)', 'min(iw,ih)')  # Square crop
                .filter('eq', saturation=1.2, brightness=0.1)  # Color boost
                .filter('noise', alls=10, allf='t')  # Film grain
                .output(output_path, acodec='aac', vcodec='libx264', crf=23)
                .overwrite_output()
                .run(quiet=True)
            )
            return output_path
        except ffmpeg.Error as e:
            raise Exception(f"FFmpeg error in Instagram preset: {e}")
    
    def _apply_youtube_preset(self, input_path, output_path):
        """YouTube: 16:9 letterbox + saturation boost"""
        try:
            (
                ffmpeg
                .input(input_path)
                .video
                .filter('pad', 'max(iw,ih*16/9)', 'max(iw*9/16,ih)', '(ow-iw)/2', '(oh-ih)/2', color='black')  # 16:9 letterbox
                .filter('eq', saturation=1.3)  # Saturation boost
                .output(output_path, acodec='aac', vcodec='libx264', crf=23)
                .overwrite_output()
                .run(quiet=True)
            )
            return output_path
        except ffmpeg.Error as e:
            raise Exception(f"FFmpeg error in YouTube preset: {e}")
    
    def apply_custom_commands(self, input_path, commands):
        """Apply custom commands to video"""
        output_path = os.path.join(self.temp_dir, f"custom_{Path(input_path).stem}.mp4")
        
        try:
            stream = ffmpeg.input(input_path).video
            
            for command in commands:
                stream = self._apply_video_command(stream, command)
            
            (
                stream
                .output(output_path, acodec='aac', vcodec='libx264', crf=23)
                .overwrite_output()
                .run(quiet=True)
            )
            return output_path
        except ffmpeg.Error as e:
            raise Exception(f"FFmpeg error in custom commands: {e}")
    
    def _apply_video_command(self, stream, command):
        """Apply individual video command"""
        cmd_type = command['type']
        params = command['params']
        
        if cmd_type == 'flip':
            if params.get('direction') == 'horizontal':
                return stream.filter('hflip')
            elif params.get('direction') == 'vertical':
                return stream.filter('vflip')
        
        elif cmd_type == 'speed':
            speed_factor = params.get('factor', 1.0)
            pts_value = 1.0 / speed_factor
            return stream.filter('setpts', f'{pts_value}*PTS')
        
        elif cmd_type == 'zoom':
            zoom_factor = params.get('factor', 1.0)
            return stream.filter('zoompan', zoom=zoom_factor, x='iw/2-(iw/zoom/2)', y='ih/2-(ih/zoom/2)', d=1)
        
        elif cmd_type == 'rotate':
            angle = params.get('angle', 0)
            return stream.filter('rotate', f'{angle}*PI/180')
        
        elif cmd_type == 'brightness':
            brightness = params.get('value', 0) / 100.0
            return stream.filter('eq', brightness=brightness)
        
        elif cmd_type == 'contrast':
            contrast = params.get('value', 100) / 100.0
            return stream.filter('eq', contrast=contrast)
        
        elif cmd_type == 'vintage':
            # Apply vintage effect with sepia and grain
            stream = stream.filter('colorchannelmixer', rr=0.393, rg=0.769, rb=0.189, gr=0.349, gg=0.686, gb=0.168, br=0.272, bg=0.534, bb=0.131)
            return stream.filter('noise', alls=15, allf='t')
        
        return stream
