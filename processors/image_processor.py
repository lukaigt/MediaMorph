from PIL import Image, ImageEnhance, ImageFilter
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
        """TikTok: Flip + color boost + noise"""
        try:
            with Image.open(input_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Horizontal flip
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
                
                # Color boost
                enhancer = ImageEnhance.Color(img)
                img = enhancer.enhance(1.3)
                
                # Brightness boost
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(1.1)
                
                # Add noise
                img = self._add_noise(img, intensity=20)
                
                img.save(output_path, 'JPEG', quality=85)
                return output_path
        except Exception as e:
            raise Exception(f"Error in TikTok image preset: {e}")
    
    def _apply_instagram_preset(self, input_path, output_path):
        """Instagram: Square crop + color enhancement + grain"""
        try:
            with Image.open(input_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Square crop
                img = self._crop_to_square(img)
                
                # Color enhancement
                enhancer = ImageEnhance.Color(img)
                img = enhancer.enhance(1.2)
                
                # Contrast boost
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(1.1)
                
                # Film grain
                img = self._add_noise(img, intensity=10)
                
                img.save(output_path, 'JPEG', quality=90)
                return output_path
        except Exception as e:
            raise Exception(f"Error in Instagram image preset: {e}")
    
    def _apply_youtube_preset(self, input_path, output_path):
        """YouTube: 16:9 letterbox + saturation"""
        try:
            with Image.open(input_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # 16:9 letterbox
                img = self._letterbox_16_9(img)
                
                # Saturation boost
                enhancer = ImageEnhance.Color(img)
                img = enhancer.enhance(1.3)
                
                # Slight sharpness increase
                enhancer = ImageEnhance.Sharpness(img)
                img = enhancer.enhance(1.1)
                
                img.save(output_path, 'JPEG', quality=95)
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
                return img.transpose(Image.FLIP_LEFT_RIGHT)
            elif params.get('direction') == 'vertical':
                return img.transpose(Image.FLIP_TOP_BOTTOM)
        
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
