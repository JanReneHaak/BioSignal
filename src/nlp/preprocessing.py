import re
import spacy

nlp = spacy.load("en_core_web_sm")

def clean_abstract(text: str) -> str:
    """Remove HTML, numbers, URLs and normalize whitespace."""

    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove numbers and percentages
    text = re.sub(r'\b\d+(\.\d+)?%?\b', '', text)
    # Remove DOIs and URLs
    text = re.sub(r'http\S+|doi:\S+', '', text, flags=re.IGNORECASE)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def lemmatize(text: str) -> str:
    """Lemmatize text and remove stopwords and punctuation using spaCy."""

    doc = nlp(text)
    tokens = [
        token.lemma_.lower() for token in doc
        if not token.is_stop
        and not token.is_punct
        and len(token.text) > 2
    ]

    return " ".join(tokens)


def preprocess(text: str) -> str:
    """Full preprocessing pipeline: clean then lemmatize."""

    return lemmatize(clean_abstract(text))
