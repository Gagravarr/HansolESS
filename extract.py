#!/usr/bin/python3
# Licensed under the Apache License, Version 2.0
#
# Extracts data from a Hansol Technics AIO ESS
# TODO work in progress

from bs4 import BeautifulSoup
from urllib.request import urlopen

url = "http://10.5.2.80:21710/F0"

try:
   import lxml
   parser = "lxml"
except ModuleNotFoundError:
   parser = "html.parser"

with urlopen(url) as page:
   soup = BeautifulSoup(page, parser)

heading_overall = "EMS Control MODE"
heading_pvbat   = "PCS Sensing Data"

def extract_4col(table):
   "Get the labels and values for a 4-column table, excluding the header"
   data = {}
   for row in table.find_all("tr")[1:]:
      cells = iter( row.find_all("td") )
      for d, v in zip(cells,cells):
         if d and v and d.text and v.text:
            # TODO ints and floats
            data[d.text] = v.text
   return data

o = soup.find("td", string=heading_overall)
p = soup.find("td", string=heading_pvbat)

print(extract_4col(o.parent.parent))
