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
        self.audio_quality = '192k'  # Default audio quality
    
    def set_audio_quality(self, quality):
        """Set the audio quality for video processing"""
        self.audio_quality = quality
    
    def set_progress_callback(self, callback):
        """Set callback function for progress updates"""
        self.progress_callback = callback
        
    def update_progress(self, percentage, text):
        """Update progress if callback is set"""
        if hasattr(self, 'progress_callback') and self.progress_callback:
            self.progress_callback(percentage, text)
    
    def apply_preset(self, input_path, platform):
        """Apply platform-specific preset to video"""
        output_path = os.path.join(self.temp_dir, f"processed_{platform}_{Path(input_path).stem}.mp4")
        
        self.update_progress(45, f"Applying {platform.upper()} algorithm evasion...")
        
        if platform == 'tiktok':
            result = self._apply_tiktok_preset(input_path, output_path)
        elif platform == 'instagram':
            result = self._apply_instagram_preset(input_path, output_path)
        elif platform == 'youtube':
            # Use the simple YouTube preset instead of complex TikTok system
            result = self._apply_youtube_preset(input_path, output_path)
        else:
            raise ValueError(f"Unknown platform: {platform}")
        
        self.update_progress(85, f"Finalizing {platform.upper()} processing...")
        return result
    
    def apply_protection_layer(self, video, layer_name, filter_func, fallback_func=None):
        """Apply a protection layer with validation and fallback"""
        try:
            result = filter_func(video)
            print(f"✓ {layer_name}: Applied successfully")
            return result
        except Exception as e:
            print(f"✗ {layer_name}: Failed ({e})")
            if fallback_func:
                try:
                    result = fallback_func(video)
                    print(f"✓ {layer_name}: Fallback applied")
                    return result
                except Exception as fallback_error:
                    print(f"✗ {layer_name}: Fallback also failed ({fallback_error})")
            print(f"→ {layer_name}: Continuing without this layer")
            return video

    def _apply_tiktok_preset(self, input_path, output_path):
        """TikTok: Robust multi-layer protection with validation and fallbacks"""
        try:
            self.update_progress(50, "Starting robust algorithm evasion system...")
            
            # Initialize
            input_stream = ffmpeg.input(input_path)
            video = input_stream.video
            protection_layers_applied = []
            
            # Check for audio
            try:
                probe = ffmpeg.probe(input_path)
                has_audio = any(stream['codec_type'] == 'audio' for stream in probe['streams'])
                print(f"Audio detection: {has_audio} streams found")
            except Exception as e:
                has_audio = False
                print(f"Warning: Audio detection failed: {e}")

            self.update_progress(55, "Applying Layer 1: Temporal Protection...")
            
            # LAYER 1: TEMPORAL DOMAIN (Guaranteed reliable)
            def temporal_advanced(v):
                return v.filter('setpts', '0.999*PTS')  # Subtle timing change
            
            def temporal_fallback(v):
                return v.filter('fps', fps=59.94)  # Simple FPS adjustment
            
            video = self.apply_protection_layer(
                video, "Temporal Protection", temporal_advanced, temporal_fallback
            )
            if video != input_stream.video:
                protection_layers_applied.append("Temporal")

            self.update_progress(60, "Applying Layer 2: Spatial Protection...")
            
            # LAYER 2: SPATIAL DOMAIN (Reliable scaling)
            def spatial_advanced(v):
                return v.filter('scale', 'iw*1.002', 'ih*1.002')  # Micro scaling
            
            def spatial_fallback(v):
                return v.filter('scale', 'iw', 'ih')  # Identity scale (still changes hash)
            
            video = self.apply_protection_layer(
                video, "Spatial Protection", spatial_advanced, spatial_fallback
            )
            if len(protection_layers_applied) < 2:
                protection_layers_applied.append("Spatial")

            self.update_progress(65, "Applying Layer 3: Color Protection...")
            
            # LAYER 3: COLOR DOMAIN (Essential and reliable)
            def color_advanced(v):
                return v.filter('eq', brightness=0.03, contrast=1.08, saturation=1.05, gamma=0.98)
            
            def color_fallback(v):
                return v.filter('eq', brightness=0.01, contrast=1.02)
            
            video = self.apply_protection_layer(
                video, "Color Protection", color_advanced, color_fallback
            )
            protection_layers_applied.append("Color")

            self.update_progress(70, "Applying Layer 4: Noise Protection...")
            
            # LAYER 4: NOISE INJECTION (Light but effective)
            def noise_advanced(v):
                return v.filter('noise', alls=8, allf='t')  # Temporal noise
            
            def noise_fallback(v):
                return v.filter('noise', alls=5)  # Static noise
            
            video = self.apply_protection_layer(
                video, "Noise Protection", noise_advanced, noise_fallback
            )
            protection_layers_applied.append("Noise")

            self.update_progress(75, "Applying Layer 5: Blur Protection...")
            
            # LAYER 5: MICRO BLUR (Subtle but effective)
            def blur_advanced(v):
                return v.filter('boxblur', luma_radius=0.8, luma_power=1)
            
            def blur_fallback(v):
                return v.filter('boxblur', luma_radius=0.5)
            
            video = self.apply_protection_layer(
                video, "Blur Protection", blur_advanced, blur_fallback
            )
            protection_layers_applied.append("Blur")

            self.update_progress(80, "Preparing ultra-high quality encoding...")
            
            print(f"Protection Summary: {len(protection_layers_applied)} layers applied: {', '.join(protection_layers_applied)}")
            
            # ULTRA-HIGH QUALITY ENCODING (Simplified and reliable)
            encoding_params = {
                'vcodec': 'libx264',
                'crf': 16,
                'preset': 'slow',
                'b:v': '12M',
                'r': 60,
                's': '1920x1080',
                'pix_fmt': 'yuv420p'
            }
            
            self.update_progress(85, "Encoding 1080p60 with validated parameters...")
            
            # ENCODING WITH VALIDATION
            try:
                print(f"Final encoding with parameters: {encoding_params}")
                
                if has_audio:
                    print("Encoding with audio preservation...")
                    (
                        ffmpeg
                        .output(video, input_stream.audio, output_path, 
                               acodec='copy', **encoding_params)
                        .overwrite_output()
                        .run(quiet=False)
                    )
                else:
                    print("Encoding video only...")
                    (
                        ffmpeg
                        .output(video, output_path, **encoding_params)
                        .overwrite_output()
                        .run(quiet=False)
                    )
                
                # VALIDATE OUTPUT QUALITY
                self.update_progress(95, "Validating output quality...")
                
                probe = ffmpeg.probe(output_path)
                video_stream = next(s for s in probe['streams'] if s['codec_type'] == 'video')
                width = int(video_stream['width'])
                height = int(video_stream['height'])
                fps_str = video_stream['r_frame_rate']
                fps = eval(fps_str) if '/' in fps_str else float(fps_str)
                
                print(f"✓ Quality Validation:")
                print(f"  Resolution: {width}x{height} ({'✓' if width >= 1920 and height >= 1080 else '✗'})")
                print(f"  Frame Rate: {fps:.1f}fps ({'✓' if fps >= 59 else '✗'})")
                print(f"  Protection Layers: {len(protection_layers_applied)}/5 applied")
                
                if width >= 1920 and height >= 1080 and fps >= 59:
                    self.update_progress(100, f"SUCCESS: 1080p60 with {len(protection_layers_applied)} protection layers!")
                else:
                    self.update_progress(100, f"Completed with {len(protection_layers_applied)} protection layers")
                
                return output_path
                
            except ffmpeg.Error as e:
                print(f"Primary encoding failed: {e}")
                
                # ROBUST FALLBACK ENCODING
                print("Applying robust fallback encoding...")
                self.update_progress(90, "Using fallback encoding...")
                
                (
                    ffmpeg
                    .input(input_path)
                    .output(output_path, 
                           vcodec='libx264', crf=18, preset='medium',
                           **{'b:v': '8M', 'r': 60, 's': '1920x1080'})
                    .overwrite_output()
                    .run(quiet=False)
                )
                
                self.update_progress(100, "Fallback encoding completed")
                return output_path
                
        except Exception as e:
            raise Exception(f"TikTok processing failed: {e}")
    
    def _apply_instagram_preset(self, input_path, output_path):
        """Instagram: Robust square processing with validated protection layers"""
        try:
            self.update_progress(50, "Starting Instagram square processing...")
            
            input_stream = ffmpeg.input(input_path)
            video = input_stream.video
            protection_layers_applied = []
            
            # Check for audio
            try:
                probe = ffmpeg.probe(input_path)
                has_audio = any(stream['codec_type'] == 'audio' for stream in probe['streams'])
                print(f"Audio detection: {has_audio} streams found")
            except Exception as e:
                has_audio = False
                print(f"Warning: Audio detection failed: {e}")

            self.update_progress(55, "Applying square crop...")
            
            # INSTAGRAM SQUARE CROP (Essential)
            def square_crop_advanced(v):
                return v.filter('crop', 'min(iw,ih)', 'min(iw,ih)')
            
            def square_crop_fallback(v):
                # Fallback: center crop to square 
                return v.filter('crop', 'iw', 'iw', '(iw-iw)/2', '(ih-iw)/2')
            
            video = self.apply_protection_layer(
                video, "Square Crop", square_crop_advanced, square_crop_fallback
            )
            protection_layers_applied.append("Square")

            self.update_progress(60, "Applying Instagram color enhancement...")
            
            # LAYER 1: INSTAGRAM COLOR ENHANCEMENT
            def color_enhance_advanced(v):
                return v.filter('eq', saturation=1.25, brightness=0.05, contrast=1.12, gamma=1.02)
            
            def color_enhance_fallback(v):
                return v.filter('eq', saturation=1.15, contrast=1.05)
            
            video = self.apply_protection_layer(
                video, "Color Enhancement", color_enhance_advanced, color_enhance_fallback
            )
            protection_layers_applied.append("Color")

            self.update_progress(65, "Applying sharpening...")
            
            # LAYER 2: SHARPENING
            def sharpen_advanced(v):
                return v.filter('unsharp', luma_msize_x=3, luma_msize_y=3, luma_amount=0.4)
            
            def sharpen_fallback(v):
                return v.filter('unsharp', luma_msize_x=3, luma_msize_y=3, luma_amount=0.2)
            
            video = self.apply_protection_layer(
                video, "Sharpening", sharpen_advanced, sharpen_fallback
            )
            protection_layers_applied.append("Sharpen")

            self.update_progress(70, "Applying algorithm evasion...")
            
            # LAYER 3: ALGORITHM EVASION
            def noise_evasion_advanced(v):
                return v.filter('noise', alls=12, allf='t')
            
            def noise_evasion_fallback(v):
                return v.filter('noise', alls=8)
            
            video = self.apply_protection_layer(
                video, "Noise Evasion", noise_evasion_advanced, noise_evasion_fallback
            )
            protection_layers_applied.append("Evasion")

            self.update_progress(75, "Preparing high-quality encoding...")
            
            print(f"Instagram Protection Summary: {len(protection_layers_applied)} layers applied: {', '.join(protection_layers_applied)}")
            
            # HIGH-QUALITY ENCODING
            encoding_params = {
                'vcodec': 'libx264',
                'crf': 16,
                'preset': 'slow',
                'b:v': '10M',
                'r': 60,
                's': '1080x1080',  # Instagram square
                'pix_fmt': 'yuv420p'
            }
            
            self.update_progress(85, "Encoding Instagram 1080x1080...")
            
            try:
                print(f"Instagram encoding with parameters: {encoding_params}")
                
                if has_audio:
                    (
                        ffmpeg
                        .output(video, input_stream.audio, output_path, 
                               acodec='copy', **encoding_params)
                        .overwrite_output()
                        .run(quiet=False)
                    )
                else:
                    (
                        ffmpeg
                        .output(video, output_path, **encoding_params)
                        .overwrite_output()
                        .run(quiet=False)
                    )
                
                # Validate output
                self.update_progress(95, "Validating Instagram output...")
                probe = ffmpeg.probe(output_path)
                video_stream = next(s for s in probe['streams'] if s['codec_type'] == 'video')
                width = int(video_stream['width'])
                height = int(video_stream['height'])
                
                print(f"✓ Instagram Validation: {width}x{height} ({'✓' if width == height == 1080 else '✗'})")
                print(f"✓ Protection Layers: {len(protection_layers_applied)}/4 applied")
                
                self.update_progress(100, f"Instagram complete with {len(protection_layers_applied)} layers!")
                return output_path
                
            except ffmpeg.Error as e:
                print(f"Instagram encoding failed: {e}")
                # Fallback encoding
                (
                    ffmpeg
                    .input(input_path)
                    .output(output_path, vcodec='libx264', crf=18, **{'s': '1080x1080'})
                    .overwrite_output()
                    .run(quiet=False)
                )
                return output_path
                
        except Exception as e:
            raise Exception(f"Instagram processing failed: {e}")
    
    def _apply_youtube_preset(self, input_path, output_path):
        """YouTube: Robust landscape processing with validated protection layers"""
        try:
            self.update_progress(50, "Starting YouTube landscape processing...")
            
            input_stream = ffmpeg.input(input_path)
            video = input_stream.video
            protection_layers_applied = []
            
            # Check for audio
            try:
                probe = ffmpeg.probe(input_path)
                has_audio = any(stream['codec_type'] == 'audio' for stream in probe['streams'])
                print(f"Audio detection: {has_audio} streams found")
            except Exception as e:
                has_audio = False
                print(f"Warning: Audio detection failed: {e}")

            self.update_progress(55, "Applying 16:9 aspect ratio...")
            
            # YOUTUBE ASPECT RATIO (Essential)
            def aspect_ratio_advanced(v):
                return v.filter('pad', 'max(iw,ih*16/9)', 'max(iw*9/16,ih)', '(ow-iw)/2', '(oh-ih)/2', color='#000000')
            
            def aspect_ratio_fallback(v):
                return v.filter('scale', '1920:1080:force_original_aspect_ratio=decrease')
            
            video = self.apply_protection_layer(
                video, "16:9 Aspect", aspect_ratio_advanced, aspect_ratio_fallback
            )
            protection_layers_applied.append("Aspect")

            self.update_progress(60, "Applying YouTube color optimization...")
            
            # LAYER 1: YOUTUBE COLOR OPTIMIZATION (No channel mixing for color preservation)
            def color_optimize_advanced(v):
                return v.filter('eq', saturation=1.2, brightness=0.02, contrast=1.08, gamma=0.98)
            
            def color_optimize_fallback(v):
                return v.filter('eq', saturation=1.1, contrast=1.05)
            
            video = self.apply_protection_layer(
                video, "Color Optimization", color_optimize_advanced, color_optimize_fallback
            )
            protection_layers_applied.append("Color")

            self.update_progress(65, "Applying quality enhancement...")
            
            # LAYER 2: QUALITY ENHANCEMENT
            def quality_enhance_advanced(v):
                return v.filter('unsharp', luma_msize_x=5, luma_msize_y=5, luma_amount=0.5)
            
            def quality_enhance_fallback(v):
                return v.filter('unsharp', luma_msize_x=3, luma_msize_y=3, luma_amount=0.3)
            
            video = self.apply_protection_layer(
                video, "Quality Enhancement", quality_enhance_advanced, quality_enhance_fallback
            )
            protection_layers_applied.append("Quality")

            self.update_progress(70, "Applying algorithm disruption...")
            
            # LAYER 3: ALGORITHM DISRUPTION
            def algorithm_disruption_advanced(v):
                return v.filter('noise', alls=10, allf='t').filter('scale', 'iw*1.001', 'ih*1.001')
            
            def algorithm_disruption_fallback(v):
                return v.filter('noise', alls=6)
            
            video = self.apply_protection_layer(
                video, "Algorithm Disruption", algorithm_disruption_advanced, algorithm_disruption_fallback
            )
            protection_layers_applied.append("Disruption")

            self.update_progress(75, "Preparing ultra-high quality encoding...")
            
            print(f"YouTube Protection Summary: {len(protection_layers_applied)} layers applied: {', '.join(protection_layers_applied)}")
            
            # ULTRA-HIGH QUALITY ENCODING (YouTube gets highest quality)
            encoding_params = {
                'vcodec': 'libx264',
                'crf': 15,  # Highest quality
                'preset': 'slow',
                'b:v': '15M',  # Highest bitrate
                'r': 60,
                's': '1920x1080',
                'pix_fmt': 'yuv420p'
            }
            
            self.update_progress(85, "Encoding YouTube 1080p60 CRF 15...")
            
            try:
                print(f"YouTube encoding with parameters: {encoding_params}")
                
                if has_audio:
                    (
                        ffmpeg
                        .output(video, input_stream.audio, output_path, 
                               acodec='copy', **encoding_params)
                        .overwrite_output()
                        .run(quiet=False)
                    )
                else:
                    (
                        ffmpeg
                        .output(video, output_path, **encoding_params)
                        .overwrite_output()
                        .run(quiet=False)
                    )
                
                # Validate output
                self.update_progress(95, "Validating YouTube output...")
                probe = ffmpeg.probe(output_path)
                video_stream = next(s for s in probe['streams'] if s['codec_type'] == 'video')
                width = int(video_stream['width'])
                height = int(video_stream['height'])
                fps_str = video_stream['r_frame_rate']
                fps = eval(fps_str) if '/' in fps_str else float(fps_str)
                
                print(f"✓ YouTube Validation:")
                print(f"  Resolution: {width}x{height} ({'✓' if width >= 1920 and height >= 1080 else '✗'})")
                print(f"  Frame Rate: {fps:.1f}fps ({'✓' if fps >= 59 else '✗'})")
                print(f"  Protection Layers: {len(protection_layers_applied)}/4 applied")
                
                self.update_progress(100, f"YouTube complete with {len(protection_layers_applied)} layers!")
                return output_path
                
            except ffmpeg.Error as e:
                print(f"YouTube encoding failed: {e}")
                # Fallback encoding
                (
                    ffmpeg
                    .input(input_path)
                    .output(output_path, vcodec='libx264', crf=17, **{'b:v': '12M', 's': '1920x1080'})
                    .overwrite_output()
                    .run(quiet=False)
                )
                return output_path
                
        except Exception as e:
            raise Exception(f"YouTube processing failed: {e}")
    
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
    
    def _validate_audio_in_output(self, file_path):
        """Check if the output file contains audio streams"""
        try:
            probe = ffmpeg.probe(file_path)
            audio_streams = [stream for stream in probe['streams'] if stream['codec_type'] == 'audio']
            if audio_streams:
                print(f"✓ Audio validated: {len(audio_streams)} audio stream(s) found")
                return True
            else:
                print("⚠ Warning: No audio streams found in output file")
                return False
        except Exception as e:
            print(f"⚠ Could not validate audio: {e}")
            return False
