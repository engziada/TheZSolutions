from PIL import Image, ImageDraw, ImageFont
import os
from random import randint, choice

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

def add_network_lines(draw, width, height, num_points=10):
    """Add network-like connecting lines"""
    points = [(randint(0, width), randint(0, height)) for _ in range(num_points)]
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            if randint(0, 2) == 0:  # 1/3 chance to draw a line
                draw.line([points[i], points[j]], fill=(255, 255, 255, 50), width=1)

def create_teleo_platform_image(size=(800, 400)):
    """Create network management platform image"""
    img = create_gradient_background(size[0], size[1], (30, 64, 175), (17, 24, 39))
    draw = ImageDraw.Draw(img)
    
    # Add network-like pattern
    add_network_lines(draw, size[0], size[1], 15)
    
    # Add some "server" rectangles
    for _ in range(4):
        x = randint(50, size[0]-100)
        y = randint(50, size[1]-100)
        draw.rectangle([x, y, x+60, y+80], outline=(255, 255, 255, 80), width=2)
    
    return img

def create_enterprise_integration_image(size=(800, 400)):
    """Create enterprise integration image"""
    img = create_gradient_background(size[0], size[1], (79, 70, 229), (45, 55, 72))
    draw = ImageDraw.Draw(img)
    
    # Add connecting circles representing different systems
    centers = []
    for _ in range(6):
        x = randint(100, size[0]-100)
        y = randint(100, size[1]-100)
        r = 30
        centers.append((x, y))
        draw.ellipse([x-r, y-r, x+r, y+r], outline=(255, 255, 255, 80), width=2)
    
    # Connect the circles
    for i in range(len(centers)):
        for j in range(i + 1, len(centers)):
            if randint(0, 1) == 0:
                draw.line([centers[i], centers[j]], fill=(255, 255, 255, 50), width=1)
    
    return img

def create_yourspace_image(size=(800, 400)):
    """Create YourSpace platform image"""
    img = create_gradient_background(size[0], size[1], (6, 182, 212), (59, 130, 246))
    draw = ImageDraw.Draw(img)
    
    # Add workspace-like elements
    for _ in range(5):
        x = randint(50, size[0]-200)
        y = randint(50, size[1]-100)
        w = randint(120, 180)
        h = randint(60, 90)
        
        # Draw workspace "card"
        draw.rectangle([x, y, x+w, y+h], fill=(255, 255, 255, 30))
        draw.rectangle([x+10, y+10, x+w-10, y+30], fill=(255, 255, 255, 50))
        draw.rectangle([x+10, y+40, x+w-10, y+h-10], fill=(255, 255, 255, 20))
    
    return img

# Create directory if it doesn't exist
projects_dir = 'f:/PythonII/TheZSolutions/app/static/img/projects'
os.makedirs(projects_dir, exist_ok=True)

# Generate project images
images = {
    'teleo-platform.jpg': create_teleo_platform_image,
    'enterprise-integration.jpg': create_enterprise_integration_image,
    'yourspace.jpg': create_yourspace_image
}

for filename, create_func in images.items():
    file_path = os.path.join(projects_dir, filename)
    img = create_func()
    img.save(file_path, quality=95)
    print(f'Created {file_path}')
