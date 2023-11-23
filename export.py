# Licensed under the Apache License, Version 2.0
#
# Exports data extracted from a Hansol Technics AIO ESS to
#  various systems
# TODO Maybe have dedicated classes/clients?

from urllib.request import urlopen

def console_write(system):
   # TODO
   print(system)

def json_write(system):
   # TODO
   print(system)

def mqtt_write(host, port, topic, system):
   # TODO
   print(system)

def influx_write(url, db, username, password, system):
   if not url.endswith("/"):
      url += "/"
   # TODO Rest
   influx_write_vips(url, db, system.vips)
def influx_write_vips(base_url, db, vips):
   lines = []
   for vip in vips:
      f = ",".join("%s=%s" % (k,v) for k,v in vip.items())
      lines.append("power,kind=%s %s" % (vip.component, f))
   data = "\n".join(lines)
   print(data)

   # TODO Refactor
   url = base_url + "write?db=%s" % (db)
   print(url)
   with urlopen(url, data.encode("utf-8")) as f:
      print(f.read())

# TODO prometheus
