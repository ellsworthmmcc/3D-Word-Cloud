from backend.scraper.scraper import scraper
from backend.scraper.processor import processor


async def url_processor(url: str) -> dict[str, float] | None:
    scraped_words = await scraper(url)

    # TODO add error handling
    if scraped_words is None:
        return None

    processed_words: dict[str, float] = {}
    try:
        processed_words = await processor(words=scraped_words)
    except Exception as e:
        print(f"Unable to process article: {type(e).__name__}: {e}")
        return None

    return processed_words
