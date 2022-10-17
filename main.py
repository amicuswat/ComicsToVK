import requests

from files_processing import load_and_save_files

CURRENT_COMMICS_URL = "https://xkcd.com/info.0.json"

# specific commics url
# https://xkcd.com/614/info.0.json


def main():
    response = requests.get(CURRENT_COMMICS_URL)
    response.raise_for_status()

    img_url = response.json()['img']
    load_and_save_files(img_url)


if __name__ == "__main__":
    main()