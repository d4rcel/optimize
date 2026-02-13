import csv
import os
import shutil
from pathlib import Path

CSV_FILE = 'optimisation_images_titabymtn.csv'
UP_DIR = 'UP'
NEWUP_DIR = 'NEWUP'

def get_webp_path(original_path):
    path_obj = Path(original_path.lstrip('/'))
    return path_obj.with_suffix('.webp')

def main():
    print("Copying non-resized images to NEWUP...")
    
    with open(CSV_FILE, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        
        count = 0
        
        for row in reader:
            if row['Besoin de redimensionnement'] == 'Non':
                original_path = row["Chemin de l'image"]
                webp_relative_path = get_webp_path(original_path)
                
                source_path = os.path.join(UP_DIR, webp_relative_path)
                target_path = os.path.join(NEWUP_DIR, webp_relative_path)
                
                if os.path.exists(source_path):
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    shutil.copy2(source_path, target_path)
                    print(f"Copied: {source_path} -> {target_path}")
                    count += 1
                else:
                    # Fallback logic: Try to find the file
                    filename = os.path.basename(webp_relative_path)
                    
                    # 1. Recursive search for exact filename
                    found_path = None
                    for root, dirs, files in os.walk(UP_DIR):
                        if filename in files:
                            found_path = os.path.join(root, filename)
                            break
                    
                    # 2. Heuristic: Remove '-scaled' if present
                    if not found_path and '-scaled' in filename:
                        clean_name = filename.replace('-scaled', '')
                        # Search for clean name
                        for root, dirs, files in os.walk(UP_DIR):
                            if clean_name in files:
                                found_path = os.path.join(root, clean_name)
                                break
                                
                    # 3. Heuristic: Try Dv.webp for Dv-scaled.webp (prefix match)
                    if not found_path and filename.startswith('Dv'):
                         # Specific check for Dv.*
                         for root, dirs, files in os.walk(UP_DIR):
                            if 'Dv.webp' in files:
                                found_path = os.path.join(root, 'Dv.webp')
                                break

                    if found_path:
                        print(f"Found alternative for {filename}: {found_path}")
                        os.makedirs(os.path.dirname(target_path), exist_ok=True)
                        shutil.copy2(found_path, target_path)
                        print(f"Copied alternative: {found_path} -> {target_path}")
                        count += 1
                    else:
                        print(f"Warning: Source file not found even after search: {source_path}")


    print(f"Done. Copied {count} files.")

if __name__ == '__main__':
    main()
