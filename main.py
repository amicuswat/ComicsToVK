import os
import random
from pathlib import Path
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

from vk_connector import get_vk_photos_upload_url
from vk_connector import save_photo_on_server
from vk_connector import send_photo_to_wall
from vk_connector import upload_photo_to_server

CURRENT_COMIC_URL = "https://xkcd.com/info.0.json"
DEFAULT_FOLDER = "Files"


def download_random_comic():
    response = requests.get(CURRENT_COMIC_URL)
    response.raise_for_status()

    comics_limit = response.json()['num']
    comic_num = random.randint(1, comics_limit)

    comic_url = f"https://xkcd.com/{comic_num}/info.0.json"

    response = requests.get(comic_url)
    response.raise_for_status()

    comic = response.json()

    img_url = comic['img']

    img_path = save_comic_img(img_url, DEFAULT_FOLDER)

    funny_comment = comic['alt']

    return funny_comment, img_path


def save_comic_img(url, folder=None):
    if not folder:
        folder = DEFAULT_FOLDER

    Path(folder).mkdir(parents=True, exist_ok=True)

    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    file_path = Path(folder, filename)

    response = requests.get(url)
    response.raise_for_status()

    with open(file_path, "wb") as file:
        file.write(response.content)

    return file_path


def main():
    load_dotenv()
    vk_access_token = os.environ['VK_ACCESS_TOKEN']

    group_id = os.environ['VK_GROUP_ID']

    funny_comment, comic_img_path = download_random_comic()

    try:
        photo_upload_url = get_vk_photos_upload_url(vk_access_token, group_id)

        upload_response = upload_photo_to_server(comic_img_path,
                                                 photo_upload_url)
    finally:
        os.remove(comic_img_path)

    _server = upload_response['server']
    _photo = upload_response['photo']
    _hash = upload_response['hash']

    save_response = save_photo_on_server(vk_access_token,
                                         group_id,
                                         _server,
                                         _photo,
                                         _hash)

    _owner_id = save_response['owner_id']
    _photo_id = save_response['id']

    send_photo_to_wall(vk_access_token, group_id, _owner_id, _photo_id,
                       funny_comment)


if __name__ == "__main__":
    main()
