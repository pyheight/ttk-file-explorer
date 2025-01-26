import os  
import base64  
from pathlib import Path


def b64encode_image(image_path):  
    with open(image_path, 'rb') as image_file:  
        encoded = base64.b64encode(image_file.read()).decode('utf-8')  
    return encoded  
  

def process_images(folder_path):  
    seen_categories = set()  
    for subfolder_name, subfolders, files in os.walk(folder_path):  
        if not subfolders and not files:  
            continue  

        if subfolder_name not in seen_categories:  
            print(f"\n{subfolder_name}\n")  
            seen_categories.add(subfolder_name)  

        for file in files:  
            if not file.endswith(('.gif', '.ico')): 
                image_path = Path(subfolder_name) / file  
                image_name = image_path.stem 
                encoded = b64encode_image(image_path)  
                print(f"'{image_name}': '{encoded}',")


if __name__ == '__main__':
    process_images('./images/')
