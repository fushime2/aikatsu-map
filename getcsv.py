#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import csv
import re
from bs4 import BeautifulSoup

def get_last_page(s):
    pos_f = s.find('p=')
    pos_e = s.find('&amp')
    return s[pos_f+2 : pos_e]

def main():
    """Create csv file"""
    PREFURL = 'http://www.aikatsu.com/shop/list.php?p={}&pref={:02d}'
    with open('shops.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(['店名', '住所'])
        for pref_num in xrange(47):
            first_page = PREFURL.format(1, pref_num+1)
            r = requests.get(first_page)
            soup = BeautifulSoup(r.text.encode(r.encoding))
            s = soup.find(class_='mark last page-numbers')
            last_page_num = get_last_page(str(s))
            for page in xrange(int(last_page_num)):
                url = PREFURL.format(page+1, pref_num+1)
                r = requests.get(url)
                soup = BeautifulSoup(r.text.encode(r.encoding))
                s = soup.find("td", class_="")
                store_name = s.next_element
                store_name = store_name.encode('utf-8')
                print store_name
                s = s.find_next("td", class_="")
                address = s.next_element
                address = re.sub(r'	', '', address)
                address = address.encode('utf-8')
                print address
                s = s.find_next("td", class_="")
                writer.writerow([store_name, address])

                for i in xrange(9):
                    try:
                        store_name = s.find_next("td", class_="").next_element
                        store_name = store_name.encode('utf-8')
                        s = s.find_next("td", class_="")
                        address = s.find_next("td", class_="").next_element
                        address = re.sub(r'	', '', address)
                        address = address.encode('utf-8')
                        print store_name
                        print address
                        writer.writerow([store_name, address])
                        for j in xrange(2):
                            s = s.find_next("td", class_="")
                        s.find_next("td", class_="")
                    except:
                        break

if __name__ == '__main__':
    main()
