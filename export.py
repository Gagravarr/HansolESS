# Licensed under the Apache License, Version 2.0
#
# Exports data extracted from a Hansol Technics AIO ESS to
#  various systems
# TODO Maybe have dedicated classes/clients?

from urllib.request import urlopen

def influx_write_vips(host,port,db,vips):
   lines = []
   for thing, values in vips.items():
      f = ",".join("%s=%s" % (k,v) for k,v in values.items())
      lines.append("power,kind=%s %s" % (thing, f))
   data = "\n".join(lines)
   print(data)

   url = "http://%s:%d/write?db=%s" % (host, port, db)
   print(url)
   with urlopen(url, data.encode("utf-8")) as f:
      print(f.read())
