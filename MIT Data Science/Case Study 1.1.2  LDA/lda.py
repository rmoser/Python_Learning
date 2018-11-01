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
out = ".\Data\\"


def read_data(file):
    text = ""  # Init return value if fail

    if not Path(file).exists():
        print("ERROR: File not found: {}".format(file))
        return text

    with open(file) as f:
        text = ''.join(f.readlines())

    return text


def read_soup(file):
    if not Path(file).exists():
        print("ERROR: File not found: {}".format(file))
        raise FileExistsError

    with open(file) as f:
        return BeautifulSoup(f, "html.parser")


def get_MIT_faculty_list():

    # Use the abstract file list if it exists
    data = Path(out)
    if data.exists():
        # Path.stem is the filename with no extension
        # Which is exactly the professor's name
        # Replace '_' with ' ' so the data is the same, regardless of which source was used
        return [f.stem.replace('_', ' ') for f in data.glob("*.txt")]

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
    return [unidecode(t.text.strip()) for t in soup.find_all("div", "views-field views-field-title")]


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

    for p in profs:
        print(p)

        with open(out + p.replace(" ", "_") + ".txt", "wb") as f:
            abs = [s.encode('UTF-8').strip() for s in get_arXiv_abstract_list(p)]
            abs = [s for s in abs if len(s)]
            f.writelines(s + "\n".encode('UTF-8') for s in abs)


def read_abstracts(prof):
    with codecs.open(out + prof.replace(' ', '_') + ".txt", encoding='UTF-8') as f:
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
    if profs is None:
        profs = get_MIT_faculty_list()

    abs_freqs = []
    word_list = []
    for p in profs:
        print(p)
        for a in read_abstracts(p):
            freqs = word_count(a)
            abs_freqs.append(freqs)
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

    # Convert word counts to %
    for a in range(n_abs):
        abstract = abs_freqs[a]
        # total = sum(abstract.values())
        for word in abstract:
            # Update word matrix with word frequencies for each abstract
            word_matrix[a, word_dict[word]] = abstract[word]

    wm = pd.DataFrame(word_matrix)
    wm.rename(columns=word_dict, inplace=True)
    # wm.to_parquet("word_matrix.parquet")
    # wm.transpose().to_csv("word_matrix.csv")

    return wm


def calc_freqs(dataframe):
    # lda.build_word_matrix()

    if dataframe is None:
        try:
            dataframe = pd.read_parquet('word_matrix.parquet')
        except:
            wm = build_word_matrix()

    word_list = dataframe.columns

    word_dict = {}
    for i in range(len(dataframe.columns)):
        word_dict[i] = dataframe.columns[i]
        word_dict[dataframe.columns[i]] = i

    word_freqs_global = {}
    for word in word_list:
        word_freqs_global[word] = dataframe[word].sum()

    # New dataframe to calculate word frequencies among the abstracts
    wf = pd.DataFrame()
    wf["word"] = word_freqs_global.keys()

    # Index on word so we can sum the values
    wf.set_index('word', inplace=True)

    # Add the word counts for each abstract
    wf["freq"] = word_freqs_global.values()

    # Sum of all values is the total number of words
    total_words = wf.values.sum()

    # Convert word counts to percents, and sort just for easy inspection
    wf["pct"] = wf.freq / total_words
    wf.sort_values("freq", inplace=True)

    # Calculate the percentage of abstracts which contain each word
    wf["pct"] = [np.mean([dataframe[w] > 0]) for w in word_list]

    # Eliminate words which are too rare or too common
    wf = wf[np.logical_and(wf.pct < 0.3, wf.pct > 0.01)]

    # Clean the main table
    dataframe = dataframe[list(wf.index.values.astype(str))]
    del wf

    dataframe.to_parquet('word_matrix_cleaned.parquet')

    # Convert word counts to % of words in each abstract
    dataframe = dataframe.div(dataframe.sum(axis=1), axis=0)

    dataframe.to_parquet('word_matrix_freqs.parquet')

    return dataframe
