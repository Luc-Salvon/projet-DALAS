# Architecture principale du scrapping

import csv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from scrapping import *

hltb_base_url = "https://howlongtobeat.com/game/"

options = Options()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)

# A changer pour définir l'intervalle d'indices à scrapper
start_id = 36708
end_id = 50000

with open("../Donnees/game_data.csv", "a") as write_file:
    writer = csv.writer(write_file)

    if start_id == 1:
        writer.writerow(["hltb_id", "title", "rating", "retirement", "platform", "genre", "date", "time", "price", "memoire_vive", "espace_disque", "pourcentage_pos", "review_count", "rating_value", "description", "twenty_four_hours", "all_time"])

    with open("../Donnees/how-long-to-beat-ids.txt", "r") as hltb_ids:
        for line in hltb_ids:
            hltb_id = int(line.strip())

            if hltb_id < start_id:
                continue

            if hltb_id >= end_id:
                break

            # How long to beat

            print(f"Processing {hltb_id}")

            hltb_page = bs4.BeautifulSoup(request.urlopen(hltb_base_url + str(hltb_id)).read(), "lxml")

            title = get_title(hltb_page)
            rating = get_rating(hltb_page)
            retirement = get_retirement(hltb_page)
            platform = get_platform(hltb_page)
            genre = get_genre(hltb_page)
            date = get_date(hltb_page)
            time = get_time(hltb_page)

            # Steam

            steam_url = get_url_steam(hltb_page)

            if steam_url is None:
                print(f"Steam URL not found for {hltb_id}")
                continue

            steam_page = get_page(steam_url, driver)

            price = get_price(steam_page)
            memoire_vive = get_memoire_vive(steam_page)
            espace_disque = get_espace_disque(steam_page)
            pourcentage_pos = get_pourcentage_pos(steam_page)
            review_count, rating_value, best_rating, worst_rating = get_steam_rating_stats(steam_page)
            description = get_steam_description(steam_page)
            #langues_audio, langues_sous_titres = get_language(steam_page) #probleme
            twenty_four_hours, all_time = get_players_stats(hltb_page, driver)

            # Write to file

            writer.writerow([hltb_id, title, rating, retirement, platform, genre, date, time, price, memoire_vive, espace_disque, pourcentage_pos, review_count, rating_value, description, twenty_four_hours, all_time])
