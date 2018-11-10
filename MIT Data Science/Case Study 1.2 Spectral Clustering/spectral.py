# MIT Data Science - Case Study 1.2 Spectral Clustering

import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
from goose3 import Goose
import newspaper
import selenium
from selenium import webdriver
import codecs
from pathlib import Path

folder = Path(r"c:\temp\CNN")
cnn = 'http://www.cnn.com'
# url = 'http://money.cnn.com/2012/02/20/news/economy/david_walker_third_party/index.htm'
# url = "https://www.npr.org/2018/11/09/666077614/wildfires-wreak-havoc-on-california-including-a-thousand-oaks-still-in-mourning"


def get_soup(url):
    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
    driver.get(url)

    # Read the full HTML of the site
    text = driver.page_source

    # Parse with BeautifulSoup
    soup = BeautifulSoup(text, 'html.parser')
    driver.close()
    return soup


def get_titles():
    soup = get_soup(cnn)

    articles = soup.find_all("article", "cd--article")

    for a, article in enumerate(articles):
        title = article.text
        topic = article.get("data-section-name")

        print(a, ": title: ", title)
        print(a, ": topic: ", topic)

        file = "title-{}.txt".format(str(a))
        with codecs.open(folder.joinpath(file), "w", encoding="UTF-8") as f:
            f.write(title)

        file = "topic-{}.txt".format(str(a))
        with codecs.open(folder.joinpath(file), "w", encoding="UTF-8") as f:
            f.write(topic)


def read_title(n):
    file = folder.joinpath("title-{}.txt".format(n))
    if not file.exists():
        print("ERROR: File {} not found".format(file))

    with open(file, "r", encoding="UTF-8") as f:
        return f.read()


def get_story(title):
    # Search just the first 5 words...
    html_title = urllib.parse.quote(" ".join(title.split()[:5]))
    url = "https://www.cnn.com/search/?size=1&q={}".format(html_title)

    soup = get_soup(url)
    story = soup.find("div", "cnn-search__result-body")
    if story is not None:
        return story.text.strip()


def run():
    if not folder.joinpath("title-10.txt").exists():
        get_titles()

    titles = folder.glob("title-*.txt")

    for file in titles:
        article = "article" + file.name[5:]
        with open(file, "r", encoding="UTF-8") as f:
            title = f.read()
            story = get_story(title)

        if isinstance(story, str):
            with open(folder.joinpath(article), "w", encoding="UTF-8") as f:
                f.write(story)
