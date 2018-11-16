# MIT Data Science - Case Study 1.2 Spectral Clustering

import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
from goose3 import Goose
import newspaper
import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import codecs
from pathlib import Path

folder = Path(r"c:\temp\CNN")

cnn = 'https://www.cnn.com'
nbc = 'https://www.nbcnews.com'

site = cnn
browser = None


# url = 'http://money.cnn.com/2012/02/20/news/economy/david_walker_third_party/index.htm'
# url = "https://www.npr.org/2018/11/09/666077614/wildfires-wreak-havoc-on-california-including-a-thousand-oaks-still-in-mourning"


def get_soup(url):
    # Use selenium to parse the javascript
    global browser
    if browser is None:
        options = Options()
        options.headless = True
        options.preferences["media.autoplay.enabled"] = False
        browser = webdriver.Firefox(options=options)

        browser.implicitly_wait(30)


    # Read the full HTML of the site
    browser.get(url)
    text = browser.page_source

    # Parse with BeautifulSoup
    soup = BeautifulSoup(text, 'html.parser')
    # driver.close()
    return soup


def get_article_urls(site=None):
    if site is None:
        site = cnn

    if isinstance(site, BeautifulSoup):
        soup = site
    else:
        # Get BeautifulSoup object for the site
        soup = get_soup(site)

    articles = soup.find_all("article", "cd--article")
    return [site + a.get("data-vr-contentbox") for a in articles]


def get_articles(urls=None):
    if urls is None:
        urls = get_article_urls(cnn)

    articles = []
    for url in urls:
        print(url)
        article = get_soup(url)

        meta = article.find_all("meta")
        print("metas: ", len(meta))

        # Init
        topic = ""
        title = ""
        story = ""

        for m in meta:
            if m.get("property") == "og:title":
                title = m.get("content")
                continue

            if m.get("name") == "section":
                topic = m.get("content")
                continue

            if len(topic) and len(title):
                pass # break

        paragraphs = article.find_all("div", "zn-body__paragraph")
        story = " ".join([p.text for p in paragraphs])

        articles.append((topic, title, story))

    return articles


def get_titles_r0():
    soup = get_soup(cnn)

    articles = soup.find_all("article", "cd--article")

    for a, article in enumerate(articles):
        title = article.text
        topic = article.get("data-section-name")

        print(a, ": title: ", title)
        print(a, ": topic: ", topic, "\n")

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
    url = site + "/search/?size=1&q={}".format(html_title)

    soup = get_soup(url)
    story = soup.find("div", "cnn-search__result-body")
    if story is not None:
        return story.text.strip()


def write_articles(urls=None):
    if urls is None:
        urls = get_article_urls(site)
    if isinstance(urls, str):
        urls = [urls]

    # Tuple indices for each Article
    topic = 0
    title = 1
    story = 2

    for i, url in enumerate(urls):
        print(i, url)
        article = get_articles([url])[0]

        print("{}: {} / {}".format(i, article[topic], article[title]))
        print("{}: story:\n{}".format(i, article[story]))

        # Write topic
        file = "topic-{}.txt".format(i)
        with open(folder.joinpath(file), "w", encoding="UTF-8") as f:
            f.write(article[topic])

        file = "title-{}.txt".format(i)
        with open(folder.joinpath(file), "w", encoding="UTF-8") as f:
            f.write(article[title])

        file = "article-{}.txt".format(i)
        with open(folder.joinpath(file), "w", encoding="UTF-8") as f:
            f.write(article[story])

        print("{}: saved.\n".format(i))

    # Done with browser
    if False:
        global browser
        browser.close()
        browser = None

def read_articles(n=None):
    if not n is None:
        file = folder.joinpath("title-{}.txt".format(n))
        if not file.exists():
            raise FileNotFoundError("Unable to locate {}/title-{}.txt".format(folder, n))
        files = [file]
    else:
        files = folder.glob("title-*.txt")

    for file in files:
        pass
