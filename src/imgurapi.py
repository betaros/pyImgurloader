import shutil

import requests
import json
from pathlib import Path

from src import config


class ImgurAPI:

    def __init__(self):
        self.configuration = config.get_config()

    def get_infos(self, album_hash):
        url = f"https://api.imgur.com/3/album/{ album_hash }"

        payload = {}
        files = {}
        headers = {
            'Authorization': 'Client-ID ' + self.configuration['client_id']
        }

        response = requests.request("GET", url, headers=headers, data=payload, files=files)

        print(response.text)
        return response.text

    def get_images(self, album_hash):

        if Path(f"temp/{album_hash}").is_dir():
            return "Already exists"

        url = f"https://api.imgur.com/3/album/{ album_hash }/images"

        payload = {}
        files = {}
        headers = {
            'Authorization': 'Client-ID ' + self.configuration['client_id']
        }

        response = requests.request("GET", url, headers=headers, data=payload, files=files)

        images = json.loads(response.text)['data']
        print(images)

        Path('temp').mkdir(parents=True, exist_ok=True)
        Path(f"temp/{album_hash}").mkdir(parents=True, exist_ok=True)

        counter = 0
        for image in images:
            image_name = f"temp/{album_hash}/{counter}_{image['id']}.jpg"
            self.download_images(image['link'], image_name)
            counter = counter + 1

        self.generate_meta_data(album_hash)

        return "Downloaded"

    def download_images(self, image, name):
        r = requests.get(image, stream=True)

        # Check if the image was retrieved successfully
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True

            # Open a local file with wb ( write binary ) permission.
            with open(name, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

            print('Image sucessfully Downloaded: ', name)
        else:
            print('Image Couldn\'t be retreived')

    def generate_meta_data(self, album_hash):
        infos = self.get_infos(album_hash)

        with open(f"temp/{album_hash}/meta.json", 'w') as meta_file:
            json.dump(infos, meta_file, indent=2)
