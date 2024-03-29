from requests import get
from bs4 import BeautifulSoup

import pandas as pd

import json
import os


def scrape_links_one_page(url):
    """
    Creates a list of 10 urls from a single page, given that page's url
    """
    headers = {'User-Agent': 'Codeup Data Science'} 
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    extension = soup.find_all("a", {"class":"v-align-middle"}, {"data-hydro-click":"url"})
    extensions = []
    for count in range(len(extension)):
        extensions.append("http://github.com/" + extension[count].get_text())
    return extensions

def make_url_list():
    """
    Creates a 10 page list. Each page needs the links to repositories scapes.
    """
    urls = []
    for count in range(1,11):
        urls.append("https://github.com/search?p={}&q=stars%3A%3E100&type=Repositories".format(count))
    return urls


def loop_through_urls():
    """
    Creates a 100 page list. Each element is a link to be scraped of their README.
    """
    ten_urls = make_url_list()
    big_list = []
    for url in ten_urls:
        big_list.extend(scrape_links_one_page(url))
    return big_list

def get_readme_text(url):
    response = get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    textboxes = soup.findAll("div", {"class": "Box-body"})
    readme_text = textboxes[0].text

    language = soup.find("span", {"class": "lang"})
    if language == None:
        language = "None"
    else:
        language = soup.find("span", {"class": "lang"}).get_text()

    return {
        "repo" : url[18:],
        "language" : language,
        "readme" : readme_text
    }

def make_corpus():
    URLs = pd.read_csv('URL_list_100.csv', header=0, names=['page'])
    corpus = [get_readme_text(url) for url in URLs.page]
    return corpus


def get_corpus(filename):
    if os.path.exists(filename):
        with open(filename) as json_file:
            reads = json.load(json_file)
        return pd.DataFrame(reads)
    else:
        data = make_corpus()
        with open(filename, 'w') as json_file:
            json.dump(data, json_file)
        return pd.DataFrame(data)

def get_big_corpus():
    df1 = pd.read_json('data_first.json')
    df2 = pd.read_json('data_second.json')
    frames = [df1,df2]
    df = pd.concat(frames)
    return df


##############
#bottom20 urls in case rate limiting is implemented again.

def make_bottom_20():
    urls = []
    for count in range(9,11):
        urls.append("https://github.com/search?p={}&q=stars%3A%3E100&type=Repositories".format(count))
    return urls

def loop_through_bottom20():
    """
    Creates a 100 page list. Each element is a link to be scraped of their README.
    """
    ten_urls = make_bottom_20()
    big_list = []
    for url in ten_urls:
        big_list.extend(scrape_links_one_page(url))
    return big_list

def make_corpus_20():
    URLs = pd.read_csv('URL_list_20.csv', header=0, names=['page'])
    corpus = [get_readme_text(url) for url in URLs.page]
    return corpus    

#############