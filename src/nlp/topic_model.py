from sklearn.feature_extraction.text import CountVectorizer
from src.nlp.preprocessing import preprocess
from bertopic import BERTopic
from hdbscan import HDBSCAN
from umap import UMAP
import re

def clean_abstract(text):
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\b\d+(\.\d+)?%?\b', '', text)
    text = re.sub(r'http\S+|doi:\S+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def build_topic_model():
    vectorizer = CountVectorizer(
        stop_words="english",
        min_df=2,
        ngram_range=(1, 2),
        token_pattern=r'[a-zA-Z]{3,}'
    )

    umap_model = UMAP(
    n_neighbors=10,
    n_components=5,
    min_dist=0.0,
    metric="cosine",
    random_state=42  # ← add this
    )

    hdbscan_model = HDBSCAN(
    min_cluster_size=10,  # ← down from 15
    min_samples=3,        # ← down from 5
    metric="euclidean",
    prediction_data=True
    )

    return BERTopic(
        vectorizer_model=vectorizer,
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        verbose=True
    )

def generate_label(keywords):
    generic_base = {"cells", "cell", "therapy", "patients", "tumor", "tumors", "treatment"}
    term_words = {w.lower() for w in term.replace("-", " ").split()}
    generic = generic_base | term_words

    seen = set()
    distinctive = []
    for k in keywords:
        words = set(k.lower().split())
        if not words & seen and k.lower() not in generic:
            distinctive.append(k)
            seen |= words

    top = distinctive[:2] if len(distinctive) >= 2 else keywords[:2]
    return " & ".join(k.title() for k in top)

def get_topics(abstracts, term=""):
    # Preprocess abstracts
    processed = [preprocess(text) for text in abstracts]

    model = build_topic_model()
    topics, probs = model.fit_transform(processed)

    topic_info = model.get_topic_info()  # ← this line was missing
    topic_info = topic_info[topic_info["Topic"] != -1]

    # Build generic terms from the search term itself + universal noise
    generic_base = {"cells", "cell", "therapy", "patients", "tumor", "tumors", "treatment"}
    term_words = {w.lower() for w in term.replace("-", " ").split()}
    generic = generic_base | term_words

    def generate_label(keywords):
        distinctive = [k for k in keywords if k.lower() not in generic]
        top = distinctive[:2] if len(distinctive) >= 2 else keywords[:2]
        return " & ".join(k.title() for k in top)

    topic_info["Label"] = topic_info["Representation"].apply(generate_label)

    return topic_info[["Topic", "Count", "Label", "Representation"]]
