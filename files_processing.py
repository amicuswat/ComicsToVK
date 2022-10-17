import os
import random
from urllib.parse import urlparse
from pathlib import Path


def get_file_extention(url):
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    filename, extention = os.path.splitext(filename)

    return extention


def get_filename(url, folder):
    default_folder = "Files"

    if not folder:
        folder = default_folder

    Path(folder).mkdir(parents=True, exist_ok=True)

    name_hash = random.getrandbits(128)
    filename = "%032x" % name_hash

    file_extention = get_file_extention(url)

    filename = f"{filename}{file_extention}"
    filename = Path(folder, filename)

    return filename


def load_and_save_files(url, folder=None):
    filename = get_filename(url, folder)
    print(filename)

    # todo - Fetch image
    # todo - Save image
