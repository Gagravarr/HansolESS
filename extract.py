#!/usr/bin/python3
# Licensed under the Apache License, Version 2.0
#
# Extracts data from a Hansol Technics AIO ESS
# TODO work in progress

from bs4 import BeautifulSoup
from urllib.request import urlopen
from models import *

url = "http://10.5.2.80:21710/F0"

try:
   import lxml
   parser = "lxml"
except ModuleNotFoundError:
   parser = "html.parser"

with urlopen(url) as page:
   soup = BeautifulSoup(page, parser)

heading_overall = "EMS Control MODE"
heading_status  = "PCS Status"
heading_pvbat   = "PCS Sensing Data"
heading_battery = "BMS data"


def find_extract_table(heading, table_type):
   "Finds the table based on the Heading, then Extracts"
   h = soup.find("td", string=heading)
   if not h:
      raise Exception("Could not find table with heading '%s' in %s" % (heading, url))

   tbl = h.parent.parent
   if table_type == "vip":
      return extract_vips(tbl)
   elif table_type == "bat":
      return extract_battery_pct(tbl)
   else:
      return extract_paired_columns(tbl)

def get_value(cell):
   "Cell's value, as int or float if possible"
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


def extract_all():
   system = System()
   # TODO
   print(find_extract_table(heading_overall, "4col"))
   print(find_extract_table(heading_status,  "6col"))

   system.vips = find_extract_table(heading_pvbat, "vip")
   system.battery = Battery(
                 find_extract_table(heading_battery, "bat"), False)
   return system

system = extract_all()


from export import *
influx_write("10.5.2.1", 8086, "power", system)
