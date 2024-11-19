#!/usr/bin/env python3
import base64
import requests
import subprocess
import os
import time
import logging
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, filename='camera.log', format='%(asctime)s %(message)s')

# Environment Variables
PICTURE_DIR = os.path.join("/", "home", "Prusacam")
FILENAME = os.path.join(PICTURE_DIR, "image.jpg")
FINGERPRINT = os.getenv("70da3c685d1b714f587a25b034ca1414171c621d")
TOKEN = os.getenv("Ag9AUEPuDOA9VV4AoedN")
UPLOAD_URL = "https://webcam.connect.prusa3d.com/c/snapshot"

# Ensure directory exists
os.makedirs(PICTURE_DIR, exist_ok=True)

def get_image():
    if os.path.exists(FILENAME):
        os.remove(FILENAME)
        logging.info(f"{FILENAME} removed successfully.")
    
    subprocess.run([
        "libcamera-still", 
        "--autofocus-mode", "continuous", 
        "--hdr", "sensor", 
        "--hflip", "1", 
        "--vflip", "1", 
        "-o", FILENAME
    ])

def read_data(filepath):
    if not os.path.exists(filepath):
        logging.warning(f"{filepath} does not exist.")
        return b""
    with open(filepath, 'rb') as file:
        return file.read()

def main():
    try:
        while True:
            get_image()
            snapshot = read_data(FILENAME)
            if not snapshot:
                continue

            headers = {
                "content-type": "image/jpg",
                "fingerprint": FINGERPRINT,
                "token": TOKEN,
            }

            retry = True
            while retry:
                try:
                    response = requests.put(UPLOAD_URL, headers=headers, data=snapshot, timeout=10)
                    logging.info(f"HTTP Response Code: {response.status_code}")
                    if response.status_code == 200:
                        os.remove(FILENAME)
                        logging.info("Image uploaded and removed successfully.")
                    retry = False
                except requests.exceptions.RequestException as e:
                    logging.error(f"Connection error: {e}")
                    logging.info("Retrying in 60 seconds...")
                    time.sleep(60)

            time.sleep(10)
    except KeyboardInterrupt:
        logging.info("Script interrupted. Exiting gracefully.")

if __name__ == "__main__":
    main()
