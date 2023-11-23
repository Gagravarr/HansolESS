#!/usr/bin/python3
# Licensed under the Apache License, Version 2.0
#
# Extracts data from a Hansol Technics AIO ESS
# TODO work in progress

from bs4 import BeautifulSoup
from urllib.request import urlopen
from models import *

try:
   import lxml
   parser = "lxml"
except ModuleNotFoundError:
   parser = "html.parser"

heading_overall = "EMS Control MODE"
heading_status  = "PCS Status"
heading_pvbat   = "PCS Sensing Data"
heading_battery = "BMS data"


def find_table(soup, heading):
   "Finds the table based on the Heading"
   h = soup.find("td", string=heading)
   if not h:
      raise Exception("Could not find table with heading '%s' in %s" % (heading, url))

   tbl = h.parent.parent
   if tbl.name != "table":
      raise Exception("Table with heading '%s' in the wrong format:\n%s" % (heading, tbl))
   return tbl

def get_value(cell):
   v = cell.text.strip()
   try:
      num = float(v)
      if num.is_integer():
         return int(num)
      return num
   except ValueError:
      return v


def extract_paired_columns(table):
   "Get the labels and values from a multi-column table"
   data = {}

   # Skip the header row, then odd-column is label, even-column value
   for row in table.find_all("tr")[1:]:
      cells = iter( row.find_all("td") )
      for d, v in zip(cells,cells):
         if d and v and d.text and v.text:
            data[d.text] = get_value(v)
   return data

def extract_vips(table):
   "Extract the Voltage/Current/Power data"
   vips = []
   for row in table.find_all("tr"):
      label = row.find("td").text
      vip = VIP(label)

      cells = iter( row.find_all("td")[1:] )
      for d, v in zip(cells,cells):
         if d.text == "V[V]:":
            vip.voltage = float(v.text.strip())
         if d.text == "I[A]:":
            vip.current = float(v.text.strip())
         if d.text == "P[W]:":
            vip.power = float(v.text.strip())
      if vip.is_complete():
         vips.append(vip)
   return vips

def extract_battery_pct(table):
   "Extract the battery's current capacity %"
   soc_td = table.find("td", string="SOC(%):")
   val_td = soc_td.next_sibling
   return get_value(val_td)


def extract_all(soup):
   system = System()

   # TODO
   print(extract_paired_columns(find_table(soup, heading_overall)))
   print(extract_paired_columns(find_table(soup, heading_status)))

   system.vips = extract_vips(find_table(soup, heading_pvbat))
   system.battery = Battery(
           extract_battery_pct(find_table(soup, heading_battery)),
           False)

   return system


def extract_remote(host, port):
   url = "http://%s:%d/F0" % (host, port)
   with urlopen(url) as page:
      soup = BeautifulSoup(page, parser)

   return extract_all(soup)

def extract_local(filename):
   with open(filename,"r") as page:
      soup = BeautifulSoup(page, parser)
   return extract_all(soup)
