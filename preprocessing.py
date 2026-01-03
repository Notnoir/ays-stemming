import nltk
import re
from stemming_ays import stemming_ays

nltk.download('punkt', quiet=True)

def load_stopwords():
    with open("stopwords_id.txt", "r", encoding="utf-8") as f:
        return set(f.read().splitlines())

STOPWORDS = load_stopwords()

def case_folding(text):
    return text.lower()

def tokenizing(text):
    return nltk.word_tokenize(text)

def filtering(tokens):
    return [t for t in tokens if t.isalpha() and t not in STOPWORDS]

def preprocess(text):
    """
    Preprocessing lengkap: case folding, tokenizing, filtering, dan stemming
    Returns: List of tuples (original_word, stemmed_word)
    """
    text = case_folding(text)
    tokens = tokenizing(text)
    filtered = filtering(tokens)
    
    # Return list of tuples: (original_word, stemmed_word)
    result = [(word, stemming_ays(word)) for word in filtered]
    return result
