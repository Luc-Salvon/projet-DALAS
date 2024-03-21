import csv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import scrapping

options = Options()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)

# Load game_data.csv and get each row
with open("../Donnees/game_data.csv", "r") as f_read:
    with open("../Donnees/game_data_bis.csv", "a") as f_write:
        reader = csv.reader(f_read)
        writer = csv.writer(f_write)

        start_id = 0
        for i, row in enumerate(reader):
            print(f"Processing line {i}")
            if i == 0:
                writer.writerow(["hltb_id", "title", "rating", "retirement", "platform", "genre", "date", "time", "price", "memoire_vive", "espace_disque", "pourcentage_pos", "review_count", "rating_value", "description", "twenty_four_hours", "all_time", "steam_id", "steam_tags", "steam_genres", "players_by_time"])
                continue
            if i < start_id:
                continue

            average_players = row[16]

            if average_players is None:
                continue

            steam_id = row[17]
            steamcharts_page = scrapping.get_page(f"https://steamcharts.com/app/{steam_id}", driver=driver)

            if steamcharts_page is None:
                print(f"{i} - Steamcharts page not found")
                continue

            players_by_time = scrapping.get_players_by_time(steamcharts_page)

            writer.writerow(row + [players_by_time])
