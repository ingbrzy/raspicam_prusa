#!/usr/bin/env python3
import base64
import requests
import subprocess
import os
import time

picturedir = os.path.join("/", "home", "Prusacam")
filename = os.path.join(picturedir, "image.jpg")

if not os.path.exists(picturedir):
    os.mkdir(picturedir)

def atob(base64_string):
    return base64.b64decode(base64_string)

def get_image():
    # Check if the file exists
    if os.path.exists(filename):
    # Remove the file
        os.remove(filename)
        print(f"{filename} removed successfully.")
    else:
        print(f"{filename} does not exist.")
    
    subprocess.run(["libcamera-still", "--autofocus-mode", "continuous", "--hdr", "sensor", "-o", os.path.join(picturedir, "image.jpg")])

def read_data(fpath):
    if not os.path.exists(fpath):
        return b""
    with open(fpath, 'rb') as file:
        data = file.read()
    return data

def main():
    while True:
        get_image()
        filename = os.path.join(picturedir, "image.jpg")
        snapshot = read_data(filename)
        if snapshot == b"":
            continue
        url = "https://webcam.connect.prusa3d.com/c/snapshot"
        headers = {
            "content-type": "image/jpg",
            "fingerprint": "70da3c685d1b714f587a25b034ca1414171c621d",  # replace with your fingerprint
            "token": "zQoBQiHc24SJSQbjEFTb",  # replace with your token
        }

        retry = True
        while retry:
            try:
                response = requests.put(url, headers=headers, data=snapshot)
                print(response.status_code)
                if response.status_code == 200:
                    os.remove(filename)
                retry = False
            except requests.exceptions.RequestException as e:
                print("Connection error:", e)
                print("Retrying in 60 seconds...")
                time.sleep(60)

        time.sleep(10)

if __name__ == "__main__":
    main()
