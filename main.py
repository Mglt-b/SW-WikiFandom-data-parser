import os
import requests
from bs4 import BeautifulSoup
import re
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})

base_url = "https://summonerswar.fandom.com"

def get_full_url(path):
    """Construit une URL complète à partir d'un chemin relatif."""
    return base_url + path

# database txt / clean before
db = "db.txt"
db_awake = "db_awake.txt"

def load_existing_db(db_path):
    db = {}
    if os.path.exists(db_path):
        with open(db_path, 'r') as file:
            for line in file:
                name, element, speed = line.strip().split('; ')
                db[(name, element)] = speed
    return db

def parse_monster_name(img_name):
    """Extracts and returns the monster's name and element from the image name."""
    name_pattern = re.compile(r"(.+?)\s\((\w+)\)\sIcon\.png")
    match = name_pattern.match(img_name)
    if match:
        return match.group(1)
    return None

def parse_monster_name_awake(img_name):
    """Extracts and returns the monster's name and element from the image name."""
    name_pattern = re.compile(r"(.+?)\sIcon\.png")
    match = name_pattern.match(img_name)
    if match:
        return match.group(1)
    return None

def store_db(clean_name, element, speed, awake):
    print(element)
    if not awake:
        name = parse_monster_name(clean_name)
        with open(db, 'a') as file:
            file.write(f"{name}; {element}; {speed}\n")
    else:
        name = parse_monster_name_awake(clean_name)
        with open(db_awake, 'a') as file:
            file.write(f"{name}; {element}; {speed}\n")

def clean_filename(filename):
    """Cleans the filename to make it compatible with the file system."""
    return re.sub(r'[\\/*?:"<>|]', '_', filename)

def download_image(folder_path, img_url, clean_name, img_page_url):
    """Downloads an image after a short pause, if it does not already exist."""
    img_path = os.path.join(folder_path, clean_name)
    if not os.path.exists(img_path):
        try:
            time.sleep(.2)  # Respectful delay to avoid overloading the server
            response = requests.get(img_url, verify=False)
            with open(img_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {clean_name}")

        except Exception as e:
            print(f"Error downloading image {img_url}: {e}")
    else:
        print(f"{clean_name} already exists, skipping.")

def get_monster_speed(img_page_url):
    """Fetches and returns the speed of the monster from its page URL."""
    try:
        response = session.get(img_page_url, headers={'User-Agent': 'Mozilla/5.0'}, verify=False)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Utilisation d'une méthode plus générique pour trouver le texte "Speed:"
        # Ceci est une approche plus directe si le texte "Speed:" est bien dans un élément spécifique
        speed_info = soup.find(text=re.compile("Speed:"))
        if speed_info:
            # Tentative de localiser directement la valeur de la vitesse en se basant sur la structure observée
            # Cela pourrait nécessiter des ajustements selon la structure exacte de la page
            speed_value = speed_info.find_next().text.strip()
            print(f"Speed found: {speed_value}")  # Debug: Afficher la vitesse trouvée
            return speed_value
        else:
            print("Speed info not found.")
    except Exception as e:
        print(f"Error fetching monster speed from {img_page_url}: {e}")
    return 'N/A'


main_folder = "SummonersWarMonsters"
if not os.path.exists(main_folder):
    os.makedirs(main_folder)

urls = [
    "https://summonerswar.fandom.com/wiki/Fire_Monsters",
    "https://summonerswar.fandom.com/wiki/Water_Monsters",
    "https://summonerswar.fandom.com/wiki/Wind_Monsters",
    "https://summonerswar.fandom.com/wiki/Dark_Monsters",
    "https://summonerswar.fandom.com/wiki/Light_Monsters"
]

for url in urls:
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')

    element = url.split("/")[-1]
    element = element.replace("_Monsters", "")

    images = soup.find_all('img', {"data-image-name": re.compile("Icon\.png$")})
    
    folder_path = os.path.join(main_folder, element)
    os.makedirs(folder_path, exist_ok=True)

    dbvalues = load_existing_db("db.txt")
    dbawakevalues = load_existing_db("db_awake.txt")

    for img in images:
        img_name = img.get('data-image-name')
        img_url = img.get('data-src') or img.get('src')
        img_page_url0 = img.parent['href'] if img.parent.name == 'a' else ''  # Assuming the parent of <img> is <a> with the URL
        img_page_url = get_full_url(img_page_url0)

        clean_name = clean_filename(img_name)
        
        if img_url and not img_url.startswith('data:image') and ")" in img_name and not "Angelmon" in img_name and not "(Second" in img_name: #si non awake
            if element in img_name and not "(" in element:
                if not str(parse_monster_name(clean_name)) in str(dbvalues):
                    speed = get_monster_speed(img_page_url)
                    download_image(folder_path, img_url, clean_name, img_page_url)
                    store_db(clean_name, element, speed, False)

        if img_url and not img_url.startswith('data:image') and not ")" in img_name and not "Angelmon" in img_name and not "(Second" in img_name:      #si awake
            if not element in img_name:
                if not str(parse_monster_name_awake(clean_name)) in str(dbawakevalues):
                    speed = get_monster_speed(img_page_url)
                    download_image(folder_path, img_url, clean_name, img_page_url)
                    store_db(clean_name, element, speed, True)

print("Download completed.")
