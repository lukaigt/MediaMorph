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
            'slow': self._parse_slow
        }
        
        self.image_commands = {
            'flip': self._parse_flip,
            'brightness': self._parse_brightness,
            'contrast': self._parse_contrast,
            'color': self._parse_color,
            'crop': self._parse_crop,
            'rotate': self._parse_rotate,
            'vintage': self._parse_vintage,
            'noise': self._parse_noise
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
