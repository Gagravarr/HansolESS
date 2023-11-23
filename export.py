# Licensed under the Apache License, Version 2.0
#
# Exports data extracted from a Hansol Technics AIO ESS to
#  various systems

from urllib.request import urlopen

def console_write(s):
   for t,p in (("Current",s.power),("30 Second Average",s.power_30s)):
      print("Power - %s" % t)
      for k in vars(p):
         v = getattr(p,k)
         dk = k.ljust(10)
         dv = ("%0.1f"%v).rjust(7) if v else ""
         print( " - %s %s" % (dk,dv))
      print("")

   print("Battery")
   print(" - Charge %%       %2d%%" % (s.battery.charge_pct))
   print(" - Charging     %s" % (str(s.battery.charging)).rjust(5))
   print("")

   print("Component Electrical Data")
   for vip in s.vips:
      v = lambda f: ("%0.1f" % f).rjust(6)
      print(" - %s" % vip.component)
      print("  * Voltage (V)    %s" % v(vip.voltage))
      print("  * Current (A)    %s" % v(vip.current))
      print("  * Power   (W)    %s" % v(vip.power))
   print("")

def json_write(system):
   import json
   data = {
       "Power": vars(system.power), 
       "Power_30s_Avg": vars(system.power_30s),
       "VIPs":  list(vars(v) for v in system.vips),  
       "Battery": vars(system.battery) 
   }
   print(  json.dumps(data, indent=2) )

def mqtt_write(host, port, topic, system):
   # TODO
   print(system)

def influx_write(base_url, db, username, password, system):
   if not base_url.endswith("/"):
      base_url += "/"
   url = base_url + "write?db=%s" % (db)

   lines = []
   _influx_vips(system.vips, lines)
   # TODO Rest

   data = "\n".join(lines)
   print(data)
   with urlopen(url, data.encode("utf-8")) as f:
      print(f.read())
      # TODO Check/use/etc

def _influx_vips(vips, lines):
   for vip in vips:
      f = ",".join("%s=%s" % (k,v) for k,v in vip.items())
      lines.append("power,kind=%s %s" % (vip.component, f))

# TODO prometheus
