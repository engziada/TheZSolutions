import os

# Define the base directory
base_dir = 'f:/PythonII/TheZSolutions/app/static/img'

# Define the subdirectories
subdirs = ['projects', 'testimonials', 'team']

# Create directories
for subdir in subdirs:
    dir_path = os.path.join(base_dir, subdir)
    os.makedirs(dir_path, exist_ok=True)
    print(f'Created directory: {dir_path}')
