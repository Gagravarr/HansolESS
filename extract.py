#!/usr/bin/python3
# Licensed under the Apache License, Version 2.0
#
# Extracts data from a Hansol Technics AIO ESS
# TODO work in progress

from bs4 import BeautifulSoup
from urllib.request import urlopen

url = "http://10.5.2.80:21710/F0"
with urlopen(url) as page:
   soup = BeautifulSoup(page)
# TODO see if we can do lxml, otherwise html.parser backup

heading_overall = "EMS Control MODE"
heading_pvbat   = "PCS Sensing Data"

print(soup)
t = soup.find("td", string=heading_overall)
print(t)
