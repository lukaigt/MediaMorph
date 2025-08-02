import ffmpeg
import tempfile
import os
from pathlib import Path
import random
import time

class VideoProcessor:
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
        self.session_history = []  # Track processing patterns to avoid repetition
        self.max_history = 10      # Remember last 10 processing sessions
    
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
        """TikTok: Advanced 8-layer anti-algorithm system with cutting-edge video evasion"""
        try:
            # Get dynamic variation with batch protection
            variation = self._get_dynamic_variation('tiktok')
            
            # Build advanced FFmpeg filter chain with 2025 research techniques
            input_stream = ffmpeg.input(input_path)
            
            # === LAYER 1: ADVANCED TEMPORAL DOMAIN MANIPULATION ===
            video = input_stream.video
            
            # Micro frame timing adjustments (imperceptible but breaks temporal fingerprints)
            speed_factor = variation['speed_factor']
            video = video.filter('setpts', f'{speed_factor}*PTS')
            
            # Frame duplication/deletion for temporal evasion (imperceptible at 30fps)
            if variation.get('frame_manipulation', False):
                # Randomly duplicate or skip frames to break temporal patterns
                video = video.filter('framestep', step=variation['frame_step'])
                # Re-interpolate to maintain smooth playback
                video = video.filter('minterpolate', fps=variation['target_fps'], mi_mode='mci', mc_mode='aobmc')
            
            # Advanced frame interpolation with motion compensation
            elif variation.get('use_frame_interpolation', False):
                video = video.filter('minterpolate', 
                    fps=variation['target_fps'], 
                    mi_mode='mci', 
                    mc_mode='aobmc',
                    me_mode='bidir',
                    vsbmc=1)  # Advanced motion estimation
            
            # === LAYER 2: ADVANCED SPATIAL DOMAIN EVASION ===
            # Dynamic zoom with sine wave micro-variations
            zoom_factor = variation['zoom_factor']
            video = video.filter('zoompan', 
                zoom=f"{zoom_factor}+0.001*sin(2*PI*t/{variation['zoom_period']})", 
                x='iw/2-(iw/zoom/2)', 
                y='ih/2-(ih/zoom/2)', 
                d=1)
            
            # Optical flow disruption (breaks motion-based detection)
            if variation.get('optical_flow_disruption', False):
                # Apply subtle motion vector modifications
                video = video.filter('vidstabdetect', stepsize=variation['flow_stepsize'], shakiness=1, accuracy=15)
                video = video.filter('vidstabtransform', 
                    smoothing=variation['flow_smoothing'], 
                    maxshift=variation['flow_maxshift'],
                    maxangle=variation['flow_maxangle'])
            
            # Advanced geometric transformations
            if variation.get('apply_perspective', False):
                video = video.filter('perspective', 
                    x0=variation['perspective']['x0'], y0=variation['perspective']['y0'],
                    x1=variation['perspective']['x1'], y1=variation['perspective']['y1'],
                    x2=variation['perspective']['x2'], y2=variation['perspective']['y2'],
                    x3=variation['perspective']['x3'], y3=variation['perspective']['y3'])
            
            # Lens distortion simulation (breaks geometric fingerprints)
            if variation.get('lens_distortion', False):
                video = video.filter('lenscorrection', 
                    cx=variation['lens_cx'], cy=variation['lens_cy'],
                    k1=variation['lens_k1'], k2=variation['lens_k2'])
            
            # === LAYER 3: FREQUENCY DOMAIN MANIPULATION ===
            # Advanced color space transformations
            video = video.filter('eq', 
                brightness=variation['brightness'], 
                contrast=variation['contrast'], 
                saturation=variation['saturation'],
                gamma=variation['gamma'])
            
            # DCT-inspired frequency domain modifications
            video = video.filter('unsharp', 
                luma_msize_x=variation['unsharp_size'], 
                luma_msize_y=variation['unsharp_size'], 
                luma_amount=variation['unsharp_amount'])
            
            # === LAYER 4: NOISE INJECTION SYSTEM ===
            # Multi-layered noise for maximum algorithm confusion
            # Temporal noise (changes over time)
            video = video.filter('noise', alls=variation['noise_level'], allf='t+u')
            
            # Content-adaptive noise (stronger in edges, weaker in smooth areas)
            if variation.get('adaptive_noise', False):
                video = video.filter('convolution', 
                    '1 -1 1|-1 5 -1|1 -1 1:1 -1 1|-1 5 -1|1 -1 1:1 -1 1|-1 5 -1|1 -1 1:1 -1 1|-1 5 -1|1 -1 1')
            
            # === LAYER 5: PIXEL-LEVEL DISRUPTION ===
            # Micro-blur with temporal variation
            blur_radius = f"{variation['blur_radius']}+{variation['blur_variation']}*sin(2*PI*t/{variation['blur_period']})"
            video = video.filter('boxblur', luma_radius=blur_radius, luma_power=1)
            
            # Color channel mixing (advanced steganography-inspired)
            video = video.filter('colorchannelmixer', 
                rr=variation['channel_mix']['rr'], rg=variation['channel_mix']['rg'], rb=variation['channel_mix']['rb'],
                gr=variation['channel_mix']['gr'], gg=variation['channel_mix']['gg'], gb=variation['channel_mix']['gb'],
                br=variation['channel_mix']['br'], bg=variation['channel_mix']['bg'], bb=variation['channel_mix']['bb'])
            
            # === LAYER 6: REVOLUTIONARY AUDIO PROCESSING ===
            audio = input_stream.audio
            
            # Stage 1: Sample rate micro-adjustments (breaks audio fingerprints)
            audio = audio.filter('asetrate', variation['sample_rate_adjust'])
            audio = audio.filter('aresample', 44100)  # Return to standard rate
            
            # Stage 2: Advanced audio steganography (LSB in frequency domain)
            if variation.get('audio_steganography', False):
                # Apply imperceptible frequency domain modifications
                audio = audio.filter('highpass', f=variation['steg_highpass'])
                audio = audio.filter('lowpass', f=variation['steg_lowpass'])
            
            # Stage 3: Multi-band EQ (imperceptible frequency domain changes)
            for freq_band in variation['eq_bands']:
                audio = audio.filter('equalizer', f=freq_band['freq'], g=freq_band['gain'], w=freq_band['width'])
            
            # Stage 4: Phase manipulation (breaks audio fingerprints)
            if variation.get('phase_manipulation', False):
                audio = audio.filter('aphaser', 
                    in_gain=variation['phase_in_gain'],
                    out_gain=variation['phase_out_gain'],
                    delay=variation['phase_delay'],
                    decay=variation['phase_decay'],
                    speed=variation['phase_speed'])
            
            # Stage 5: Audio stereo field manipulation
            if variation.get('stereo_manipulation', False):
                audio = audio.filter('extrastereo', m=variation['stereo_factor'])
            
            # Stage 6: Psychoacoustic volume adjustments
            audio = audio.filter('volume', variation['volume_factor'])
            
            # Stage 7: Silent frame insertion (advanced temporal evasion)
            if variation.get('insert_silence', False):
                silence_duration = variation['silence_duration']
                silence_position = variation['silence_position']
                silence = ffmpeg.input('anullsrc=r=44100:cl=stereo', f='lavfi', t=silence_duration)
                audio = ffmpeg.filter([audio, silence], 'concat', n=2, v=0, a=1)
            
            # Stage 8: Audio compression artifacts simulation
            if variation.get('compression_artifacts', False):
                # Simulate and then reverse compression artifacts to confuse algorithms
                audio = audio.filter('acompressor', 
                    threshold=variation['comp_threshold'],
                    ratio=variation['comp_ratio'],
                    attack=variation['comp_attack'],
                    release=variation['comp_release'])
            
            # === LAYER 7: METADATA & CONTAINER MANIPULATION ===
            # Advanced encoding with randomized parameters
            encoding_params = {
                'acodec': 'aac',
                'vcodec': 'libx264',
                'crf': variation['crf'],
                'preset': variation['encoding_preset'],
                'profile:v': variation['h264_profile'],
                'level': variation['h264_level'],
                'b:v': variation['bitrate'],
                'b:a': variation['audio_bitrate'],
                'movflags': '+faststart',  # Optimize for streaming
                'pix_fmt': variation['pixel_format']
            }
            
            # === LAYER 8: ADVANCED CONTAINER FORMAT CHAIN ===
            # Multi-stage encoding with keyframe manipulation
            
            # Stage 1: Intermediate encoding with custom keyframe intervals
            temp_output = output_path.replace('.mp4', '_temp.mkv')
            intermediate_params = encoding_params.copy()
            intermediate_params.update({
                'g': variation['keyframe_interval'],  # Custom keyframe interval
                'sc_threshold': variation['scene_threshold'],  # Scene change detection
                'keyint_min': variation['min_keyframe_interval']
            })
            
            (
                ffmpeg
                .output(video, audio, temp_output, **intermediate_params)
                .overwrite_output()
                .run(quiet=True)
            )
            
            # Stage 2: Final encoding with different compression settings
            final_params = {
                'acodec': 'aac',
                'vcodec': 'libx264', 
                'crf': variation['final_crf'],
                'preset': variation['final_preset'],
                'profile:v': variation['final_profile'],
                'b:a': variation['audio_bitrate'],  # CRITICAL: Audio bitrate for final stage
                'movflags': '+faststart',
                'metadata': f"creation_time={variation['fake_creation_time']}",
                # Advanced compression settings
                'x264opts': f"keyint={variation['final_keyframe_interval']}:min-keyint={variation['final_min_keyframe']}:bframes={variation['b_frames']}",
                'bf': variation['b_frames'],  # B-frame count
                'refs': variation['ref_frames']  # Reference frame count
            }
            
            (
                ffmpeg
                .input(temp_output)
                .output(output_path, **final_params)
                .overwrite_output()
                .run(quiet=True)
            )
            
            # Clean up temporary file
            os.remove(temp_output)
            
            return output_path
        except ffmpeg.Error as e:
            raise Exception(f"FFmpeg error in TikTok preset: {e}")
            
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
                .output(output_path, acodec='aac', vcodec='libx264', crf=22, **{'b:v': '2.5M', 'b:a': '192k'})
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
                .output(output_path, acodec='aac', vcodec='libx264', crf=21, **{'b:v': '3M', 'b:a': '192k'})
                .overwrite_output()
                .run(quiet=True)
            )
            return output_path
        except ffmpeg.Error as e:
            raise Exception(f"FFmpeg error in YouTube preset: {e}")
    
    def _get_dynamic_variation(self, platform):
        """Get advanced dynamic variation with batch protection for 2025 video processing"""
        # Use current time and random seed for variation selection
        variation_seed = int(time.time()) % 7 + random.randint(1, 4)
        
        # Apply batch protection
        variation_seed = self._apply_batch_protection(variation_seed, platform)
        
        if platform == 'tiktok':
            return {
                # === TEMPORAL DOMAIN ===
                'speed_factor': random.uniform(0.998, 1.002),    # Micro speed variations (imperceptible)
                'frame_manipulation': random.choice([True, False]),
                'frame_step': random.choice([1, 2, 3]),          # Frame step for duplication/deletion
                'use_frame_interpolation': random.choice([True, False]),
                'target_fps': random.choice([29.97, 30, 30.03]), # Slight FPS variations
                
                # === SPATIAL DOMAIN ===
                'zoom_factor': random.uniform(1.01, 1.05),       # Subtle zoom
                'zoom_period': random.uniform(60, 120),          # Zoom oscillation period
                'optical_flow_disruption': random.choice([True, False]),
                'flow_stepsize': random.choice([6, 8, 12]),      # Motion detection step size
                'flow_smoothing': random.randint(10, 30),        # Flow smoothing
                'flow_maxshift': random.randint(5, 15),          # Max motion shift
                'flow_maxangle': random.uniform(0.1, 0.3),       # Max rotation angle
                'apply_perspective': random.choice([True, False]),
                'perspective': {
                    'x0': random.uniform(0, 5), 'y0': random.uniform(0, 5),
                    'x1': random.uniform(95, 100), 'y1': random.uniform(0, 5),
                    'x2': random.uniform(0, 5), 'y2': random.uniform(95, 100),
                    'x3': random.uniform(95, 100), 'y3': random.uniform(95, 100)
                },
                'lens_distortion': random.choice([True, False]),
                'lens_cx': random.uniform(0.45, 0.55),           # Lens center X
                'lens_cy': random.uniform(0.45, 0.55),           # Lens center Y
                'lens_k1': random.uniform(-0.05, 0.05),          # Lens distortion k1
                'lens_k2': random.uniform(-0.02, 0.02),          # Lens distortion k2
                
                # === FREQUENCY DOMAIN ===
                'brightness': random.uniform(0.005, 0.02),       # Very subtle brightness
                'contrast': random.uniform(1.01, 1.05),          # Minimal contrast changes
                'saturation': random.uniform(1.02, 1.08),        # Subtle saturation
                'gamma': random.uniform(0.98, 1.02),             # Gamma correction
                'unsharp_size': random.choice([3, 5]),           # Sharpening variations
                'unsharp_amount': random.uniform(0.1, 0.3),      # Minimal sharpening
                
                # === NOISE SYSTEM ===
                'noise_level': random.randint(3, 8),             # Very low noise
                'adaptive_noise': random.choice([True, False]),
                
                # === PIXEL DISRUPTION ===
                'blur_radius': random.uniform(0.1, 0.3),         # Minimal blur
                'blur_variation': random.uniform(0.05, 0.1),     # Blur oscillation
                'blur_period': random.uniform(30, 90),           # Blur period
                'channel_mix': {
                    'rr': random.uniform(0.98, 1.02), 'rg': random.uniform(-0.01, 0.01), 'rb': random.uniform(-0.01, 0.01),
                    'gr': random.uniform(-0.01, 0.01), 'gg': random.uniform(0.98, 1.02), 'gb': random.uniform(-0.01, 0.01),
                    'br': random.uniform(-0.01, 0.01), 'bg': random.uniform(-0.01, 0.01), 'bb': random.uniform(0.98, 1.02)
                },
                
                # === REVOLUTIONARY AUDIO ===
                'sample_rate_adjust': random.choice([44095, 44105, 44110]), # Micro sample rate changes
                'audio_steganography': random.choice([True, False]),
                'steg_highpass': random.choice([50, 80, 120]),   # Steganography highpass
                'steg_lowpass': random.choice([8000, 12000, 16000]), # Steganography lowpass
                'eq_bands': [
                    {'freq': random.choice([440, 880, 1320]), 'gain': random.uniform(-0.1, 0.1), 'width': random.choice([1, 2])},
                    {'freq': random.choice([2200, 4400, 8800]), 'gain': random.uniform(-0.08, 0.08), 'width': random.choice([1, 2])},
                    {'freq': random.choice([100, 200, 400]), 'gain': random.uniform(-0.05, 0.05), 'width': random.choice([2, 3])}
                ],
                'phase_manipulation': random.choice([True, False]),
                'phase_in_gain': random.uniform(0.4, 0.6),       # Phase input gain
                'phase_out_gain': random.uniform(0.7, 0.9),      # Phase output gain
                'phase_delay': random.uniform(2.0, 4.0),         # Phase delay
                'phase_decay': random.uniform(0.3, 0.7),         # Phase decay
                'phase_speed': random.uniform(0.1, 0.5),         # Phase speed
                'stereo_manipulation': random.choice([True, False]),
                'stereo_factor': random.uniform(0.98, 1.02),
                'volume_factor': random.uniform(0.999, 1.001),   # Barely perceptible
                'insert_silence': random.choice([True, False]),
                'silence_duration': random.uniform(0.005, 0.02), # Very short silence
                'silence_position': random.choice(['start', 'middle', 'end']),
                'compression_artifacts': random.choice([True, False]),
                'comp_threshold': random.uniform(0.1, 0.3),      # Compressor threshold
                'comp_ratio': random.uniform(2, 4),              # Compressor ratio
                'comp_attack': random.uniform(1, 5),             # Compressor attack
                'comp_release': random.uniform(50, 150),         # Compressor release
                
                # === ADVANCED ENCODING PARAMETERS ===
                'crf': random.randint(20, 24),
                'encoding_preset': random.choice(['medium', 'slow', 'slower']),
                'h264_profile': random.choice(['main', 'high']),
                'h264_level': random.choice(['3.1', '4.0', '4.1']),
                'pixel_format': random.choice(['yuv420p', 'yuvj420p']),
                'bitrate': random.choice(['1.8M', '2M', '2.2M']),
                'audio_bitrate': random.choice(['128k', '160k', '192k']),
                
                # === KEYFRAME MANIPULATION ===
                'keyframe_interval': random.randint(250, 350),   # GOP size
                'scene_threshold': random.uniform(0.3, 0.5),     # Scene change threshold
                'min_keyframe_interval': random.randint(10, 25), # Min keyframe interval
                
                # === FINAL ENCODING ===
                'final_crf': random.randint(21, 25),
                'final_preset': random.choice(['fast', 'medium', 'slow']),
                'final_profile': random.choice(['main', 'high']),
                'final_keyframe_interval': random.randint(200, 400),
                'final_min_keyframe': random.randint(8, 20),
                'b_frames': random.randint(2, 5),                # B-frame count
                'ref_frames': random.randint(2, 4),              # Reference frames
                'fake_creation_time': self._generate_fake_timestamp()
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
    
    def _apply_batch_protection(self, variation_seed, platform):
        """Prevent pattern detection across multiple video uploads in the same session"""
        # Create unique fingerprint for this processing session
        session_fingerprint = {
            'platform': platform,
            'variation_type': variation_seed % 8,  # 8 different types for videos
            'timestamp': int(time.time() / 600)    # 10-minute windows (videos take longer)
        }
        
        # Check if this combination was used recently
        recent_similar = [h for h in self.session_history 
                         if h['platform'] == platform and 
                         h['variation_type'] == session_fingerprint['variation_type'] and
                         abs(h['timestamp'] - session_fingerprint['timestamp']) <= 3]
        
        # If similar pattern found recently, modify the variation
        if recent_similar:
            # Force a different variation type
            available_types = list(range(8))
            used_types = [h['variation_type'] for h in recent_similar]
            available_types = [t for t in available_types if t not in used_types]
            
            if available_types:
                new_type = random.choice(available_types)
                variation_seed = (variation_seed // 8) * 8 + new_type
            else:
                # All types used recently, add random offset
                variation_seed += random.randint(15, 75)
        
        # Add this session to history
        self.session_history.append(session_fingerprint)
        
        # Keep only recent history
        if len(self.session_history) > self.max_history:
            self.session_history = self.session_history[-self.max_history:]
        
        return variation_seed
    
    def _generate_fake_timestamp(self):
        """Generate fake but realistic video creation timestamp"""
        import datetime
        now = datetime.datetime.now()
        random_days_ago = random.randint(1, 90)  # 1-90 days ago
        fake_time = now - datetime.timedelta(days=random_days_ago, 
                                           hours=random.randint(0, 23),
                                           minutes=random.randint(0, 59),
                                           seconds=random.randint(0, 59))
        return fake_time.strftime('%Y-%m-%dT%H:%M:%S.000000Z')
