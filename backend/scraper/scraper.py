import asyncio
import re

from bs4 import BeautifulSoup
import requests


async def scraper(url: str) -> list[str] | None:
    '''Attempts to pull all words from a given url'''
    # Helps to fake being a proper user to a website
    HEADERS = {
      "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
      "accept": "*/*",
      "accept-language": "en-US",
      "accept-encoding": "gzip, deflate, br, zstd",
    }

    soup: BeautifulSoup | None = None

    try:
        soup = BeautifulSoup(
            markup=requests.get(url, headers=HEADERS, timeout=10).text,
            features="html.parser"
        )
    except (requests.exceptions.RequestException) as e:
        print(f"Error during request for: {url},\n{e}")
        return None

    words: list[str] = []

    for el in soup.find_all(['div', 'article', 'p',]):
        raw_text: str = str.lower(el.text)
        words.append(raw_text)

    return words
