from bs4 import BeautifulSoup
import httpx


async def scraper(url: str) -> list[str] | None:
    '''Attempts to pull all words from a given url'''
    HEADERS = {
        "user-agent": "3DWordCloud/1.0 (https://github.com/ellsworthmmcc/3d-word-cloud-ellsworth; bot-traffic@wikimedia.org) httpx/0.28.0",
        "accept": "*/*",
        "accept-language": "en-US",
        "accept-encoding": "gzip, deflate, br, zstd",
    }

    try:
        async with httpx.AsyncClient(verify=True, follow_redirects=True) as client:
            response = await client.get(url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(
                markup=response.text,
                features="html.parser"
            )
    except httpx.RequestError as e:
        print(f"Error during request for: {url},\n{e}")
        return None

    words: list[str] = []

    for raw_text in soup.find_all(['span', 'p',]):
        words.append(raw_text.text)

    return words
