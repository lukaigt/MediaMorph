from PIL import Image, ImageEnhance, ImageFilter
from PIL.Image import Resampling
import tempfile
import os
from pathlib import Path
import numpy as np

class ImageProcessor:
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
    
    def apply_preset(self, input_path, platform):
        """Apply platform-specific preset to image"""
        output_path = os.path.join(self.temp_dir, f"processed_{platform}_{Path(input_path).stem}.jpg")
        
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
            with Image.open(input_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Skip horizontal flip to preserve text readability
                # Instead use advanced noise patterns for algorithm evasion
                
                # Multiple color adjustments for heavy algorithm evasion
                enhancer = ImageEnhance.Color(img)
                img = enhancer.enhance(1.35)
                
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(1.08)
                
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(1.12)
                
                enhancer = ImageEnhance.Sharpness(img)
                img = enhancer.enhance(1.15)
                
                # Add strong noise for algorithm confusion
                img = self._add_noise(img, intensity=30)
                
                # Advanced hash evasion techniques
                img = self._apply_steganographic_evasion(img, intensity=20)
                img = self._apply_perceptual_hash_evasion(img)
                img = self._apply_dct_domain_modifications(img)
                
                # Apply subtle rotation to change pixel positions
                img = img.rotate(0.5, expand=False, fillcolor=(0, 0, 0))
                
                # Color channel manipulation
                img = self._adjust_color_channels(img, r_adjust=1.02, g_adjust=0.98, b_adjust=1.01)
                
                # Micro resize to change file hash
                width, height = img.size
                img = img.resize((int(width * 0.999), int(height * 0.999)), Resampling.LANCZOS)
                img = img.resize((width, height), Resampling.LANCZOS)
                
                img.save(output_path, 'JPEG', quality=82, optimize=True)
                return output_path
        except Exception as e:
            raise Exception(f"Error in TikTok image preset: {e}")
    
    def _apply_instagram_preset(self, input_path, output_path):
        """Instagram: Advanced square processing with heavy algorithm evasion"""
        try:
            with Image.open(input_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Square crop
                img = self._crop_to_square(img)
                
                # Heavy color and contrast adjustments
                enhancer = ImageEnhance.Color(img)
                img = enhancer.enhance(1.28)
                
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(1.14)
                
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(1.05)
                
                enhancer = ImageEnhance.Sharpness(img)
                img = enhancer.enhance(1.18)
                
                # Strong film grain and noise
                img = self._add_noise(img, intensity=22)
                
                # Advanced algorithm evasion for Instagram
                img = self._apply_steganographic_evasion(img, intensity=18)
                img = self._apply_perceptual_hash_evasion(img)
                img = self._apply_dct_domain_modifications(img)
                
                # Color channel manipulation for algorithm confusion
                img = self._adjust_color_channels(img, r_adjust=1.03, g_adjust=0.97, b_adjust=1.02)
                
                # Micro rotation and resize
                img = img.rotate(-0.3, expand=False, fillcolor=(0, 0, 0))
                
                # Scale manipulation to change hash
                width, height = img.size
                img = img.resize((int(width * 1.002), int(height * 1.002)), Resampling.LANCZOS)
                img = img.resize((width, height), Resampling.LANCZOS)
                
                img.save(output_path, 'JPEG', quality=88, optimize=True)
                return output_path
        except Exception as e:
            raise Exception(f"Error in Instagram image preset: {e}")
    
    def _apply_youtube_preset(self, input_path, output_path):
        """YouTube: Advanced landscape processing with heavy algorithm evasion"""
        try:
            with Image.open(input_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # 16:9 letterbox
                img = self._letterbox_16_9(img)
                
                # Heavy color and enhancement adjustments
                enhancer = ImageEnhance.Color(img)
                img = enhancer.enhance(1.38)
                
                enhancer = ImageEnhance.Sharpness(img)
                img = enhancer.enhance(1.22)
                
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(1.08)
                
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(1.02)
                
                # Algorithm evasion noise
                img = self._add_noise(img, intensity=18)
                
                # Advanced YouTube-specific evasion
                img = self._apply_steganographic_evasion(img, intensity=16)
                img = self._apply_perceptual_hash_evasion(img)
                img = self._apply_dct_domain_modifications(img)
                
                # Color channel manipulation
                img = self._adjust_color_channels(img, r_adjust=0.99, g_adjust=1.02, b_adjust=0.98)
                
                # Tiny rotation for pixel position changes
                img = img.rotate(0.2, expand=False, fillcolor=(1, 1, 1))
                
                # Scale manipulation
                width, height = img.size
                img = img.resize((int(width * 1.001), int(height * 1.001)), Resampling.LANCZOS)
                img = img.resize((width, height), Resampling.LANCZOS)
                
                img.save(output_path, 'JPEG', quality=91, optimize=True)
                return output_path
        except Exception as e:
            raise Exception(f"Error in YouTube image preset: {e}")
    
    def apply_custom_commands(self, input_path, commands):
        """Apply custom commands to image"""
        output_path = os.path.join(self.temp_dir, f"custom_{Path(input_path).stem}.jpg")
        
        try:
            with Image.open(input_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                for command in commands:
                    img = self._apply_image_command(img, command)
                
                img.save(output_path, 'JPEG', quality=90)
                return output_path
        except Exception as e:
            raise Exception(f"Error in custom image commands: {e}")
    
    def _apply_image_command(self, img, command):
        """Apply individual image command"""
        cmd_type = command['type']
        params = command['params']
        
        if cmd_type == 'flip':
            if params.get('direction') == 'horizontal':
                return img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            elif params.get('direction') == 'vertical':
                return img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        
        elif cmd_type == 'brightness':
            value = params.get('value', 100) / 100.0
            enhancer = ImageEnhance.Brightness(img)
            return enhancer.enhance(value)
        
        elif cmd_type == 'contrast':
            value = params.get('value', 100) / 100.0
            enhancer = ImageEnhance.Contrast(img)
            return enhancer.enhance(value)
        
        elif cmd_type == 'color':
            value = params.get('value', 100) / 100.0
            enhancer = ImageEnhance.Color(img)
            return enhancer.enhance(value)
        
        elif cmd_type == 'crop':
            if params.get('shape') == 'square':
                return self._crop_to_square(img)
        
        elif cmd_type == 'rotate':
            angle = params.get('angle', 0)
            return img.rotate(angle, expand=True)
        
        elif cmd_type == 'vintage':
            return self._apply_vintage_filter(img)
        
        elif cmd_type == 'noise':
            intensity = params.get('intensity', 15)
            return self._add_noise(img, intensity)
        
        return img
    
    def _crop_to_square(self, img):
        """Crop image to square aspect ratio"""
        width, height = img.size
        size = min(width, height)
        left = (width - size) // 2
        top = (height - size) // 2
        right = left + size
        bottom = top + size
        return img.crop((left, top, right, bottom))
    
    def _letterbox_16_9(self, img):
        """Add letterbox padding to make 16:9 aspect ratio"""
        width, height = img.size
        target_ratio = 16 / 9
        current_ratio = width / height
        
        if current_ratio > target_ratio:
            # Image is wider than 16:9, add vertical padding
            new_height = int(width / target_ratio)
            new_img = Image.new('RGB', (width, new_height), color='black')
            paste_y = (new_height - height) // 2
            new_img.paste(img, (0, paste_y))
        else:
            # Image is taller than 16:9, add horizontal padding
            new_width = int(height * target_ratio)
            new_img = Image.new('RGB', (new_width, height), color='black')
            paste_x = (new_width - width) // 2
            new_img.paste(img, (paste_x, 0))
        
        return new_img
    
    def _add_noise(self, img, intensity=15):
        """Add noise/grain to image"""
        img_array = np.array(img)
        noise = np.random.randint(-intensity, intensity + 1, img_array.shape, dtype=np.int16)
        noisy_array = np.clip(img_array.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        return Image.fromarray(noisy_array)
    
    def _apply_vintage_filter(self, img):
        """Apply vintage/sepia filter"""
        # Convert to sepia
        img_array = np.array(img)
        sepia_filter = np.array([
            [0.393, 0.769, 0.189],
            [0.349, 0.686, 0.168],
            [0.272, 0.534, 0.131]
        ])
        
        sepia_img = img_array @ sepia_filter.T
        sepia_img = np.clip(sepia_img, 0, 255).astype(np.uint8)
        vintage_img = Image.fromarray(sepia_img)
        
        # Add slight grain
        vintage_img = self._add_noise(vintage_img, intensity=10)
        
        # Reduce contrast slightly for vintage look
        enhancer = ImageEnhance.Contrast(vintage_img)
        vintage_img = enhancer.enhance(0.9)
        
        return vintage_img
    
    def _adjust_color_channels(self, img, r_adjust=1.0, g_adjust=1.0, b_adjust=1.0):
        """Adjust individual color channels for algorithm evasion"""
        img_array = np.array(img)
        
        # Adjust each channel separately
        img_array[:, :, 0] = np.clip(img_array[:, :, 0] * r_adjust, 0, 255)  # Red
        img_array[:, :, 1] = np.clip(img_array[:, :, 1] * g_adjust, 0, 255)  # Green
        img_array[:, :, 2] = np.clip(img_array[:, :, 2] * b_adjust, 0, 255)  # Blue
        
        return Image.fromarray(img_array.astype(np.uint8))
    
    def _apply_steganographic_evasion(self, img, intensity=15):
        """Apply LSB steganography-based evasion to modify hash"""
        img_array = np.array(img)
        height, width, channels = img_array.shape
        
        # Generate pseudo-random modifications based on pixel positions
        np.random.seed(42)  # Consistent but unpredictable pattern
        for i in range(0, height, 8):
            for j in range(0, width, 8):
                # Modify LSB of random pixels to change hash
                if np.random.random() > 0.7:
                    # Flip least significant bit
                    for c in range(channels):
                        if i < height and j < width:
                            img_array[i, j, c] = img_array[i, j, c] ^ 1
        
        return Image.fromarray(img_array)
    
    def _apply_perceptual_hash_evasion(self, img):
        """Apply gradient-based perturbations to evade perceptual hashing"""
        img_array = np.array(img).astype(np.float32)
        height, width, channels = img_array.shape
        
        # Add minimal gradient-based noise that changes hash but preserves perception
        gradient_noise = np.random.uniform(-2, 2, (height, width, channels))
        
        # Apply noise more heavily to edges and high-frequency areas
        from scipy import ndimage
        edges = ndimage.sobel(np.mean(img_array, axis=2))
        edges_3d = np.stack([edges] * channels, axis=2)
        
        # Amplify noise in edge regions
        adaptive_noise = gradient_noise * (1 + edges_3d / 255.0 * 0.5)
        
        modified_array = img_array + adaptive_noise
        modified_array = np.clip(modified_array, 0, 255).astype(np.uint8)
        
        return Image.fromarray(modified_array)
    
    def _apply_dct_domain_modifications(self, img):
        """Apply discrete cosine transform domain modifications"""
        img_array = np.array(img)
        height, width, channels = img_array.shape
        
        # Process in 8x8 blocks like JPEG compression
        for i in range(0, height - 8, 8):
            for j in range(0, width - 8, 8):
                for c in range(channels):
                    block = img_array[i:i+8, j:j+8, c].astype(np.float32)
                    
                    # Apply DCT
                    from scipy.fft import dctn, idctn
                    dct_block = dctn(block, norm='ortho')
                    
                    # Modify high-frequency coefficients slightly
                    if np.random.random() > 0.6:
                        dct_block[6:8, 6:8] += np.random.uniform(-0.5, 0.5, (2, 2))
                    
                    # Apply inverse DCT
                    modified_block = idctn(dct_block, norm='ortho')
                    img_array[i:i+8, j:j+8, c] = np.clip(modified_block, 0, 255)
        
        return Image.fromarray(img_array.astype(np.uint8))
    
    def apply_custom_command(self, input_path, commands):
        """Apply custom commands to image"""
        output_path = input_path.replace('.jpg', '_custom.jpg').replace('.png', '_custom.jpg')
        
        try:
            with Image.open(input_path) as img:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Apply each command in sequence
                for command in commands:
                    img = self._apply_single_command(img, command)
                
                img.save(output_path, 'JPEG', quality=85, optimize=True)
                return output_path
        except Exception as e:
            raise Exception(f"Error applying custom commands: {e}")
    
    def _apply_single_command(self, img, command):
        """Apply a single command to image"""
        cmd_type = command['type']
        params = command['params']
        
        # Basic adjustments
        if cmd_type == 'brightness':
            enhancer = ImageEnhance.Brightness(img)
            return enhancer.enhance(params['value'] / 100.0)
        elif cmd_type == 'contrast':
            enhancer = ImageEnhance.Contrast(img)
            return enhancer.enhance(params['value'] / 100.0)
        elif cmd_type == 'color':
            enhancer = ImageEnhance.Color(img)
            return enhancer.enhance(params['value'] / 100.0)
        elif cmd_type == 'flip':
            if params['direction'] == 'horizontal':
                return img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            else:
                return img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        elif cmd_type == 'rotate':
            return img.rotate(params['degrees'], expand=False, fillcolor=(0, 0, 0))
        elif cmd_type == 'crop':
            if params['shape'] == 'square':
                return self._crop_to_square(img)
            return img
        elif cmd_type == 'noise':
            return self._add_noise(img, params['intensity'])
        elif cmd_type == 'vintage':
            return self._apply_vintage_filter(img)
        
        # New advanced effects
        elif cmd_type == 'blur':
            from PIL import ImageFilter
            return img.filter(ImageFilter.GaussianBlur(radius=params['strength']))
        elif cmd_type == 'sharpen':
            enhancer = ImageEnhance.Sharpness(img)
            return enhancer.enhance(params['strength'])
        elif cmd_type == 'grain':
            return self._add_noise(img, params['amount'])
        elif cmd_type == 'glitch':
            return self._apply_glitch_effect(img, params['intensity'])
        elif cmd_type == 'chromatic':
            return self._apply_chromatic_aberration(img, params['shift'])
        elif cmd_type == 'vhs':
            return self._apply_vhs_effect(img)
        elif cmd_type == 'film':
            return self._apply_film_effect(img)
        elif cmd_type == 'sepia':
            return self._apply_sepia_effect(img)
        elif cmd_type == 'invert':
            from PIL import ImageOps
            return ImageOps.invert(img)
        elif cmd_type == 'mirror':
            if params['direction'] == 'horizontal':
                width, height = img.size
                left = img.crop((0, 0, width//2, height))
                mirrored = left.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                result = Image.new('RGB', (width, height))
                result.paste(left, (0, 0))
                result.paste(mirrored, (width//2, 0))
                return result
            else:
                width, height = img.size
                top = img.crop((0, 0, width, height//2))
                mirrored = top.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
                result = Image.new('RGB', (width, height))
                result.paste(top, (0, 0))
                result.paste(mirrored, (0, height//2))
                return result
        elif cmd_type == 'pixelate':
            size = params['pixel_size']
            width, height = img.size
            small = img.resize((width//size, height//size), Image.Resampling.NEAREST)
            return small.resize((width, height), Image.Resampling.NEAREST)
        elif cmd_type == 'emboss':
            from PIL import ImageFilter
            return img.filter(ImageFilter.EMBOSS)
        elif cmd_type == 'edge':
            from PIL import ImageFilter
            return img.filter(ImageFilter.FIND_EDGES)
        elif cmd_type == 'solarize':
            from PIL import ImageOps
            return ImageOps.solarize(img, threshold=params['threshold'])
        elif cmd_type == 'posterize':
            from PIL import ImageOps
            return ImageOps.posterize(img, bits=params['bits'])
        elif cmd_type == 'gamma':
            return self._apply_gamma_correction(img, params['gamma'])
        elif cmd_type == 'hue':
            return self._adjust_hue(img, params['shift'])
        elif cmd_type == 'saturation':
            enhancer = ImageEnhance.Color(img)
            return enhancer.enhance(params['factor'])
        elif cmd_type == 'vignette':
            return self._apply_vignette(img, params['strength'])
        elif cmd_type == 'tilt':
            return img.rotate(params['angle'], expand=False, fillcolor=(0, 0, 0))
        elif cmd_type == 'dither':
            return img.convert('P', dither=Image.Dither.FLOYDSTEINBERG).convert('RGB')
        elif cmd_type == 'square':
            return self._crop_to_square(img)
        elif cmd_type == 'fisheye':
            return self._apply_fisheye_effect(img, params['strength'])
        elif cmd_type == 'sketch':
            return self._apply_sketch_effect(img)
        elif cmd_type == 'cartoon':
            return self._apply_cartoon_effect(img)
        elif cmd_type == 'thermal':
            return self._apply_thermal_effect(img)
        elif cmd_type == 'night_vision':
            return self._apply_night_vision_effect(img)
        
        return img
    
    def _apply_glitch_effect(self, img, intensity):
        """Apply digital glitch effect"""
        img_array = np.array(img)
        height, width, channels = img_array.shape
        
        # Random horizontal shifts
        for _ in range(int(intensity)):
            y = np.random.randint(0, height)
            shift = np.random.randint(-20, 20)
            if shift > 0:
                img_array[y, shift:] = img_array[y, :-shift]
            elif shift < 0:
                img_array[y, :shift] = img_array[y, -shift:]
        
        # Color channel corruption
        if np.random.random() > 0.5:
            channel = np.random.randint(0, 3)
            corruption = np.random.randint(0, 50)
            img_array[:, :, channel] = np.clip(img_array[:, :, channel] + corruption, 0, 255)
        
        return Image.fromarray(img_array.astype(np.uint8))
    
    def _apply_chromatic_aberration(self, img, shift):
        """Apply chromatic aberration effect"""
        img_array = np.array(img)
        height, width, channels = img_array.shape
        
        # Shift red and blue channels
        red_shifted = np.zeros_like(img_array)
        blue_shifted = np.zeros_like(img_array)
        
        shift = int(shift)
        
        # Red channel shift
        red_shifted[:-shift, :-shift, 0] = img_array[shift:, shift:, 0]
        red_shifted[:, :, 1] = img_array[:, :, 1]
        
        # Blue channel shift  
        blue_shifted[shift:, shift:, 2] = img_array[:-shift, :-shift, 2]
        blue_shifted[:, :, 1] = img_array[:, :, 1]
        
        # Combine with original green
        result = np.zeros_like(img_array)
        result[:, :, 0] = red_shifted[:, :, 0]
        result[:, :, 1] = img_array[:, :, 1]
        result[:, :, 2] = blue_shifted[:, :, 2]
        
        return Image.fromarray(result.astype(np.uint8))
    
    def _apply_vhs_effect(self, img):
        """Apply VHS tape effect"""
        img_array = np.array(img)
        
        # Add horizontal noise lines
        for i in range(0, img_array.shape[0], 3):
            if np.random.random() > 0.7:
                img_array[i] = np.clip(img_array[i] + np.random.randint(-30, 30), 0, 255)
        
        # Color bleeding
        img_array[:, :, 0] = np.roll(img_array[:, :, 0], 1, axis=1)  # Red shift
        
        # Reduce saturation slightly
        img = Image.fromarray(img_array.astype(np.uint8))
        enhancer = ImageEnhance.Color(img)
        return enhancer.enhance(0.8)
    
    def _apply_film_effect(self, img):
        """Apply film grain and color effect"""
        img_array = np.array(img)
        
        # Add film grain
        grain = np.random.normal(0, 15, img_array.shape)
        img_array = np.clip(img_array + grain, 0, 255)
        
        # Slight color temperature shift
        img_array[:, :, 0] = np.clip(img_array[:, :, 0] * 1.1, 0, 255)  # Warm reds
        img_array[:, :, 2] = np.clip(img_array[:, :, 2] * 0.9, 0, 255)  # Cool blues
        
        return Image.fromarray(img_array.astype(np.uint8))
    
    def _apply_sepia_effect(self, img):
        """Apply sepia tone effect"""
        img_array = np.array(img).astype(np.float64)
        
        # Sepia transformation matrix
        sepia_filter = np.array([
            [0.393, 0.769, 0.189],
            [0.349, 0.686, 0.168],
            [0.272, 0.534, 0.131]
        ])
        
        sepia_img = img_array.dot(sepia_filter.T)
        sepia_img = np.clip(sepia_img, 0, 255)
        
        return Image.fromarray(sepia_img.astype(np.uint8))
    
    def _apply_gamma_correction(self, img, gamma):
        """Apply gamma correction"""
        img_array = np.array(img).astype(np.float64) / 255.0
        corrected = np.power(img_array, gamma)
        return Image.fromarray((corrected * 255).astype(np.uint8))
    
    def _adjust_hue(self, img, shift):
        """Adjust hue by shift degrees"""
        img_array = np.array(img)
        
        # Convert to HSV
        from PIL import ImageEnhance
        import colorsys
        
        # Simple hue shift by adjusting color channels
        shift_factor = shift / 360.0
        
        # Rotate color channels slightly
        if shift > 0:
            r, g, b = img_array[:,:,0], img_array[:,:,1], img_array[:,:,2]
            img_array[:,:,0] = np.clip(r * (1 + shift_factor), 0, 255)
            img_array[:,:,1] = np.clip(g * (1 - shift_factor * 0.5), 0, 255)
        
        return Image.fromarray(img_array.astype(np.uint8))
    
    def _apply_vignette(self, img, strength):
        """Apply vignette effect"""
        img_array = np.array(img)
        height, width = img_array.shape[:2]
        
        # Create vignette mask
        Y, X = np.ogrid[:height, :width]
        center_x, center_y = width // 2, height // 2
        
        # Distance from center
        dist_from_center = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
        max_dist = np.sqrt(center_x**2 + center_y**2)
        
        # Create vignette
        vignette = 1 - (dist_from_center / max_dist) * strength
        vignette = np.clip(vignette, 0, 1)
        
        # Apply to all channels
        for i in range(3):
            img_array[:, :, i] = img_array[:, :, i] * vignette
        
        return Image.fromarray(img_array.astype(np.uint8))
    
    def _apply_fisheye_effect(self, img, strength):
        """Apply fisheye lens distortion"""
        width, height = img.size
        img_array = np.array(img)
        
        # Create coordinate grids
        x, y = np.meshgrid(np.arange(width), np.arange(height))
        
        # Center coordinates
        cx, cy = width // 2, height // 2
        
        # Convert to polar coordinates
        dx, dy = x - cx, y - cy
        r = np.sqrt(dx**2 + dy**2)
        max_r = min(cx, cy)
        
        # Apply fisheye transformation
        r_new = r * (1 + strength * (r / max_r)**2)
        
        # Convert back to cartesian
        theta = np.arctan2(dy, dx)
        x_new = cx + r_new * np.cos(theta)
        y_new = cy + r_new * np.sin(theta)
        
        # Clip coordinates
        x_new = np.clip(x_new, 0, width - 1).astype(int)
        y_new = np.clip(y_new, 0, height - 1).astype(int)
        
        # Map pixels
        result = np.zeros_like(img_array)
        result[y, x] = img_array[y_new, x_new]
        
        return Image.fromarray(result)
    
    def _apply_sketch_effect(self, img):
        """Apply pencil sketch effect"""
        # Convert to grayscale
        gray = img.convert('L')
        
        # Invert
        from PIL import ImageOps
        inverted = ImageOps.invert(gray)
        
        # Blur
        from PIL import ImageFilter
        blurred = inverted.filter(ImageFilter.GaussianBlur(radius=5))
        
        # Blend with original
        result = Image.blend(gray.convert('RGB'), blurred.convert('RGB'), 0.8)
        return result
    
    def _apply_cartoon_effect(self, img):
        """Apply cartoon effect"""
        img_array = np.array(img)
        
        # Reduce colors (posterize)
        img_array = (img_array // 32) * 32
        
        # Apply slight blur
        from PIL import ImageFilter
        img = Image.fromarray(img_array.astype(np.uint8))
        blurred = img.filter(ImageFilter.GaussianBlur(radius=1))
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(blurred)
        return enhancer.enhance(1.3)
    
    def _apply_thermal_effect(self, img):
        """Apply thermal imaging effect"""
        # Convert to grayscale
        gray = img.convert('L')
        gray_array = np.array(gray)
        
        # Create thermal color map
        thermal = np.zeros((gray_array.shape[0], gray_array.shape[1], 3), dtype=np.uint8)
        
        # Map grayscale to thermal colors (blue to red)
        thermal[:, :, 0] = gray_array  # Red channel
        thermal[:, :, 1] = 255 - gray_array  # Green channel
        thermal[:, :, 2] = 255 - gray_array  # Blue channel
        
        return Image.fromarray(thermal)
    
    def _apply_night_vision_effect(self, img):
        """Apply night vision effect"""
        # Convert to grayscale
        gray = img.convert('L')
        
        # Convert back to RGB with green tint
        rgb_array = np.array(gray.convert('RGB'))
        rgb_array[:, :, 0] = rgb_array[:, :, 0] * 0.3  # Reduce red
        rgb_array[:, :, 1] = rgb_array[:, :, 1] * 1.5  # Enhance green
        rgb_array[:, :, 2] = rgb_array[:, :, 2] * 0.3  # Reduce blue
        
        rgb_array = np.clip(rgb_array, 0, 255)
        
        # Add scanlines
        for i in range(0, rgb_array.shape[0], 4):
            rgb_array[i] = rgb_array[i] * 0.8
        
        return Image.fromarray(rgb_array.astype(np.uint8))
