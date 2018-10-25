from pathlib import Path
import io
import collections
import nltk
import urllib.request
import re
from bs4 import BeautifulSoup
from unidecode import unidecode
import os


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
    url = r'https://www.eecs.mit.edu/people/faculty-advisors'

    text = urllib.request.urlopen(url).read()

    soup = BeautifulSoup(text, 'html.parser')

    profs = [unidecode(t.text.strip()) for t in soup.find_all("div", "views-field views-field-title")]

    return profs

def get_arXiv_abstract_list(prof):
    arXiv = 'https://arxiv.org/search/?query={}&searchtype=all&abstracts=show'

    url = arXiv.format(prof.replace(' ', '+'))

    text = urllib.request.urlopen(url).read()

    soup = BeautifulSoup(text, 'html.parser')

    # return soup
    # return soup.find_all("li", "arxiv-result")
    # abstracts = [t.text.strip() for t in soup.find_all("div", "views-field views-field-title")]
    abstracts = [re.sub(r'\n.*' ,'\n', unidecode(t).text.strip()) for t in soup.find_all("span", "abstract-full")]
    print(abstracts)

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
    with open(out + prof.replace(' ', '_') + ".txt") as f:
        abstracts = f.readlines()
        return abstracts
