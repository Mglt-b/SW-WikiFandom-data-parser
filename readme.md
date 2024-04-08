# Summoners War Monsters Image Scraper

This Python script is designed to automatically download monster images from the Summoners War game's monster collection, available on the Summoners War Wiki. The images are categorized by element (Fire, Water, Wind, Light, Dark) and saved in corresponding folders.

## How It Works

The script uses `requests` for making HTTP requests and `BeautifulSoup` for parsing the HTML of web pages. It downloads images whose file name contains "Icon.png" and organizes them into folders by element.

### Dependencies

- Python 3
- requests
- BeautifulSoup4

You can install the necessary dependencies via pip:

```bash
pip install requests beautifulsoup4
```

### Usage

1. Ensure all dependencies are installed.
2. Place the script in a directory of your choice.
3. Run the script:

```bash
python main.py
```

## Data Organization

The downloaded images are organized into folders by element, under the main folder `SummonersWarMonsters`. Each element folder contains the corresponding monsters' images and a `list{element}.txt` file that lists the names of the downloaded images.

Example of folder structure:

```
SummonersWarMonsters/
│
├── Fire/
│   ├── monster1.png
│   ├── monster2.png
│   └── listFire.txt
│
├── Water/
│   ├── monster1.png
│   ├── monster2.png
│   └── listWater.txt
│
... etc.
```

## Respect for the Website

To be respectful to the website and to avoid overloading its server, the script introduces a one-second delay between each image download.

## Note

This script is intended for educational and research purposes. Make sure you have permission to scrape the website and use the downloaded images in accordance with their terms of use.


This `README.md` provides a general overview of what the script does, how to install and run it, and an explanation of how the downloaded files are organized. 
Make sure to adjust the instructions and descriptions according to the specifics of your script and the exact dependencies.
