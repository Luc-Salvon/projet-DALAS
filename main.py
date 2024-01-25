import bs4
import lxml
import pandas
import urllib
import re

from urllib import request

base_url = "https://howlongtobeat.com/game/"


def get_title(page):
    title = page.find("title").text
    title = title[12:].split('?')[0]
    return title

def get_rating(page):
    rating_tag = page.find("a", attrs={"class": "text_primary", "href": re.compile("/game/[0-9]+/reviews")})
    if rating_tag is None:
        return "NR"

    rating = rating_tag.text.split("%")[0]
    return rating

def get_platform(page):
    classes = page.find_all("div","GameSummary_profile_info__HZFQu GameSummary_medium___r_ia")
    for classe in classes:
        if "Platform" in classe.find("strong").text:
            platform = classe.text
            platform = platform.split(":")[1][1:]
            platform = platform.split(', ')
            return platform
    return ["NP"] # pas de plateforme renseignee

# 108288
for i in range(60000, 60011):
    try:
        request_text = request.urlopen(base_url + str(i)).read()
        page = bs4.BeautifulSoup(request_text, "lxml")
    except urllib.error.HTTPError:
        continue

    print(get_title(page))
    print(get_rating(page))
    print(get_platform(page))
    print("")




