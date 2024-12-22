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

def create_event_system_image(size=(800, 400)):
    """Create event registration system image"""
    img = create_gradient_background(size[0], size[1], (220, 38, 38), (136, 19, 55))
    draw = ImageDraw.Draw(img)
    
    # Add ticket-like shapes
    for i in range(4):
        x = 100 + i * 200
        y = size[1] // 2 - 40
        draw.rectangle([x, y, x+150, y+80], outline=(255, 255, 255, 80), width=2)
        draw.line([x+30, y, x+30, y+80], fill=(255, 255, 255, 80), width=1)
        draw.line([x+120, y, x+120, y+80], fill=(255, 255, 255, 80), width=1)
    
    return img

def create_celebrity_monitor_image(size=(800, 400)):
    """Create celebrity monitoring system image"""
    img = create_gradient_background(size[0], size[1], (79, 70, 229), (109, 40, 217))
    draw = ImageDraw.Draw(img)
    
    # Add social media-like elements
    for _ in range(6):
        x = randint(50, size[0]-150)
        y = randint(50, size[1]-150)
        size_rect = randint(80, 120)
        draw.rectangle([x, y, x+size_rect, y+size_rect], outline=(255, 255, 255, 80), width=2)
        draw.ellipse([x+10, y+10, x+40, y+40], outline=(255, 255, 255, 80), width=2)
    
    return img

def create_data_office_image(size=(800, 400)):
    """Create data office management image"""
    img = create_gradient_background(size[0], size[1], (6, 182, 212), (59, 130, 246))
    draw = ImageDraw.Draw(img)
    
    # Add graph-like elements
    points = [(100, 300), (200, 150), (300, 250), (400, 100), (500, 200), (600, 150)]
    for i in range(len(points)-1):
        draw.line([points[i], points[i+1]], fill=(255, 255, 255, 80), width=2)
        draw.ellipse([points[i][0]-5, points[i][1]-5, points[i][0]+5, points[i][1]+5], 
                    fill=(255, 255, 255))
    
    return img

def create_clipboard_manager_image(size=(800, 400)):
    """Create clipboard manager image"""
    img = create_gradient_background(size[0], size[1], (55, 65, 81), (31, 41, 55))
    draw = ImageDraw.Draw(img)
    
    # Add clipboard-like elements
    for i in range(4):
        x = 100 + i * 180
        y = 100
        draw.rectangle([x, y, x+150, y+200], outline=(255, 255, 255, 80), width=2)
        draw.rectangle([x+10, y+10, x+140, y+30], fill=(255, 255, 255, 30))
        draw.rectangle([x+10, y+40, x+140, y+60], fill=(255, 255, 255, 20))
        draw.rectangle([x+10, y+70, x+140, y+90], fill=(255, 255, 255, 10))
    
    return img

def create_border_center_image(size=(800, 400)):
    """Create border center management image"""
    img = create_gradient_background(size[0], size[1], (17, 24, 39), (55, 65, 81))
    draw = ImageDraw.Draw(img)
    
    # Add checkpoint-like elements
    for i in range(3):
        x = 150 + i * 250
        y = size[1] // 2 - 50
        draw.rectangle([x, y, x+200, y+100], outline=(255, 255, 255, 80), width=2)
        draw.line([x+50, y, x+50, y+100], fill=(255, 255, 255, 80), width=1)
        draw.line([x+150, y, x+150, y+100], fill=(255, 255, 255, 80), width=1)
    
    return img

def create_youtube_dl_image(size=(800, 400)):
    """Create YouTube downloader image"""
    img = create_gradient_background(size[0], size[1], (220, 38, 38), (185, 28, 28))
    draw = ImageDraw.Draw(img)
    
    # Add video player-like elements
    margin = 50
    draw.rectangle([margin, margin, size[0]-margin, size[1]-margin], 
                  outline=(255, 255, 255, 80), width=2)
    
    # Add play button
    center_x = size[0] // 2
    center_y = size[1] // 2
    draw.polygon([(center_x-30, center_y-40), (center_x+40, center_y), (center_x-30, center_y+40)], 
                outline=(255, 255, 255, 80), width=2)
    
    return img

# Create directory if it doesn't exist
projects_dir = 'f:/PythonII/TheZSolutions/app/static/img/projects'
os.makedirs(projects_dir, exist_ok=True)

# Generate project images
images = {
    'event-system.jpg': create_event_system_image,
    'celebrity-monitor.jpg': create_celebrity_monitor_image,
    'data-office.jpg': create_data_office_image,
    'clipboard-manager.jpg': create_clipboard_manager_image,
    'border-center.jpg': create_border_center_image,
    'youtube-dl.jpg': create_youtube_dl_image
}

for filename, create_func in images.items():
    file_path = os.path.join(projects_dir, filename)
    img = create_func()
    img.save(file_path, quality=95)
    print(f'Created {file_path}')
