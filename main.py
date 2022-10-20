import os

import requests
from dotenv import load_dotenv

from files_processing import load_and_save_files

CURRENT_COMMICS_URL = "https://xkcd.com/info.0.json"

BASE_VK_UPI_URL = 'https://api.vk.com/method/'

VK_METHODS = {
        'get_groups': 'groups.get',
        'photos_get_wall_upload_server': 'photos.getWallUploadServer'
    }

# specific commics url
# https://xkcd.com/614/info.0.json


def get_vk_photos_upload_url(vk_access_token, group_id):
    params = {
        'access_token': vk_access_token,
        'v': '5.131',
        'group_id': group_id
    }

    url_with_method = f"{BASE_VK_UPI_URL}" \
                      f"{VK_METHODS['photos_get_wall_upload_server']}"

    response = requests.get(url_with_method, params=params)
    response.raise_for_status()

    server_serialized = response.json()['response']

    return server_serialized['upload_url']


def load_random_comics():
    response = requests.get(CURRENT_COMMICS_URL)
    response.raise_for_status()

    comics = response.json()

    img_url = comics['img']
    load_and_save_files(img_url)

    funny_comment = comics['alt']

    print(funny_comment)


def main():
    load_dotenv()
    vk_access_token = os.environ['VK_ACCESS_TOKEN']

    group_id = '216541309'

    photo_upload_url = get_vk_photos_upload_url(vk_access_token, group_id)



if __name__ == "__main__":
    main()