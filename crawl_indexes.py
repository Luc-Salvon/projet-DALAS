import urllib
from urllib import request

import bs4

base_url = "https://howlongtobeat.com/game/"


def get_url_steam(page):
    a = page.find("a", "GameSummary_steam_text__Fe9Uv")
    if a is None:
        return

    return a["href"]


with open("how-long-to-beat-ids.txt", "a") as f:
    for i in range(4563, 100000):
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