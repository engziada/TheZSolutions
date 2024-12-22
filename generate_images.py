from PIL import Image, ImageDraw, ImageFont
import os
from random import randint

def create_gradient_background(width, height, color1, color2):
    """Create a gradient background"""
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)
    for y in range(height):
        r = int(color1[0] + (color2[0] - color1[0]) * y / height)
        g = int(color1[1] + (color2[1] - color1[1]) * y / height)
        b = int(color1[2] + (color2[2] - color1[2]) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    return image

def create_project_image(name, size=(800, 400)):
    """Create project placeholder images with modern UI elements"""
    # Create base image with gradient
    img = create_gradient_background(size[0], size[1], (45, 55, 72), (74, 85, 104))
    draw = ImageDraw.Draw(img)
    
    # Add some UI elements
    for i in range(3):
        x = randint(50, size[0]-200)
        y = randint(50, size[1]-100)
        w = randint(100, 180)
        h = randint(40, 80)
        draw.rectangle([x, y, x+w, y+h], fill=(255, 255, 255, 50))
    
    return img

def create_profile_image(size=(400, 400)):
    """Create professional-looking profile placeholder"""
    # Create base image with gradient
    img = create_gradient_background(size[0], size[1], (49, 46, 129), (79, 70, 229))
    draw = ImageDraw.Draw(img)
    
    # Add a circle for the profile
    margin = size[0] // 4
    draw.ellipse([margin, margin, size[0]-margin, size[1]-margin], 
                 fill=(255, 255, 255, 50))
    
    return img

# Create directories if they don't exist
base_path = 'f:/PythonII/TheZSolutions/app/static/img'
directories = {
    'projects': ['mall-system.jpg', 'clinic-system.jpg', 'edu-portal.jpg'],
    'testimonials': ['ahmed.jpg', 'fatima.jpg'],
    'team': ['ziada.jpg', 'omar.jpg', 'layla.jpg', 'kareem.jpg']
}

for directory, files in directories.items():
    dir_path = os.path.join(base_path, directory)
    os.makedirs(dir_path, exist_ok=True)
    
    for file in files:
        file_path = os.path.join(dir_path, file)
        if directory == 'projects':
            img = create_project_image(file.split('.')[0])
        else:
            img = create_profile_image()
        
        img.save(file_path, quality=95)
        print(f'Created {file_path}')
