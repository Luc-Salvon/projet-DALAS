# Permet de crawler les pages de how long to beat pour récupérer les indices des jeux qui ont une page steam associée

import urllib
from urllib import request

import bs4

base_url = "https://howlongtobeat.com/game/"


def get_url_steam(page):
    a = page.find("a", "StoreButton_steam__RJCCL")
    if a is None:
        return

    return a["href"]


with open("../Donnees/how-long-to-beat-ids.txt", "a") as f:
    for i in range(89240, 90000):  # Indices sur lesquels crawler
        if i % 10 == 0:
            print(i)

        try:
            request_text = request.urlopen(base_url + str(i)).read()
            page = bs4.BeautifulSoup(request_text, "lxml")
        except urllib.error.HTTPError:
            continue

        url_steam = get_url_steam(page)

        if url_steam:
            f.write(f"{i}\n")
