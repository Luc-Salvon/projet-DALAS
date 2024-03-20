import csv

import scrapping

# Load game_data.csv and get each row
with open("../Donnees/game_data.csv", "r") as f_read:
    with open("../Donnees/game_data_bis.csv", "a") as f_write:
        reader = csv.reader(f_read)
        writer = csv.writer(f_write)

        start_id = 0
        for i, row in enumerate(reader):
            if i == 0:
                writer.writerow(["hltb_id", "title", "rating", "retirement", "platform", "genre", "date", "time", "price", "memoire_vive", "espace_disque", "pourcentage_pos", "review_count", "rating_value", "description", "twenty_four_hours", "all_time", "steam_id", "steam_tags", "steam_genres"])
                continue
            if i < start_id:
                continue

            hltb_id = row[0]
            hltb_page = scrapping.get_page(f"https://howlongtobeat.com/game/{hltb_id}")
            steam_url = scrapping.get_url_steam(hltb_page)
            if steam_url is None:
                print(f"Steam URL not found for {hltb_id}")
                continue
            steam_page = scrapping.get_page(steam_url)

            steam_id = steam_url.split("/")[-2]
            steam_tags = scrapping.get_user_tags(steam_page)
            steam_genres = scrapping.get_genres_steam(steam_page)

            writer.writerow(row + [steam_id, steam_tags, steam_genres])
