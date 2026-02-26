import asyncio
import itertools
import re
import json


# TODO Add NLP later
async def processor(words: list[str]) -> str:
    word_dict: dict[str, float] = {}

    for raw_words in words:
        # TODO fix regex
        processed_words: list[str] = re.findall(r'\b\w+\b', raw_words)
        for word in processed_words:
            if str.isnumeric(word):
                pass
            elif word in word_dict:
                word_dict[word] += 1
            else:
                word_dict[word] = 1

    sorted_word_dict = {k: v for k, v in sorted(word_dict.items(), key=lambda item: item[1], reverse=True)}
    shortened_word_dict = dict(itertools.islice(sorted_word_dict.items(), 50))

    return shortened_word_dict

    return json.dumps(shortened_word_dict, indent=4)
