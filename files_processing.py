import os
import random
from urllib.parse import urlparse


def get_file_extention(url):
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    filename, extention = os.path.splitext(filename)

    return extention


def get_filename(url, folder):
    # todo - If no Folder create it
    # todo - Generate file name

    file_extention = get_file_extention(url)
    filename = f"{file_extention}"
    return filename


def load_and_save_files(url, folder=None):
    filename = get_filename(url, folder)

    # todo - Fetch image
    # todo - Save image
