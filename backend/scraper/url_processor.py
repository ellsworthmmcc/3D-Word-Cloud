from backend.scraper.scraper import scraper
from backend.scraper.processor import processor


async def url_processor(url: str) -> str | None:
    scraped_words = await scraper(url)

    # TODO add error handling
    if scraped_words is None:
        return None

    processed_words = await processor(words=scraped_words)

    return processed_words
