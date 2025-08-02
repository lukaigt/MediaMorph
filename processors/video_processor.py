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
        """TikTok: Advanced algorithm evasion with multiple transformations"""
        try:
            (
                ffmpeg
                .input(input_path)
                .video
                .filter('hflip')  # Horizontal flip
                .filter('setpts', '0.85*PTS')  # Speed up by 15%
                .filter('zoompan', zoom='1.15', x='iw/2-(iw/zoom/2)', y='ih/2-(ih/zoom/2)', d=1)  # Stronger zoom
                .filter('eq', brightness=0.05, contrast=1.1, saturation=1.2)  # Color adjustments
                .filter('unsharp', luma_msize_x=5, luma_msize_y=5, luma_amount=0.8)  # Sharpening
                .filter('noise', alls=25, allf='t+u')  # Strong noise
                .filter('boxblur', luma_radius=1, luma_power=1)  # Subtle blur to change pixels
                .filter('colorbalance', rs=0.1, gs=-0.05, bs=0.02)  # Color balance shift
                .output(output_path, acodec='aac', vcodec='libx264', crf=22, **{'b:v': '2M'})
                .overwrite_output()
                .run(quiet=True)
            )
            return output_path
        except ffmpeg.Error as e:
            raise Exception(f"FFmpeg error in TikTok preset: {e}")
    
    def _apply_instagram_preset(self, input_path, output_path):
        """Instagram: Advanced square processing with heavy modifications"""
        try:
            (
                ffmpeg
                .input(input_path)
                .video
                .filter('crop', 'min(iw,ih)', 'min(iw,ih)')  # Square crop
                .filter('eq', saturation=1.3, brightness=0.08, contrast=1.15, gamma=1.05)  # Enhanced color adjustments
                .filter('hue', h=2)  # Slight hue shift
                .filter('unsharp', luma_msize_x=3, luma_msize_y=3, luma_amount=0.6)  # Sharpening
                .filter('noise', alls=18, allf='t+u')  # Film grain + temporal noise
                .filter('colorbalance', rm=0.05, gm=-0.03, bm=0.02)  # Color balance
                .filter('eq', saturation=1.4)  # Enhanced saturation instead of vibrance
                .filter('scale', 'iw*0.999', 'ih*0.999')  # Tiny scale change
                .output(output_path, acodec='aac', vcodec='libx264', crf=22, **{'b:v': '2.5M'})
                .overwrite_output()
                .run(quiet=True)
            )
            return output_path
        except ffmpeg.Error as e:
            raise Exception(f"FFmpeg error in Instagram preset: {e}")
    
    def _apply_youtube_preset(self, input_path, output_path):
        """YouTube: Advanced landscape processing with heavy algorithm evasion"""
        try:
            (
                ffmpeg
                .input(input_path)
                .video
                .filter('pad', 'max(iw,ih*16/9)', 'max(iw*9/16,ih)', '(ow-iw)/2', '(oh-ih)/2', color='#010101')  # 16:9 letterbox with near-black
                .filter('eq', saturation=1.4, brightness=0.03, contrast=1.12, gamma=0.98)  # Enhanced adjustments
                .filter('hue', h=-1, s=0.05)  # Hue and saturation shift
                .filter('unsharp', luma_msize_x=7, luma_msize_y=7, luma_amount=0.7)  # Strong sharpening
                .filter('noise', alls=15, allf='t+u')  # Noise for algorithm confusion
                .filter('colorbalance', rs=-0.02, gs=0.03, bs=-0.01)  # Color balance
                .filter('eq', gamma=0.95)  # Gamma adjustment instead of curves
                .filter('scale', 'iw*1.001', 'ih*1.001')  # Minimal scale to change hash
                .output(output_path, acodec='aac', vcodec='libx264', crf=21, **{'b:v': '3M'})
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
