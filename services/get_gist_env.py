import requests
from functools import lru_cache


def fetch_gist_file(url):
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()
