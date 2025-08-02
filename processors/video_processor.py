import ffmpeg
import tempfile
import os
from pathlib import Path
import random
import time

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
        """TikTok: Research-based 2025 anti-algorithm system with audio frequency manipulation"""
        try:
            # Get dynamic variation for this processing session
            variation = self._get_dynamic_variation('tiktok')
            
            # Build complex FFmpeg filter chain based on research findings
            input_stream = ffmpeg.input(input_path)
            
            # Video processing with advanced evasion techniques
            video = input_stream.video
            
            # Skip horizontal flip to preserve text readability
            # Apply dynamic speed variation (research shows micro-variations fool detection)
            speed_factor = variation['speed_factor']
            video = video.filter('setpts', f'{speed_factor}*PTS')
            
            # Dynamic zoom with variation to prevent pattern detection
            zoom_factor = variation['zoom_factor']
            video = video.filter('zoompan', zoom=zoom_factor, x='iw/2-(iw/zoom/2)', y='ih/2-(ih/zoom/2)', d=1)
            
            # Adversarial color adjustments based on variation
            video = video.filter('eq', 
                brightness=variation['brightness'], 
                contrast=variation['contrast'], 
                saturation=variation['saturation'],
                gamma=variation['gamma'])
            
            # DCT domain inspired modifications through unsharp filter
            video = video.filter('unsharp', 
                luma_msize_x=variation['unsharp_size'], 
                luma_msize_y=variation['unsharp_size'], 
                luma_amount=variation['unsharp_amount'])
            
            # Dynamic noise patterns (FGS-Audio inspired for video)
            video = video.filter('noise', alls=variation['noise_level'], allf='t+u')
            
            # Micro-blur for pixel-level changes
            video = video.filter('boxblur', luma_radius=variation['blur_radius'], luma_power=1)
            
            # Color balance shifts (content-adaptive)
            video = video.filter('colorbalance', 
                rs=variation['color_balance']['r'], 
                gs=variation['color_balance']['g'], 
                bs=variation['color_balance']['b'])
            
            # Audio processing with frequency manipulation (Triple-Stage Audio inspired)
            audio = input_stream.audio
            
            # Stage 1: Pitch shift (imperceptible but changes audio fingerprint)
            audio = audio.filter('asetrate', variation['sample_rate_adjust'])
            audio = audio.filter('aresample', 44100)  # Return to standard rate
            
            # Stage 2: Audio frequency band manipulation
            audio = audio.filter('equalizer', f=variation['eq_frequency'], width_type='h', width=2, g=variation['eq_gain'])
            
            # Stage 3: Micro-volume adjustments for audio fingerprint evasion
            audio = audio.filter('volume', variation['volume_factor'])
            
            # Dynamic output settings to prevent encoding pattern detection
            output_settings = {
                'acodec': 'aac',
                'vcodec': 'libx264', 
                'crf': variation['crf'],
                'b:v': variation['bitrate'],
                'b:a': variation['audio_bitrate']
            }
            
            # Combine video and audio with dynamic settings
            (
                ffmpeg
                .output(video, audio, output_path, **output_settings)
                .overwrite_output()
                .run(quiet=True)
            )
            return output_path
        except ffmpeg.Error as e:
            raise Exception(f"FFmpeg error in TikTok advanced preset: {e}")
    
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
    
    def _get_dynamic_variation(self, platform):
        """Get dynamic variation for video processing to prevent pattern detection"""
        # Use current time and random seed for variation selection
        variation_seed = int(time.time()) % 7 + random.randint(1, 4)
        
        if platform == 'tiktok':
            return {
                'speed_factor': random.uniform(0.97, 1.03),  # Micro speed variations
                'zoom_factor': random.uniform(1.08, 1.18),   # Dynamic zoom
                'brightness': random.uniform(0.02, 0.08),    # Brightness shifts
                'contrast': random.uniform(1.05, 1.15),      # Contrast adjustments
                'saturation': random.uniform(1.15, 1.25),    # Saturation boost
                'gamma': random.uniform(0.98, 1.05),         # Gamma correction
                'unsharp_size': random.choice([3, 5, 7]),    # Sharpening variations
                'unsharp_amount': random.uniform(0.6, 0.9),  # Sharpening strength
                'noise_level': random.randint(20, 30),       # Noise intensity
                'blur_radius': random.uniform(0.8, 1.5),     # Blur amount
                'color_balance': {
                    'r': random.uniform(0.05, 0.12),         # Red balance
                    'g': random.uniform(-0.08, -0.02),       # Green balance  
                    'b': random.uniform(0.01, 0.05)          # Blue balance
                },
                # Audio frequency manipulation (research-based)
                'sample_rate_adjust': random.choice([44050, 44150, 44250]),  # Micro sample rate changes
                'eq_frequency': random.choice([440, 880, 1320, 2200]),       # EQ target frequencies
                'eq_gain': random.uniform(-0.5, 0.5),                        # EQ gain adjustments
                'volume_factor': random.uniform(0.98, 1.02),                 # Volume micro-adjustments
                'crf': random.randint(20, 24),                               # Dynamic quality
                'bitrate': random.choice(['1.8M', '2M', '2.2M']),           # Bitrate variation
                'audio_bitrate': random.choice(['128k', '160k', '192k'])     # Audio bitrate variation
            }
        elif platform == 'instagram':
            return {
                'speed_factor': random.uniform(0.98, 1.02),
                'brightness': random.uniform(0.05, 0.10),
                'contrast': random.uniform(1.10, 1.20),
                'saturation': random.uniform(1.25, 1.35),
                'gamma': random.uniform(1.02, 1.08),
                'unsharp_size': random.choice([3, 5]),
                'unsharp_amount': random.uniform(0.5, 0.7),
                'noise_level': random.randint(15, 22),
                'color_balance': {
                    'r': random.uniform(0.03, 0.08),
                    'g': random.uniform(-0.05, -0.01),
                    'b': random.uniform(0.01, 0.04)
                },
                'sample_rate_adjust': random.choice([44080, 44120, 44180]),
                'eq_frequency': random.choice([660, 1100, 1760]),
                'eq_gain': random.uniform(-0.3, 0.3),
                'volume_factor': random.uniform(0.99, 1.01),
                'crf': random.randint(21, 25),
                'bitrate': random.choice(['2M', '2.5M', '3M']),
                'audio_bitrate': random.choice(['160k', '192k', '224k'])
            }
        else:  # youtube
            return {
                'speed_factor': random.uniform(0.995, 1.005),
                'zoom_factor': random.uniform(1.02, 1.08),
                'brightness': random.uniform(0.01, 0.05),
                'contrast': random.uniform(1.02, 1.10),
                'saturation': random.uniform(1.05, 1.15),
                'gamma': random.uniform(0.99, 1.03),
                'unsharp_size': random.choice([3, 5]),
                'unsharp_amount': random.uniform(0.4, 0.6),
                'noise_level': random.randint(8, 18),
                'color_balance': {
                    'r': random.uniform(0.01, 0.05),
                    'g': random.uniform(-0.03, 0.01),
                    'b': random.uniform(0.01, 0.03)
                },
                'sample_rate_adjust': random.choice([44090, 44110, 44130]),
                'eq_frequency': random.choice([800, 1200, 1600, 2400]),
                'eq_gain': random.uniform(-0.2, 0.2),
                'volume_factor': random.uniform(0.995, 1.005),
                'crf': random.randint(18, 22),
                'bitrate': random.choice(['3M', '4M', '5M']),
                'audio_bitrate': random.choice(['192k', '256k', '320k'])
            }
    
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
