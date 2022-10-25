from http.client import HTTPException

import requests

BASE_VK_API_URL = 'https://api.vk.com/method/'


class VKException(Exception):
    pass


def check_for_error(response):
    unpacked_response = response.json()
    if 'error' in response.json():
        raise VKException(unpacked_response['error']['error_msg'])


def get_vk_photos_upload_url(vk_access_token, group_id):
    vk_method = "photos.getWallUploadServer"

    params = {
        'access_token': vk_access_token,
        'v': '5.131',
        'group_id': group_id
    }

    api_endpoint = f"{BASE_VK_API_URL}{vk_method}"

    response = requests.get(api_endpoint, params=params)
    response.raise_for_status()
    check_for_error(response)

    upload_url = response.json()['response']['upload_url']

    return upload_url


def upload_photo_to_server(photo_path, upload_url):
    with open(photo_path, "rb") as file:
        files = {
            "photo": file
        }
        response = requests.post(upload_url, files=files)

    response.raise_for_status()
    check_for_error(response)

    return response.json()


def save_photo_on_server(vk_access_token, group_id, _server, _photo, _hash):
    vk_method = "photos.saveWallPhoto"

    params = {
        'access_token': vk_access_token,
        'v': '5.131',
        'group_id': group_id,
        'server': _server,
        'photo': _photo,
        'hash': _hash
    }

    api_endpoint = f"{BASE_VK_API_URL}{vk_method}"

    response = requests.get(api_endpoint, params=params)
    response.raise_for_status()
    check_for_error(response)

    return response.json()['response'][0]


def send_photo_to_wall(vk_access_token, group_id, _owner_id, _photo_id, funny_comment):
    vk_method = "wall.post"

    attachment = f"photo{_owner_id}_{_photo_id}"

    params = {
        'access_token': vk_access_token,
        'v': '5.131',
        'owner_id': -int(group_id),
        'attachments': attachment,
        'from_group': 1,
        'message': funny_comment
    }

    api_endpoint = f"{BASE_VK_API_URL}{vk_method}"

    response = requests.post(api_endpoint, params=params)
    response.raise_for_status()
    check_for_error(response)

    return response.json()
