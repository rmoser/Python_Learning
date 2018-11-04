from pathlib import Path
import io
import collections as coll
import nltk
import nltk.stem
import urllib.request
import re
from bs4 import BeautifulSoup
from unidecode import unidecode
import os
import codecs
import string
import numpy as np
import pandas as pd

# Store out folder as module variable for now
os.chdir(r"F:\Users\Bob\Documents\Git\Python_Learning\MIT Data Science\Case Study 1.1.2  LDA")
data = Path("./Data")
out = Path("./temp")

# Ensure the folders exist
if not data.exists():
    data.mkdir()

if not out.exists():
    out.mkdir()

def read_data(file):
    text = ""  # Init return value if fail

    if not Path(file).exists():
        print("ERROR: File not found: {}".format(file))
        return text

    with open(file) as f:
        text = ''.join(f.readlines())

    return text


def read_soup(file):
    f = Path(file)

    if not f.exists():
        print("ERROR: File not found: {}".format(file))
        raise FileExistsError

    return BeautifulSoup(f.read_text('utf-8'), "html.parser", )


def get_MIT_faculty_list():

    # Use the downloaded html file if it exists
    file = "Faculty.html"

    # data is a global Path object pointing to the Data sub folder
    f = data.joinpath(file)
    if f.exists():
        # Path.stem is the filename with no extension
        # Which is exactly the professor's name
        # Replace '_' with ' ' so the data is the same, regardless of which source was used
        soup = read_soup(f)

    else:
        # Otherwise, scrape the list from the MIT EECS faculty web site
        url = r'https://www.eecs.mit.edu/people/faculty-advisors'

        # Read the full HTML of the site
        text = urllib.request.urlopen(url).read()

        # Parse with BeautifulSoup
        soup = BeautifulSoup(text, 'html.parser')

    # Prof names are in views-field views-field-title
    # Then remove all whitespace and
    #   downgrade all chars to simple A-Za-z,
    #   since we know that will work as input to the abstract search engine
    names = [unidecode(t.text.strip()) for t in soup.find_all("span", "field-content card-title")]
    depts = [t.text.split(',')[0].strip() for t in soup.find_all("div", "views-field views-field-term-node-tid")]

    return dict(zip(names, depts))


def get_arXiv_abstract_list(prof):
    arXiv = 'https://arxiv.org/search/?query={}&searchtype=all&abstracts=show'

    url = arXiv.format(prof.replace(' ', '+'))

    text = urllib.request.urlopen(url).read()

    soup = BeautifulSoup(text, 'html.parser')

    # return soup
    # return soup.find_all("li", "arxiv-result")
    # abstracts = [t.text.strip() for t in soup.find_all("div", "views-field views-field-title")]
    abstracts = [re.sub(r'\n.*', '\n', unidecode(t).text.strip()) for t in soup.find_all("span", "abstract-full")]
    # print(abstracts)

    return abstracts


def save_abstracts():
    profs = get_MIT_faculty_list()

    # get_MIT_faciulty_list returns a dict of name: dept
    for p in profs:
        print(p)

        with open(data.joinpath(p.replace(" ", "_") + ".txt"), "wb") as f:
            abs = [s.encode('UTF-8').strip() for s in get_arXiv_abstract_list(p)]
            abs = [s for s in abs if len(s)]
            f.writelines(s + "\n".encode('UTF-8') for s in abs)


def read_abstracts(prof):
    with codecs.open(data.joinpath(prof.replace(' ', '_') + ".txt"), encoding='UTF-8') as f:
        abstracts = f.readlines()
        return abstracts


def word_count(text):
    lem = nltk.stem.WordNetLemmatizer()
    words = " ".join(lem.lemmatize(word) for word in text.split())
    cntr = coll.Counter(nltk.word_tokenize(words.lower()))
    for c in string.punctuation:
        if c in cntr:
            del cntr[c]
    return cntr


def build_word_matrix(profs=None):
    if isinstance(profs, str):
        profs = [profs]  # Coerce to list
    elif profs is None or len(profs) == 0:
        profs = get_MIT_faculty_list()

    abs_freqs = []
    word_list = []
    abs_depts = []
    for p in profs:
        print(p)
        for a in read_abstracts(p):
            freqs = word_count(a)
            abs_freqs.append(freqs)

            # Collect list of name, dept FOR EACH ABSTRACT
            abs_depts.append((p, profs[p]))  # prof's name and dept
            [word_list.append(k) for k in freqs.keys() if k not in word_list]

    n_abs = len(abs_freqs)
    n_words = len(word_list)

    # Bidirectional word dictionary
    word_dict = {}
    for i, word in enumerate(word_list):
        word_dict[i] = word
        word_dict[word] = i

    # Initialize word matrix with zeros
    word_matrix = np.zeros((n_abs, n_words), int)

    # Store word counts, not %
    for a in range(n_abs):
        abstract = abs_freqs[a]
        # total = sum(abstract.values())
        for word in abstract:
            # Update word matrix with word frequencies for each abstract
            word_matrix[a, word_dict[word]] = abstract[word]

    wm = pd.DataFrame(word_matrix)
    wm.rename(columns=word_dict, inplace=True)

    wd = pd.DataFrame(abs_depts)
    wd.rename(columns=dict(enumerate(["PROF_NAME", "PROF_DEPT"])), inplace=True)

    wm = wm.join(wd)
    wm.set_index(["PROF_NAME", "PROF_DEPT"], inplace=True)

    # Add columns for abstract title and department name, which will be indices so they aren't counted in data operations

    return wm


def clean_words(dataframe):
    # lda.build_word_matrix()

    # Discard words that are too common or too rare, based on these thresholds
    too_common = 0.3
    too_rare = 0.02

    if dataframe is None:
        try:
            df = pd.read_parquet(out.joinpath('word_matrix.parquet'))
        except:
            df = build_word_matrix()
    else:
        df = dataframe.copy()

    # Look at percentage of abstracts within which each word appears
    n = len(df.index)  # Number of abstracts
    drop_words = []

    for word in sorted(df.columns):
        word_abs_freq = sum(df[word] > 0) / n
        if len(word) < 3:
            print("DROP: ", word, len(word))
            drop_words.append(word)
        elif not (too_rare < word_abs_freq < too_common):
            print("DROP: ", word, word_abs_freq)
            drop_words.append(word)
        elif word_abs_freq == 0:
            # Make sure we drop any words that somehow do not exist
            print("DROP: ", word, word_abs_freq)
            drop_words.append(word)
        else:
            print("    : ", word, word_abs_freq)

    if len(drop_words) > 0:
        df.drop(drop_words, axis=1, inplace=True)

    return df


def calc_freqs(dataframe):
    # lda.build_word_matrix()

    if dataframe is None:
        try:
            df = pd.read_parquet(out.joinpath('word_matrix.parquet'))
        except:
            df = build_word_matrix()
    else:
        df = dataframe.copy()

    for r in range(len(df.index)):
        row = df.iloc[r]
        n = np.sum(row)
        df.iloc[r] = row / n

    return df


def topic_words(L, n):
    if not isinstance(n, int):
        n = 10

    # Show top ten words per topic
    top_words = np.zeros((L._K, n), dtype=np.object)
    v = L._vocab
    rv = {}
    for word in v:
        rv[v[word]] = word

    for topic in range(L._K):
        lam = L._lambda[topic]
        idx = np.argsort(lam)[:-n-1:-1]
        words = [rv[w] for w in idx]
        for rank, word in enumerate(words):
            top_words[topic, rank] = word

    return top_words
