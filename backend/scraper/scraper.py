import asyncio
import re

from bs4 import BeautifulSoup
import requests


async def scraper(url: str) -> dict[str] | None:
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
            markup=requests.get(url, headers=HEADERS).text,
            features="html.parser")
    except (requests.exceptions.RequestException) as e:
        print(f"Error during request for: {url},\n{e}")
        return None

    word_dict: dict[str] = {}

    for el in soup.find_all('div'):
        raw: str = str.lower(el.text)
        words: list[str] = re.findall(r'\b\w+\b', raw)
        for word in words:

            if word in word_dict:
                word_dict[word] += 1
            else:
                word_dict[word] = 1

    return word_dict


if __name__ == '__main__':
    example_url = 'https://en.wikipedia.org/wiki/Gilgamesh'

    res = asyncio.get_event_loop().run_until_complete(scraper(url=example_url))
