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
   # TODO MQTT
   print(system)


def influx_write(base_url, db, username, password, system):
   if not base_url.endswith("/"):
      base_url += "/"
   url = base_url + "write?db=%s" % (db)

   lines = []
   _influx_power(system.power, lines)
   _influx_vips(system.vips, lines)
   _influx_bat(system.battery, lines)

   data = "\n".join(lines)
   with urlopen(url, data.encode("utf-8")) as f:
      resp = f.read()
      if resp:
         print("Unexpected InfluxDB response:")
         print(resp)

def _influx_power(power, lines):
   for thing in vars(power):
      lines.append("power,kind=%s power=%0.1f" % (thing,getattr(power,thing)))
def _influx_vips(vips, lines):
   for vip in vips:
      f = ",".join("%s=%s" % (k,v) for k,v in vip.items())
      lines.append("electrical,kind=%s %s" % (vip.component, f))
def _influx_bat(battery, lines):
   lines.append("battery,kind=battery charge=%0.1f,charge_pct=%0d" %
                (battery.charge_01, battery.charge_pct))

# TODO prometheus
