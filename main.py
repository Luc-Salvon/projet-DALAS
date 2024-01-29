import bs4
import lxml
import pandas as pd
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

def get_genre(page):
    classes = page.find_all("div","GameSummary_profile_info__HZFQu GameSummary_medium___r_ia")
    for classe in classes:
        if "Genre" in classe.find("strong").text:
            genre = classe.text
            genre = genre.split(":")[1][1:]
            genre = genre.split(', ')
            return genre
    return ["NG"] # pas de genre renseigne

def get_date(page):
    classes = page.find_all("div","GameSummary_profile_info__HZFQu")
    for classe in classes:
        description = classe.find("strong")
        if description != None:
            if "NA" in description.text:
                date = classe.text
                date = date.split(":")[1][1:]
                return int(date[-4:])
    return "ND" # pas de date renseignee

def get_time(page):
    table = page.find("table","GameTimeTable_game_main_table__7uN3H")
    if table != None:
        colonne_main_story = table.find("tr","spreadsheet")
        time_main_story = colonne_main_story.find_all("td")[2]
        time_main_story = time_main_story.text
        time_main_story = time_main_story.split(" ")
        if len(time_main_story)>1:
            heures = float(time_main_story[0][:-1])
            minutes = float(time_main_story[1][:-1])
            time = heures + minutes*1/60
        else:
            time = time_main_story[0][:-1]

        return float(time)
    else:
        return "NT" # temps non renseigné


df = pd.DataFrame(columns=["title","rating","platform","avg_time","genre","date"])

# 108288
for i in range(40000, 40011):
    try:
        request_text = request.urlopen(base_url + str(i)).read()
        page = bs4.BeautifulSoup(request_text, "lxml")
    except urllib.error.HTTPError:
        continue
    df = df.append({"title":get_title(page),"rating":get_rating(page),
                    "platform":get_platform(page),"avg_time":get_time(page),
                    "genre":get_genre(page),"date":get_date(page)},ignore_index=True)
    """
    print(get_title(page))
    print(get_rating(page))
    print(get_platform(page))
    print(get_time(page))
    print(get_genre(page))
    print(get_date(page))
    print("")
    """

print(df)



