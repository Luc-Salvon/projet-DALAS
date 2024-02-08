import urllib
from urllib import request

import bs4

from main import get_url_steam

base_url = "https://howlongtobeat.com/game/"

with open("how-long-to-bead-ids.txt", "a") as f:
    for i in range(1501, 2501):
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
