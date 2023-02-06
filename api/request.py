import logging
import os
import requests
from dotenv import load_dotenv

load_dotenv()


def get_url_from_pastebin(result_json: str) -> str:
    """
    This function makes request with code to API Pastebin, return url
    """
    logger = logging.getLogger(__name__)

    url = os.getenv('API_URL_PASTEBIN')
    params = {
        'api_dev_key': os.getenv('API_DEV_KEY_PASTEBIN'),
        'api_option': 'paste',
        'api_paste_code': result_json,
    }

    try:
        request = requests.post(url=url, data=params)
        return request.text
    except requests.exceptions.RequestException as e:
        logger.error(e, exc_info=e)

print(get_url_from_pastebin('fdsfds'))