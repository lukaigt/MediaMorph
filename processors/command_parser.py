import re

class CommandParser:
    def __init__(self):
        self.video_commands = {
            'flip': self._parse_flip,
            'speed': self._parse_speed,
            'zoom': self._parse_zoom,
            'rotate': self._parse_rotate,
            'brightness': self._parse_brightness,
            'contrast': self._parse_contrast,
            'vintage': self._parse_vintage,
            'slow': self._parse_slow,
            'blur': self._parse_blur,
            'sharpen': self._parse_sharpen,
            'grain': self._parse_grain,
            'glitch': self._parse_glitch,
            'chromatic': self._parse_chromatic,
            'vhs': self._parse_vhs,
            'film': self._parse_film,
            'sepia': self._parse_sepia,
            'invert': self._parse_invert,
            'mirror': self._parse_mirror,
            'kaleidoscope': self._parse_kaleidoscope,
            'wave': self._parse_wave,
            'pixelate': self._parse_pixelate,
            'oil': self._parse_oil,
            'emboss': self._parse_emboss,
            'edge': self._parse_edge,
            'solarize': self._parse_solarize,
            'posterize': self._parse_posterize,
            'gamma': self._parse_gamma,
            'hue': self._parse_hue,
            'saturation': self._parse_saturation,
            'temperature': self._parse_temperature,
            'fade': self._parse_fade,
            'vignette': self._parse_vignette,
            'tilt': self._parse_tilt,
            'compression': self._parse_compression,
            'dither': self._parse_dither,
            'halftone': self._parse_halftone,
            'letterbox': self._parse_letterbox,
            'crop_zoom': self._parse_crop_zoom,
            'stabilize': self._parse_stabilize,
            'framerate': self._parse_framerate,
            'reverse': self._parse_reverse,
            'loop': self._parse_loop,
            'echo': self._parse_echo,
            'freeze': self._parse_freeze,
            'skip': self._parse_skip,
            'audio_pitch': self._parse_audio_pitch,
            'audio_echo': self._parse_audio_echo,
            'audio_bass': self._parse_audio_bass
        }
        
        self.image_commands = {
            'flip': self._parse_flip,
            'brightness': self._parse_brightness,
            'contrast': self._parse_contrast,
            'color': self._parse_color,
            'crop': self._parse_crop,
            'rotate': self._parse_rotate,
            'vintage': self._parse_vintage,
            'noise': self._parse_noise,
            'blur': self._parse_blur,
            'sharpen': self._parse_sharpen,
            'grain': self._parse_grain,
            'glitch': self._parse_glitch,
            'chromatic': self._parse_chromatic,
            'vhs': self._parse_vhs,
            'film': self._parse_film,
            'sepia': self._parse_sepia,
            'invert': self._parse_invert,
            'mirror': self._parse_mirror,
            'kaleidoscope': self._parse_kaleidoscope,
            'wave': self._parse_wave,
            'pixelate': self._parse_pixelate,
            'oil': self._parse_oil,
            'emboss': self._parse_emboss,
            'edge': self._parse_edge,
            'solarize': self._parse_solarize,
            'posterize': self._parse_posterize,
            'gamma': self._parse_gamma,
            'hue': self._parse_hue,
            'saturation': self._parse_saturation,
            'temperature': self._parse_temperature,
            'fade': self._parse_fade,
            'vignette': self._parse_vignette,
            'tilt': self._parse_tilt,
            'compression': self._parse_compression,
            'dither': self._parse_dither,
            'halftone': self._parse_halftone,
            'letterbox': self._parse_letterbox,
            'crop_zoom': self._parse_crop_zoom,
            'square': self._parse_square,
            'portrait': self._parse_portrait,
            'landscape': self._parse_landscape,
            'fisheye': self._parse_fisheye,
            'barrel': self._parse_barrel,
            'perspective': self._parse_perspective,
            'sketch': self._parse_sketch,
            'cartoon': self._parse_cartoon,
            'watercolor': self._parse_watercolor,
            'pencil': self._parse_pencil,
            'mosaic': self._parse_mosaic,
            'cross_hatch': self._parse_cross_hatch,
            'stipple': self._parse_stipple,
            'ascii': self._parse_ascii,
            'thermal': self._parse_thermal,
            'x_ray': self._parse_x_ray,
            'night_vision': self._parse_night_vision
        }
    
    def parse_command(self, command_string, media_type):
        """Parse command string into structured commands"""
        commands = []
        
        # Split by '+' or 'and' for multiple commands
        parts = re.split(r'\s*\+\s*|\s+and\s+', command_string.lower().strip())
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
            
            parsed_command = self._parse_single_command(part, media_type)
            if parsed_command:
                commands.append(parsed_command)
        
        return commands
    
    def _parse_single_command(self, command, media_type):
        """Parse a single command"""
        command = command.strip().lower()
        
        # Get available commands for media type
        available_commands = self.video_commands if media_type == 'video' else self.image_commands
        
        for cmd_name, parser_func in available_commands.items():
            if cmd_name in command:
                return parser_func(command)
        
        return None
    
    def _parse_flip(self, command):
        """Parse flip command"""
        if 'horizontal' in command or 'left' in command or 'right' in command:
            direction = 'horizontal'
        elif 'vertical' in command or 'up' in command or 'down' in command:
            direction = 'vertical'
        else:
            direction = 'horizontal'  # default
        
        return {
            'type': 'flip',
            'params': {'direction': direction}
        }
    
    def _parse_speed(self, command):
        """Parse speed command"""
        # Look for numbers in the command
        numbers = re.findall(r'\d+\.?\d*', command)
        if numbers:
            speed_factor = float(numbers[0])
            # Handle percentage
            if '%' in command:
                speed_factor = speed_factor / 100.0
        else:
            speed_factor = 1.5  # default speed up
        
        return {
            'type': 'speed',
            'params': {'factor': speed_factor}
        }
    
    def _parse_slow(self, command):
        """Parse slow command (inverse of speed)"""
        # Look for numbers in the command
        numbers = re.findall(r'\d+\.?\d*', command)
        if numbers:
            slow_percentage = float(numbers[0])
            if '%' in command:
                speed_factor = 1.0 - (slow_percentage / 100.0)
            else:
                speed_factor = 1.0 / slow_percentage
        else:
            speed_factor = 0.8  # default slow down
        
        return {
            'type': 'speed',
            'params': {'factor': speed_factor}
        }
    
    def _parse_zoom(self, command):
        """Parse zoom command"""
        numbers = re.findall(r'\d+\.?\d*', command)
        if numbers:
            zoom_factor = float(numbers[0])
        else:
            zoom_factor = 1.2  # default zoom
        
        return {
            'type': 'zoom',
            'params': {'factor': zoom_factor}
        }
    
    def _parse_rotate(self, command):
        """Parse rotate command"""
        numbers = re.findall(r'\d+\.?\d*', command)
        if numbers:
            angle = float(numbers[0])
        else:
            angle = 90  # default rotation
        
        return {
            'type': 'rotate',
            'params': {'angle': angle}
        }
    
    def _parse_brightness(self, command):
        """Parse brightness command"""
        numbers = re.findall(r'\d+\.?\d*', command)
        if numbers:
            brightness = float(numbers[0])
        else:
            brightness = 120  # default brightness boost
        
        return {
            'type': 'brightness',
            'params': {'value': brightness}
        }
    
    def _parse_contrast(self, command):
        """Parse contrast command"""
        numbers = re.findall(r'\d+\.?\d*', command)
        if numbers:
            contrast = float(numbers[0])
        else:
            contrast = 110  # default contrast boost
        
        return {
            'type': 'contrast',
            'params': {'value': contrast}
        }
    
    def _parse_color(self, command):
        """Parse color/saturation command"""
        numbers = re.findall(r'\d+\.?\d*', command)
        if numbers:
            color = float(numbers[0])
        else:
            color = 120  # default color boost
        
        return {
            'type': 'color',
            'params': {'value': color}
        }
    
    def _parse_crop(self, command):
        """Parse crop command"""
        if 'square' in command:
            shape = 'square'
        else:
            shape = 'square'  # default
        
        return {
            'type': 'crop',
            'params': {'shape': shape}
        }
    
    def _parse_vintage(self, command):
        """Parse vintage filter command"""
        return {
            'type': 'vintage',
            'params': {}
        }
    
    def _parse_noise(self, command):
        """Parse noise/grain command"""
        numbers = re.findall(r'\d+\.?\d*', command)
        if numbers:
            intensity = int(float(numbers[0]))
        else:
            intensity = 15  # default noise intensity
        
        return {
            'type': 'noise',
            'params': {'intensity': intensity}
        }
    
    # Additional parsing functions for new commands
    def _parse_blur(self, command):
        numbers = re.findall(r'\d+\.?\d*', command)
        strength = float(numbers[0]) if numbers else 5.0
        return {'type': 'blur', 'params': {'strength': strength}}
    
    def _parse_sharpen(self, command):
        numbers = re.findall(r'\d+\.?\d*', command)
        strength = float(numbers[0]) if numbers else 1.5
        return {'type': 'sharpen', 'params': {'strength': strength}}
    
    def _parse_grain(self, command):
        numbers = re.findall(r'\d+\.?\d*', command)
        amount = float(numbers[0]) if numbers else 25
        return {'type': 'grain', 'params': {'amount': amount}}
    
    def _parse_glitch(self, command):
        numbers = re.findall(r'\d+\.?\d*', command)
        intensity = float(numbers[0]) if numbers else 10
        return {'type': 'glitch', 'params': {'intensity': intensity}}
    
    def _parse_chromatic(self, command):
        numbers = re.findall(r'\d+\.?\d*', command)
        shift = float(numbers[0]) if numbers else 3
        return {'type': 'chromatic', 'params': {'shift': shift}}
    
    def _parse_vhs(self, command):
        return {'type': 'vhs', 'params': {}}
    
    def _parse_film(self, command):
        return {'type': 'film', 'params': {}}
    
    def _parse_sepia(self, command):
        return {'type': 'sepia', 'params': {}}
    
    def _parse_invert(self, command):
        return {'type': 'invert', 'params': {}}
    
    def _parse_mirror(self, command):
        direction = 'horizontal'
        if 'vertical' in command or 'v' in command:
            direction = 'vertical'
        return {'type': 'mirror', 'params': {'direction': direction}}
    
    def _parse_kaleidoscope(self, command):
        numbers = re.findall(r'\d+', command)
        segments = int(numbers[0]) if numbers else 6
        return {'type': 'kaleidoscope', 'params': {'segments': segments}}
    
    def _parse_wave(self, command):
        numbers = re.findall(r'\d+\.?\d*', command)
        amplitude = float(numbers[0]) if numbers else 10
        frequency = float(numbers[1]) if len(numbers) > 1 else 0.5
        return {'type': 'wave', 'params': {'amplitude': amplitude, 'frequency': frequency}}
    
    def _parse_pixelate(self, command):
        numbers = re.findall(r'\d+', command)
        pixel_size = int(numbers[0]) if numbers else 8
        return {'type': 'pixelate', 'params': {'pixel_size': pixel_size}}
    
    def _parse_oil(self, command):
        numbers = re.findall(r'\d+\.?\d*', command)
        radius = float(numbers[0]) if numbers else 4
        return {'type': 'oil', 'params': {'radius': radius}}
    
    def _parse_emboss(self, command):
        return {'type': 'emboss', 'params': {}}
    
    def _parse_edge(self, command):
        return {'type': 'edge', 'params': {}}
    
    def _parse_solarize(self, command):
        numbers = re.findall(r'\d+', command)
        threshold = int(numbers[0]) if numbers else 128
        return {'type': 'solarize', 'params': {'threshold': threshold}}
    
    def _parse_posterize(self, command):
        numbers = re.findall(r'\d+', command)
        bits = int(numbers[0]) if numbers else 4
        return {'type': 'posterize', 'params': {'bits': bits}}
    
    def _parse_gamma(self, command):
        numbers = re.findall(r'\d+\.?\d*', command)
        gamma = float(numbers[0]) if numbers else 1.2
        return {'type': 'gamma', 'params': {'gamma': gamma}}
    
    def _parse_hue(self, command):
        numbers = re.findall(r'-?\d+\.?\d*', command)
        shift = float(numbers[0]) if numbers else 30
        return {'type': 'hue', 'params': {'shift': shift}}
    
    def _parse_saturation(self, command):
        numbers = re.findall(r'\d+\.?\d*', command)
        factor = float(numbers[0]) if numbers else 1.3
        return {'type': 'saturation', 'params': {'factor': factor}}
    
    def _parse_temperature(self, command):
        numbers = re.findall(r'-?\d+', command)
        temp = int(numbers[0]) if numbers else 200
        return {'type': 'temperature', 'params': {'temp': temp}}
    
    def _parse_fade(self, command):
        numbers = re.findall(r'\d+\.?\d*', command)
        amount = float(numbers[0]) if numbers else 0.3
        return {'type': 'fade', 'params': {'amount': amount}}
    
    def _parse_vignette(self, command):
        numbers = re.findall(r'\d+\.?\d*', command)
        strength = float(numbers[0]) if numbers else 0.8
        return {'type': 'vignette', 'params': {'strength': strength}}
    
    def _parse_tilt(self, command):
        numbers = re.findall(r'-?\d+\.?\d*', command)
        angle = float(numbers[0]) if numbers else 2.0
        return {'type': 'tilt', 'params': {'angle': angle}}
    
    def _parse_compression(self, command):
        numbers = re.findall(r'\d+', command)
        quality = int(numbers[0]) if numbers else 70
        return {'type': 'compression', 'params': {'quality': quality}}
    
    def _parse_dither(self, command):
        return {'type': 'dither', 'params': {}}
    
    def _parse_halftone(self, command):
        numbers = re.findall(r'\d+', command)
        dots = int(numbers[0]) if numbers else 15
        return {'type': 'halftone', 'params': {'dots': dots}}
    
    def _parse_letterbox(self, command):
        return {'type': 'letterbox', 'params': {}}
    
    def _parse_crop_zoom(self, command):
        numbers = re.findall(r'\d+\.?\d*', command)
        zoom = float(numbers[0]) if numbers else 1.2
        return {'type': 'crop_zoom', 'params': {'zoom': zoom}}
    
    def _parse_stabilize(self, command):
        return {'type': 'stabilize', 'params': {}}
    
    def _parse_framerate(self, command):
        numbers = re.findall(r'\d+', command)
        fps = int(numbers[0]) if numbers else 30
        return {'type': 'framerate', 'params': {'fps': fps}}
    
    def _parse_reverse(self, command):
        return {'type': 'reverse', 'params': {}}
    
    def _parse_loop(self, command):
        numbers = re.findall(r'\d+', command)
        times = int(numbers[0]) if numbers else 2
        return {'type': 'loop', 'params': {'times': times}}
    
    def _parse_echo(self, command):
        numbers = re.findall(r'\d+\.?\d*', command)
        delay = float(numbers[0]) if numbers else 0.5
        return {'type': 'echo', 'params': {'delay': delay}}
    
    def _parse_freeze(self, command):
        numbers = re.findall(r'\d+\.?\d*', command)
        duration = float(numbers[0]) if numbers else 1.0
        return {'type': 'freeze', 'params': {'duration': duration}}
    
    def _parse_skip(self, command):
        numbers = re.findall(r'\d+\.?\d*', command)
        seconds = float(numbers[0]) if numbers else 1.0
        return {'type': 'skip', 'params': {'seconds': seconds}}
    
    def _parse_audio_pitch(self, command):
        numbers = re.findall(r'\d+\.?\d*', command)
        pitch = float(numbers[0]) if numbers else 1.2
        return {'type': 'audio_pitch', 'params': {'pitch': pitch}}
    
    def _parse_audio_echo(self, command):
        numbers = re.findall(r'\d+\.?\d*', command)
        delay = float(numbers[0]) if numbers else 0.3
        return {'type': 'audio_echo', 'params': {'delay': delay}}
    
    def _parse_audio_bass(self, command):
        numbers = re.findall(r'\d+\.?\d*', command)
        boost = float(numbers[0]) if numbers else 5
        return {'type': 'audio_bass', 'params': {'boost': boost}}
    
    def _parse_square(self, command):
        return {'type': 'square', 'params': {}}
    
    def _parse_portrait(self, command):
        return {'type': 'portrait', 'params': {}}
    
    def _parse_landscape(self, command):
        return {'type': 'landscape', 'params': {}}
    
    def _parse_fisheye(self, command):
        numbers = re.findall(r'\d+\.?\d*', command)
        strength = float(numbers[0]) if numbers else 0.8
        return {'type': 'fisheye', 'params': {'strength': strength}}
    
    def _parse_barrel(self, command):
        numbers = re.findall(r'\d+\.?\d*', command)
        distortion = float(numbers[0]) if numbers else 0.3
        return {'type': 'barrel', 'params': {'distortion': distortion}}
    
    def _parse_perspective(self, command):
        return {'type': 'perspective', 'params': {}}
    
    def _parse_sketch(self, command):
        return {'type': 'sketch', 'params': {}}
    
    def _parse_cartoon(self, command):
        return {'type': 'cartoon', 'params': {}}
    
    def _parse_watercolor(self, command):
        return {'type': 'watercolor', 'params': {}}
    
    def _parse_pencil(self, command):
        return {'type': 'pencil', 'params': {}}
    
    def _parse_mosaic(self, command):
        numbers = re.findall(r'\d+', command)
        tile_size = int(numbers[0]) if numbers else 20
        return {'type': 'mosaic', 'params': {'tile_size': tile_size}}
    
    def _parse_cross_hatch(self, command):
        return {'type': 'cross_hatch', 'params': {}}
    
    def _parse_stipple(self, command):
        return {'type': 'stipple', 'params': {}}
    
    def _parse_ascii(self, command):
        return {'type': 'ascii', 'params': {}}
    
    def _parse_thermal(self, command):
        return {'type': 'thermal', 'params': {}}
    
    def _parse_x_ray(self, command):
        return {'type': 'x_ray', 'params': {}}
    
    def _parse_night_vision(self, command):
        return {'type': 'night_vision', 'params': {}}
