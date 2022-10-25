
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

