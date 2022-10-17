import os
import random
from urllib.parse import urlparse
from pathlib import Path

import requests

DEFAULT_FOLDER = "Files"


def get_file_extention(url):
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    filename, extention = os.path.splitext(filename)

    return extention


def get_filename(url, folder):

    if not folder:
        folder = DEFAULT_FOLDER

    Path(folder).mkdir(parents=True, exist_ok=True)

    name_hash = random.getrandbits(128)
    filename = "%032x" % name_hash

    file_extention = get_file_extention(url)

    filename = f"{filename}{file_extention}"
    filename = Path(folder, filename)

    return filename


def load_and_save_files(url, folder=None):
    filename = get_filename(url, folder)

    response = requests.get(url)
    response.raise_for_status()

    with open(filename, "wb") as file:
        file.write(response.content)
