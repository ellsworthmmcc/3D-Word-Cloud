from itertools import islice
import re

from bertopic import BERTopic

# Removes need for nltk
STOPWORDS = {
    "i", "me", "my", "myself", "we", "our",
    "ours", "ourselves", "you", "your", "yours", "yourself",
    "yourselves", "he", "him", "his", "himself", "she", "her",
    "hers", "herself", "it", "its", "itself", "they", "them",
    "their", "theirs", "themselves", "what", "which", "who",
    "whom", "this", "that", "these", "those", "am", "is", "are",
    "was", "were", "be", "been", "being", "have", "has", "had",
    "having", "do", "does", "did", "doing", "a", "an", "the",
    "and", "but", "if", "or", "because", "as", "until", "while",
    "of", "at", "by", "for", "with", "about", "against", "between",
    "into", "through", "during", "before", "after", "above", "below",
    "to", "from", "up", "down", "in", "out", "on", "off", "over",
    "under", "again", "further", "then", "once", "here", "there",
    "when", "where", "why", "how", "all", "any", "both", "each",
    "few", "more", "most", "other", "some", "such", "no", "nor",
    "not", "only", "own", "same", "so", "than", "too", "very",
    "s", "t", "can", "will", "just", "don", "should", "now"
}


async def preprocessing(words: list[str]) -> list[str]:

    processed_words: list[str] = []
    for raw_words in words:
        sentence = re.findall(r"\b[a-zA-Z]{2,}\b", raw_words)

        processed_sentence: str = ''
        for word in sentence:
            if str.strip(word) not in STOPWORDS:
                processed_sentence += word + ' '

            if len(processed_sentence) > 100:
                processed_words.append(processed_sentence)
                processed_sentence = ''

        if processed_sentence:
            processed_words.append(processed_sentence)

    return processed_words


async def normalization(word_scores: dict[str, float]) -> dict[str, float]:
    values = word_scores.values()
    min_val = min(values)
    max_val = max(values)

    # prevent division by 0
    if max_val == min_val:
        return {word: 1.0 for word in word_scores}

    return {
        word: (val - min_val) / (max_val - min_val)
        for word, val in word_scores.items()
    }


async def processor(words: list[str]) -> dict[str, float]:

    processed_words = await preprocessing(words)

    topic_model = BERTopic(verbose=False)
    topic_model.fit_transform(processed_words)

    word_scores: dict[str, float] = {}
    topic_info = topic_model.get_topic_info()

    for topic_id in topic_info.Topic:
        # -1 is outliers, no reason to include
        if topic_id == -1:
            continue

        topic_words = topic_model.get_topic(topic_id)
        for word, score in topic_words:
            if not word:
                continue
            if word in word_scores:
                word_scores[word] += score
            else:
                word_scores[word] = score

    positive_word_scores = {
        word: score for word,
        score in word_scores.items()
        if score > 0
    }

    sorted_word_scores = {
        word: flo for word, flo in sorted(
            positive_word_scores.items(), key=lambda item: item[1], reverse=True
        )
    }

    sliced_word_scores = dict(islice(sorted_word_scores.items(), 64))

    normalized_word_scores: dict[str, float] = await normalization(word_scores=sliced_word_scores)

    return normalized_word_scores
