import bs4
import lxml
import pandas
import urllib

from urllib import request

base_url = "https://howlongtobeat.com/game/"

# 108288
for i in range(60000, 60011):
    try:
        request_text = request.urlopen(base_url + str(i)).read()
        page = bs4.BeautifulSoup(request_text, "lxml")
    except urllib.error.HTTPError:
        continue

    print(page.find("title"))


