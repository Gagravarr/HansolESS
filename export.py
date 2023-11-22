# Licensed under the Apache License, Version 2.0
#
# Exports data extracted from a Hansol Technics AIO ESS to
#  various systems
# TODO Maybe have dedicated classes/clients?

from urllib.request import urlopen

def influx_write(host, port, db, system):
   influx_write_vips(host, port, db, system.vips)
def influx_write_vips(host, port, db, vips):
   lines = []
   for vip in vips:
      f = ",".join("%s=%s" % (k,v) for k,v in vip.items())
      lines.append("power,kind=%s %s" % (vip.component, f))
   data = "\n".join(lines)
   print(data)

   url = "http://%s:%d/write?db=%s" % (host, port, db)
   print(url)
   with urlopen(url, data.encode("utf-8")) as f:
      print(f.read())
