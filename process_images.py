import csv
import os
import sys
from pathlib import Path
from PIL import Image

CSV_FILE = sys.argv[1] if len(sys.argv) > 1 else 'optimisation_images_titabymtn.csv'
SOURCE_DIR = 'UP'
TARGET_DIR = 'NEWUP'

def parse_dimensions(dim_str):
    """
    Parses dimension strings like:
    - "400px largeur" -> (400, None)  (width, height)
    - "80x80px (160x160 retina)" -> (80, 80)
    """
    if not dim_str:
        return None, None
    
    dim_str = dim_str.lower().strip()
    
    if 'largeur' in dim_str:
        try:
            width = int(dim_str.split('px')[0].strip())
            return width, None
        except ValueError:
            return None, None
            
    if 'px' in dim_str:
        try:
            # Handle "80x80px..."
            parts = dim_str.split('px')[0].strip().split('x')
            if len(parts) >= 2:
                return int(parts[0]), int(parts[1])
        except ValueError:
            return None, None
            
    return None, None

def process_images():
    # Create target directory if it doesn't exist
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)

    with open(CSV_FILE, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            if row['Besoin de redimensionnement'] == 'Oui':
                original_path = row["Chemin de l'image"]
                recommended_dims = row['Dimensions recommandées']
                
                # 1. Convert path to use .webp extension and find in UP folder
                # original_path comes like /2022/11/asset1.png
                # We need UP/2022/11/asset1.webp
                
                path_obj = Path(original_path.lstrip('/')) # Remove leading slash
                webp_path = path_obj.with_suffix('.webp')
                full_source_path = os.path.join(SOURCE_DIR, webp_path)
                
                if not os.path.exists(full_source_path):
                    print(f"Warning: File not found: {full_source_path}")
                    continue
                
                # 2. Determine target path
                full_target_path = os.path.join(TARGET_DIR, webp_path)
                os.makedirs(os.path.dirname(full_target_path), exist_ok=True)
                
                # 3. Resize and save
                width, height = parse_dimensions(recommended_dims)
                
                try:
                    with Image.open(full_source_path) as img:
                        original_w, original_h = img.size
                        
                        target_w, target_h = original_w, original_h
                        
                        if width and height:
                            target_w, target_h = width, height
                        elif width:
                            # Calculate height to maintain aspect ratio
                            ratio = width / original_w
                            target_w = width
                            target_h = int(original_h * ratio)
                        
                        resized_img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
                        resized_img.save(full_target_path, 'WEBP')
                        print(f"Processed: {full_source_path} -> {full_target_path} ({target_w}x{target_h})")
                        
                except Exception as e:
                    print(f"Error processing {full_source_path}: {e}")

if __name__ == "__main__":
    process_images()
