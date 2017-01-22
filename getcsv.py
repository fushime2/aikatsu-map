import re
import urllib.request
import csv
from bs4 import BeautifulSoup

# page = 1,2,...
# prefnum = 01,02,...,47
BASE_URL = "http://www.aikatsu.com/stars/playshop/list.php?p={page:d}&pref={prefnum:02d}"

rows = [["店名", "住所"]]


def get_last_page(pref):
    """ '>>' の href 要素から最後のページ番号を取得 """
    url = BASE_URL.format(page=1, prefnum=pref)
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, "lxml")
    try:
        href = soup.find("a", text=re.compile(("»")))["href"]
    except KeyError:
        return 1
    last_page = re.search("p=[0-9]+&", href).group().replace("p=", "").replace("&", "")
    return int(last_page)


def format_string(tag):
    """ タグから空白とかを削除して文字列型で返す """
    delete = [" ", "\n", "\r", "<td>"]
    if tag.string is not None:
        s = tag.string
        for d in delete:
            s = s.replace(d, "")
        print(s)
        return s
    else:
        s = str(tag)
        ng_words = ["paginator", "titlenum"]
        for ng in ng_words:
            if ng in s: return
        p = s.find("<a class")
        s = s[:p]
        for d in delete:
            s = s.replace(d, "")
        print(s)
        return s


def make_list(pref, page):
    url = BASE_URL.format(page=page, prefnum=pref)
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, "lxml")
    td = soup.find_all("td")
    data = list()
    for tag in td:
        str = format_string(tag)
        if str is not None:
            data.append(str)
    for i in range(0, len(data), 2):
        rows.append([data[i], data[i + 1]])


def main():
    print("Start")
    for pref in range(1, 48):
        lastpage = get_last_page(pref)
        for page in range(1, lastpage + 1):
            make_list(pref, page)

    f = open("shops.csv", "w", encoding="utf-8")
    writer = csv.writer(f, lineterminator="\n")
    writer.writerows(rows)
    f.close()
    print("End")


if __name__ == "__main__":
    main()
