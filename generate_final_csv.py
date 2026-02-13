import csv
import os
import sys
from pathlib import Path

CSV_FILE = sys.argv[1] if len(sys.argv) > 1 else 'optimisation_images_titabymtn.csv'
OUTPUT_CSV = 'final_images_paths.csv'
OUTPUT_URL_CSV = 'final_images_urls.csv'
UP_DIR = 'UP'
NEWUP_DIR = 'NEWUP'
URL_PREFIX = 'https://titabymtn.bj/wp-content/uploads/'

def get_webp_path(original_path):
    # Remove leading slash if present and replace extension with .webp
    path_obj = Path(original_path.lstrip('/'))
    return path_obj.with_suffix('.webp')

def main():
    print(f"Generating {OUTPUT_CSV} and {OUTPUT_URL_CSV}...")
    
    with open(CSV_FILE, 'r', encoding='utf-8') as infile, \
         open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as outfile, \
         open(OUTPUT_URL_CSV, 'w', newline='', encoding='utf-8') as url_outfile:
        
        reader = csv.DictReader(infile)
        writer = csv.writer(outfile)
        url_writer = csv.writer(url_outfile)
        
        writer.writerow(['image path', 'Has been resizing'])
        url_writer.writerow(['image url', 'Has been resizing'])
        
        count = 0
        
        for row in reader:
            original_path = row["Chemin de l'image"]
            resize_needed = row['Besoin de redimensionnement']
            
            # Map French Oui/Non to Yes/No
            has_been_resized = 'Yes' if resize_needed == 'Oui' else 'No'
            
            webp_relative_path = get_webp_path(original_path)
            
            # Now all images should be in NEWUP
            candidate_path = os.path.join(NEWUP_DIR, webp_relative_path)
            
            # Generate URL (replace NEWUP/ with URL_PREFIX)
            # candidate_path is like NEWUP/2022/11/image.webp
            # We want https://titabymtn.bj/wp-content/uploads/2022/11/image.webp
            # We can simply replace the prefix or construct from webp_relative_path
            image_url = URL_PREFIX + str(webp_relative_path)
            
            if os.path.exists(candidate_path):
                writer.writerow([candidate_path, has_been_resized])
                url_writer.writerow([image_url, has_been_resized])
                count += 1
            else:
                print(f"Warning: File not found in NEWUP: {candidate_path}")
                # Write the expected NEWUP path even if missing, as per previous logic/request consistency
                writer.writerow([candidate_path, has_been_resized])
                url_writer.writerow([image_url, has_been_resized])
                count += 1

                
    print(f"Done. Wrote {count} paths/urls to {OUTPUT_CSV} and {OUTPUT_URL_CSV}.")

if __name__ == '__main__':
    main()
