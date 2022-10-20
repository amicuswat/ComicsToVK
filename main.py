import os
import random

import requests
from dotenv import load_dotenv

from files_processing import get_all_files, load_and_save_files

CURRENT_COMMICS_URL = "https://xkcd.com/info.0.json"
BASE_VK_UPI_URL = 'https://api.vk.com/method/'

VK_METHODS = {
        'get_groups': 'groups.get',
        'photos_get_wall_upload_server': 'photos.getWallUploadServer',
        'save_photos': 'photos.saveWallPhoto',
        'wall_post': 'wall.post'
    }


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


def upload_photo_to_server(photo_path, upload_url):
    with open(photo_path, "rb") as file:
        files = {
            "photo": file
        }

        response = requests.post(upload_url, files=files)
        response.raise_for_status()

    return response.json()


def save_photo_on_server(vk_access_token, group_id, upload_response):
    params = {
        'access_token': vk_access_token,
        'v': '5.131',
        'group_id': group_id,
        'server': upload_response['server'],
        'photo': upload_response['photo'],
        'hash': upload_response['hash']
    }

    url_with_method = f"{BASE_VK_UPI_URL}" \
                      f"{VK_METHODS['save_photos']}"

    response = requests.get(url_with_method, params=params)
    response.raise_for_status()

    return response.json()['response'][0]


def send_comics_to_wall(vk_access_token, group_id, save_response, funny_comment):
    attachment = f"photo{save_response['owner_id']}_{save_response['id']}"

    params = {
        'access_token': vk_access_token,
        'v': '5.131',
        'owner_id': -int(group_id),
        'attachments': attachment,
        'from_group': 1,
        'message': funny_comment
    }

    url_with_method = f"{BASE_VK_UPI_URL}" \
                      f"{VK_METHODS['wall_post']}"

    response = requests.post(url_with_method, params=params)
    response.raise_for_status()

    return response.json()


def get_num_of_comics():
    response = requests.get(CURRENT_COMMICS_URL)
    response.raise_for_status()

    return response.json()['num']


def load_random_comics():
    comics_limit = get_num_of_comics()
    comics_to_upload = random.randint(1, comics_limit)

    comics_url = f"https://xkcd.com/{comics_to_upload}/info.0.json"

    response = requests.get(comics_url)
    response.raise_for_status()

    comics = response.json()

    img_url = comics['img']
    load_and_save_files(img_url)

    funny_comment = comics['alt']

    return funny_comment


def main():
    load_dotenv()
    vk_access_token = os.environ['VK_ACCESS_TOKEN']

    group_id = os.environ['VK_GROUP_ID']''

    funny_comment = load_random_comics()
    comics_path = get_all_files("Files").pop()

    photo_upload_url = get_vk_photos_upload_url(vk_access_token, group_id)
    upload_response = upload_photo_to_server(comics_path, photo_upload_url)
    save_response = save_photo_on_server(vk_access_token,
                                         group_id,
                                         upload_response)
    send_comics_to_wall(vk_access_token,
                        group_id,
                        save_response,
                        funny_comment)

    os.remove(comics_path)


if __name__ == "__main__":
    main()
