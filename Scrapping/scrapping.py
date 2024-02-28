import time
import urllib
from urllib import request

import bs4
import pandas as pd
import re


# •=================•
#  |  UTILITAIRES  |
# •=================•


def get_page(url, driver=None):
    try:
        # On utilise Selenium si le driver est renseigné
        if driver is not None:
            driver.get(url)
            time.sleep(.5)
            return bs4.BeautifulSoup(driver.page_source, 'html.parser')

        # Sinon, on utilise urllib
        request_text = request.urlopen(url).read()
        page = bs4.BeautifulSoup(request_text, "lxml")
        return page

    except urllib.error.HTTPError:
        return


# •======================•
#  |  HOW LONG TO BEAT  |
# •======================•

def get_title(page):
    title = page.find("title").text
    title = title[12:].split('?')[0]
    return title


def get_rating(page):
    rating_tag = page.find("a", attrs={"class": "text_primary", "href": re.compile("/game/[0-9]+/reviews")})

    if rating_tag is None:
        return pd.NA

    rating = rating_tag.text.split("%")[0]
    return rating


def get_retirement(page):
    retirement_tag = page.find("a", attrs={"class": "text_primary", "href": re.compile("/game/[0-9]+/lists#retirement")})
    if retirement_tag is None:
        return pd.NA

    retirement = retirement_tag.h5.text.split("%")[0]
    retirement = re.sub("([A-Z]|[a-z])+", "", retirement)
    return retirement


def get_platform(page):
    classes = page.find_all("div", "GameSummary_profile_info__HZFQu GameSummary_medium___r_ia")
    for classe in classes:
        if "Platform" in classe.find("strong").text:
            platform = classe.text
            platform = platform.split(":")[1][1:]
            platform = platform.split(', ')
            return platform
    return pd.NA  # pas de plateforme renseignee


def get_genre(page):
    classes = page.find_all("div", "GameSummary_profile_info__HZFQu GameSummary_medium___r_ia")
    for classe in classes:
        if "Genre" in classe.find("strong").text:
            genre = classe.text
            genre = genre.split(":")[1][1:]
            genre = genre.split(', ')
            return genre
    return pd.NA  # pas de genre renseigne


def get_date(page):
    classes = page.find_all("div", "GameSummary_profile_info__HZFQu")
    for classe in classes:
        description = classe.find("strong")
        if description is not None:
            if "NA" in description.text:
                date = classe.text
                date = date.split(":")[1][1:]
                return int(date[-4:])
    return pd.NA  # pas de date renseignee


def get_time(page):
    table = page.find("table", "GameTimeTable_game_main_table__7uN3H")
    if table is not None:
        colonne_main_story = table.find("tr", "spreadsheet")
        time_main_story = colonne_main_story.find_all("td")[2]
        time_main_story = time_main_story.text
        time_main_story = time_main_story.split(" ")
        if len(time_main_story) > 1 and time_main_story[1][0].isdigit():
            heures = float(time_main_story[0][:-1])
            minutes = float(time_main_story[1][:-1])
            time = heures + minutes * 1 / 60
        elif len(time_main_story) > 1:
            time = time_main_story[0]
        else:
            time = time_main_story[0][:-1]
        try:
            return float(time)
        except ValueError:
            return pd.NA
    else:
        return pd.NA  # temps non renseigné


# •===========•
#  |  STEAM  |
# •===========•


def get_url_steam(page):
    a = page.find("a", "StoreButton_steam__RJCCL")
    if a is None:
        return

    return a["href"]


def get_price(page_steam):
    div = page_steam.find("div", "game_purchase_price")

    if div is None:
        return pd.NA

    return div.text.strip()


def get_memoire_vive(page_steam):
    try:
        div = page_steam.find("div", "game_area_sys_req_full")
        if div is not None:
            ul = div.find("ul", "bb_ul")
            if ul is None:
                return pd.NA
            lis = ul.find_all("li")
            for li in lis:
                if li.find("strong") is not None:
                    if "Memory:" == li.text[:7]:
                        memoire_vive = li.text.split(":")[1]
                        if memoire_vive[0]==" ":
                            try:
                                memoire_vive_nb = float(memoire_vive.split(" ")[1])
                                unite = memoire_vive.split(" ")[2]
                            except ValueError:
                                return pd.NA
                        else:
                            try:
                                memoire_vive_nb = float(memoire_vive.split(" ")[0])
                                unite = memoire_vive.split(" ")[1]
                            except ValueError:
                                return pd.NA
                        if unite == "MB":
                            memoire_vive_nb *= 0.001
                        return memoire_vive_nb
        else:
            div = page_steam.find("div", "game_area_sys_req_leftCol")
            if div is not None:
                ul = div.find("ul", "bb_ul")
                if ul is not None:
                    lis = ul.find_all("li")
                    for li in lis:
                        if li.text is not None:
                            if "Memory:" == li.text[:7]:
                                memoire_vive = li.text.split(":")[1]
                                if memoire_vive[0]==" ":
                                    try:
                                        memoire_vive_nb = float(memoire_vive.split(" ")[1])
                                        unite = memoire_vive.split(" ")[2]
                                    except ValueError:
                                        return pd.NA
                                else:
                                    try:
                                        memoire_vive_nb = float(memoire_vive.split(" ")[0])
                                        unite = memoire_vive.split(" ")[1]
                                    except ValueError:
                                        return pd.NA
                                if unite == "MB":
                                    memoire_vive_nb *= 0.001
                                return memoire_vive_nb
    except:
        return pd.NA

    return pd.NA


def get_espace_disque(page_steam):
    try:
        div = page_steam.find("div", "game_area_sys_req_full")
        if div is not None:
            ul = div.find("ul", "bb_ul")
            if ul is None:
                return pd.NA
            lis = ul.find_all("li")
            for li in lis:
                if li.text is not None:
                    if "Storage:" == li.text[:8] or "Hard Drive"==li.text[:10]:
                        espace_disque = li.text.split(":")[1]
                        if espace_disque[0]==" ":
                            try:
                                espace_disque_nb = float(espace_disque.split(" ")[1])
                                unite = espace_disque.split(" ")[2]
                            except ValueError:
                                espace_disque_nb = float(espace_disque.split(" ")[1][:-2])
                                unite = espace_disque.split(" ")[1][-2:]
                        else:
                            try:
                                espace_disque_nb = float(espace_disque.split(" ")[0])
                                unite = espace_disque.split(" ")[1]
                            except ValueError:
                                espace_disque_nb = float(espace_disque.split(" ")[0][:-2])
                                unite = espace_disque.split(" ")[1][-2:]
                        if unite == "MB":
                            espace_disque_nb *= 0.001
                        return espace_disque_nb
        else:
            div = page_steam.find("div", "game_area_sys_req_leftCol")
            if div is not None:
                ul = div.find("ul", "bb_ul")
                if ul is not None:
                    lis = ul.find_all("li")
                    for li in lis:
                        if li.text is not None:
                            if "Storage" == li.text[:7] or "Hard Drive"==li.text[:10]:
                                espace_disque = li.text.split(":")[1]
                                if espace_disque[0]==" ":
                                    try:
                                        espace_disque_nb = float(espace_disque.split(" ")[1])
                                        unite = espace_disque.split(" ")[2]
                                    except ValueError:
                                        espace_disque_nb = float(espace_disque.split(" ")[1][:-2])
                                        unite = espace_disque.split(" ")[1][-2:]
                                else:
                                    espace_disque_nb = float(espace_disque.split(" ")[0])
                                    unite = espace_disque.split(" ")[1]
                                if unite == "MB":
                                    espace_disque_nb *= 0.001
                                return espace_disque_nb
    except:
        return pd.NA

    return pd.NA


def get_pourcentage_pos(page_steam):
    span = page_steam.find("span", "nonresponsive_hidden responsive_reviewdesc")
    if span is not None:
        texte = span.text
        texte = texte.split("-")[1]
        texte = texte.split("%")[0]
        pourcentage = texte[1:]
        return pourcentage

    return pd.NA


def get_steam_rating_stats(page_steam):
    reviewCount = page_steam.find("meta", itemprop="reviewCount")
    if reviewCount is not None:
        reviewCount = int(reviewCount.get("content"))
        ratingValue = page_steam.find("meta", itemprop="ratingValue")
        ratingValue = int(ratingValue.get("content"))
        bestRating = page_steam.find("meta", itemprop="bestRating")
        bestRating = int(bestRating.get("content"))
        worstRating = page_steam.find("meta", itemprop="worstRating")
        worstRating = int(worstRating.get("content"))
        return reviewCount, ratingValue, bestRating, worstRating

    return pd.NA, pd.NA, pd.NA, pd.NA


def get_steam_description(page_steam):
    div = page_steam.find("div", id="game_area_description")
    if div is not None:
        descr = div.text[16:].replace("\n"," ").replace("\t","")
        return descr

    return pd.NA


def get_language(page_steam):
    tables = page_steam.find_all("table")
    for table in tables:
        if table["class"] == ["game_language_options"]:
            trs = table.find_all("tr")
            langues_audio = []
            langues_sous_titres = []
            for tr in trs[1:]:
                tds = tr.find_all("td")
                if len(tds) >= 3 and tds[2].find("span") is not None:
                    langues_audio.append(tds[0].text[6:-3])
                if len(tds) >= 4 and tds[3].find("span") is not None:
                    langues_sous_titres.append(tds[0].text[6:-3])
            if langues_audio:
                langues_audio = pd.NA
            if langues_sous_titres:
                langues_sous_titres = pd.NA
            return langues_audio, langues_sous_titres

    return pd.NA, pd.NA


def get_players_stats(page, driver):
    numero_de_jeu = get_url_steam(page).split("/")[-2]
    url_charts = "https://steamcharts.com/app/" + numero_de_jeu
    page_charts = get_page(url_charts, driver)
    divs = page_charts.find_all("div", "app-stat")
    if divs:
        twenty_four_hours = divs[1].find("span").text.replace(',', '')
        all_time = divs[2].find("span").text.replace(',', '')
        return int(twenty_four_hours), int(all_time)
    return pd.NA, pd.NA
