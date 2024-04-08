import os
import requests
from bs4 import BeautifulSoup
import re
import time

# database txt / clean before
db = "db.txt"
with open(db, 'w') as file:
    file.write("")

def parse_monster_name(img_name):
    """Extracts and returns the monster's name and element from the image name."""
    name_pattern = re.compile(r"(.+?)\s\((\w+)\)\sIcon\.png")
    match = name_pattern.match(img_name)
    if match:
        return match.group(1)
    return None

def store_db(clean_name, element):
    name = parse_monster_name(clean_name)

    with open(db, 'a') as file:
        file.write(f"{name}; {element}\n")

def clean_filename(filename):
    """Cleans the filename to make it compatible with the file system."""
    return re.sub(r'[\\/*?:"<>|]', '_', filename)

def download_image(folder_path, img_url, clean_name):
    """Downloads an image after a short pause, if it does not already exist."""
    
    img_path = os.path.join(folder_path, clean_name)
    if not os.path.exists(img_path):
        try:
            time.sleep(.5)  # Respectful delay to avoid overloading the server
            response = requests.get(img_url, verify=False)
            with open(img_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {clean_name}")
        except Exception as e:
            print(f"Error downloading image {img_url}: {e}")
    else:
        print(f"{clean_name} already exist, skip")

main_folder = "SummonersWarMonsters"
if not os.path.exists(main_folder):
    os.makedirs(main_folder)

urls = [
    "https://summonerswar.fandom.com/wiki/Monster_Collection#Fire",
    "https://summonerswar.fandom.com/wiki/Monster_Collection#Water",
    "https://summonerswar.fandom.com/wiki/Monster_Collection#Wind",
    "https://summonerswar.fandom.com/wiki/Monster_Collection#Light",
    "https://summonerswar.fandom.com/wiki/Monster_Collection#Dark",
]

for url in urls:
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    element = url.split("#")[-1]
    images = soup.find_all('img', {"data-image-name": re.compile("Icon\.png$")})
    
    folder_path = os.path.join(main_folder, element)
    os.makedirs(folder_path, exist_ok=True)

    for img in images:
        img_name = img.get('data-image-name')
        img_url = img.get('data-src') or img.get('src')

        if img_url and not img_url.startswith('data:image') and ")" in img_name and not "Angelmon" in img_name and not "(Second" in img_name:
            if element in img_name:
                clean_name = clean_filename(img_name)
                store_db(clean_name, element)
                download_image(folder_path, img_url, clean_name)

print("Download completed.")
