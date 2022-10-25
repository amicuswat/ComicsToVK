import requests

BASE_VK_UPI_URL = 'https://api.vk.com/method/'


def get_vk_photos_upload_url(vk_access_token, group_id):
    vk_method = "photos.getWallUploadServer"

    params = {
        'access_token': vk_access_token,
        'v': '5.131',
        'group_id': group_id
    }

    url_with_method = f"{BASE_VK_UPI_URL}" \
                      f"{vk_method}"

    response = requests.get(url_with_method, params=params)
    response.raise_for_status()

    upload_url = response.json()['response']['upload_url']

    return upload_url


def upload_photo_to_server(photo_path, upload_url):
    with open(photo_path, "rb") as file:
        files = {
            "photo": file
        }

        response = requests.post(upload_url, files=files)
        response.raise_for_status()

    return response.json()


def save_photo_on_server(vk_access_token, group_id, upload_response):
    vk_method = "photos.saveWallPhoto"

    params = {
        'access_token': vk_access_token,
        'v': '5.131',
        'group_id': group_id,
        'server': upload_response['server'],
        'photo': upload_response['photo'],
        'hash': upload_response['hash']
    }

    url_with_method = f"{BASE_VK_UPI_URL}" \
                      f"{vk_method}"

    response = requests.get(url_with_method, params=params)
    response.raise_for_status()

    return response.json()['response'][0]


def send_comics_to_wall(vk_access_token, group_id, save_response, funny_comment):
    vk_method = "wall.post"

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
                      f"{vk_method}"

    response = requests.post(url_with_method, params=params)
    response.raise_for_status()

    return response.json()

