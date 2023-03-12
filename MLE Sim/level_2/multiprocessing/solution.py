
import re
from string import punctuation
from joblib import Parallel, delayed

import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


def clear_text(text: str) -> list:
    """
    Clear text

    Parameters
    ----------
    text : str
        Path to process

    Returns
    -------
    list
        List of cleared strings
    """
    lemmatizer = WordNetLemmatizer()

    cleaned_text_list = []

    text = str(text)
    text = re.sub(r"https?://[^,\s]+,?", "", text)
    text = re.sub(r"@[^,\s]+,?", "", text)

    stop_words = stopwords.words("english")
    transform_text = text.translate(str.maketrans("", "", punctuation))
    transform_text = re.sub(" +", " ", transform_text)

    text_tokens = word_tokenize(transform_text)

    lemma_text = [
        lemmatizer.lemmatize(word.lower()) for word in text_tokens
    ]
    cleaned_text = " ".join(
        [str(word) for word in lemma_text if word not in stop_words])

    cleaned_text_list.append(cleaned_text)
    return cleaned_text_list


def clear_data(source_path: str, target_path: str, n_jobs: int):
    """Baseline process df

    Parameters
    ----------
    source_path : str
        Path to load dataframe from

    target_path : str
        Path to save dataframe to

    n_jobs : int
        Count of job to process
    """
    data = pd.read_parquet(source_path)
    data = data.copy().dropna().reset_index(drop=True)

    cleaned_text_list = Parallel(
        n_jobs=-1, backend='multiprocessing')(delayed(clear_text)(text) for text in data['text'])

    data["cleaned_text"] = cleaned_text_list
    data.to_parquet(target_path)
